import matplotlib.pyplot as plt
import time
from shapely.geometry import Polygon
from RRT import *

plt.ion()
fig, ax = plt.subplots()
plt.xlim(0,105)
plt.ylim(-5,105)
fig.canvas.manager.set_window_title('RRT Visualizer')
plt.draw()

obstacles = [[(40,0),(40,40),(50,50),(60,40),(50,40)],
[(10,10),(20,20),(10,30),(0,20)],
[(50,60),(70,80),(60,100),(40,80),(45,100)],
[(70,20),(90,20),(80,40)]]

polygon = [Polygon(obstacles[i]) for i in range(len(obstacles))]

"""polygon = [Polygon([(40,0),(40,40),(50,50),(60,40),(50,40)]), 
           Polygon([(10,10),(20,20),(10,30),(0,20)]),
           Polygon([(50,60),(70,80),(60,100),(40,80),(45,100)]),
           Polygon([(70,20),(90,20),(80,40)])]"""

graph = Map((1,1),(100,1),1,fig,ax)
graph.drawObs(polygon)
graph.drawMap()

goal = False

while not goal:
   goal = graph.makeNode()
   fig.canvas.draw_idle()
   plt.pause(0.05)

child = graph.totalNodes() - 1
start = False

while not start:
    current = graph.drawPath(child)
    fig.canvas.draw_idle()
    plt.pause(0.1)
    child = current
    if child == 0:
        start = True
plt.waitforbuttonpress()