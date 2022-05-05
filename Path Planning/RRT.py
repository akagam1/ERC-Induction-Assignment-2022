import matplotlib.pyplot as plt
import time
from shapely.geometry import Polygon, Point
import numpy as np
import math

class Node:

	def __init__(self, x, y, parent, isStart=False):
		self.x = x
		self.y = y 
		self.parent = parent
		self.isStart = isStart

	def coordinates(self):
		return (self.x, self.y)

class Map:

	def __init__ (self, start, goal, fig, ax):
		self.start = start
		self.goal = goal
		self.fig = fig
		self.ax = ax
		self.plt = plt

		self.nodes = []
		self.obstacles = []

		self.xStart, self.yStart = self.start
		self.nodes.append(Node(self.xStart, self.yStart, 0, True))

		self.goalFlag = False

		self.neighbourhood = []
		self.step = 5

		self.validConnects = []
		self.validConnectsIndex = []
		self.edges = {}

	def totalNodes(self):
		return len(self.nodes)

	def drawObs(self, obs_list):
		for i in range(len(obs_list)):
			x, y = obs_list[i].exterior.xy
			self.obstacles.append(obs_list[i])
			plt.plot(x, y, c="black")
			plt.show()

	def drawMap(self):
		startNode = plt.Circle(self.start, 2, color='darkgreen')
		goalNode = plt.Circle(self.goal, 2, color='red')
		self.ax.add_patch(startNode) 
		self.ax.add_patch(goalNode)

	def drawPath(self, child):
		parent = self.nodes[child].parent
		xp,yp = self.nodes[parent].coordinates()
		xc,yc = self.nodes[child].coordinates()
		line = plt.Line2D((xc,xp),(yc,yp),color='aqua')
		self.ax.add_line(line)
		return parent

	def collision(self, x,y):
		point = Point(x,y)
		for i in range(len(self.obstacles)):
			if point.within(self.obstacles[i]):
				return True
		return False

	def stepNode(self, p1, p2):
		d = self.distance(p1,p2)
		dmax = self.step
		xrand, yrand = p1
		x,y = p2

		if xrand == self.goal[0] and yrand == self.goal[1]:
			if d > dmax:
				u = dmax/d
				xNew = ((d-dmax)*x+(dmax)*xrand)/d
				yNew = ((d-dmax)*y+(dmax)*yrand)/d
				return (xNew,yNew)

			else:
				self.goalFlag = True
				return self.goal

		elif d>dmax:
			u = dmax/d
			xNew = ((d-dmax)*x+(dmax)*xrand)/d
			yNew = ((d-dmax)*y+(dmax)*yrand)/d
			if (x-self.goal[0])**2 + (y-self.goal[1])**2 <= 4:
				self.goalFlag = True
				return self.goal
			else:
				return (xNew,yNew)
		else:
			if (xrand-self.goal[0])**2 + (yrand-self.goal[1])**2 <= 4:
				self.goalFlag = True
				return self.goal
			else:
				return (xrand,yrand)


	def makeNode(self):
		self.validConnects = []
		choice = np.random.rand()

		if choice >= 0.7:
			for i in range(len(self.nodes)):
				p = self.nodes[i].coordinates()
				pNew = self.goal
				distance = self.distance(p,pNew)
				check = self.edgeCheck(pNew,p)
				if not check:
					self.validConnects.append(i)
			if len(self.validConnects) == 0:
				x,y = self.expand()
			else:
				x,y = self.goal

		else:
			x, y = self.expand()

		dmin = 100000
		index = 0
		for i in range(len(self.validConnects)):
			if self.distance((x,y),self.nodes[self.validConnects[i]].coordinates()) < dmin:
				dmin = self.distance((x,y),self.nodes[self.validConnects[i]].coordinates())
				index = self.validConnects[i]
		point = self.stepNode((x,y),self.nodes[index].coordinates())
		#point = (x,y)
		self.drawEdge(point, self.nodes[index].coordinates(),len(self.nodes),index)
		node = plt.Circle(point, 1, color='blue')
		self.ax.add_patch(node)
		self.nodes.append(Node(point[0],point[1],index))

		currentNode = len(self.nodes) - 1
		return self.goalFlag

	def expand(self):
		notValid = True
		while notValid:
			x = np.random.rand()*100
			y = np.random.rand()*100
			notValid = self.collision(x,y)
			self.validConnects = []
			if notValid == False:
				for i in range(len(self.nodes)):
					p = self.nodes[i].coordinates()
					pNew = (x,y)
					distance = self.distance(p,pNew)
					check = self.edgeCheck(pNew,p)
					if not check:
						self.validConnects.append(i)
				if len(self.validConnects) == 0:
					notValid = True
		return (x,y)
		
	def edgeCheck(self,pNew,p):
		xNew, yNew = pNew
		x, y = p

		for i in range(len(self.obstacles)):
			for j in range(1001):
				u = j/1000
				v = 1-u
				xTemp = (u*x + v*xNew)
				yTemp = (u*y + v*yNew)
				point = Point(xTemp,yTemp)
				if point.within(self.obstacles[i]):
					return True
		return False

	def distance(self, p1, p2):
		x1, y1 = p1
		x2, y2 = p2
		dist = (x1-x2)**2 + (y1-y2)**2
		return dist**0.5 

	def drawEdge(self, p1, p2, i1, i2):
		xc,yc = p1
		xp, yp = p2
		line = plt.Line2D((xc,xp),(yc,yp),color='red')
		self.ax.add_line(line)
		self.edges[f"{i1}-{i2}"] = line #stores edge line in dictionary with key as childIndex-parentIndex