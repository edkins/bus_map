import sys
import json
import random

def color(i):
    colors = ['#000','#00f','#0f0','#0ff','#f00','#f0f','#ff0']
    if i >= len(colors):
        return colors[-1]
    else:
        return colors[i]

class Bounds:
    def __init__(self):
        self.minlat = 43.591495
        self.minlon = -79.650423
        self.maxlat = 43.909681
        self.maxlon = -79.12274

    def scale(self, point):
        x = (point['lon'] - self.minlon) / (self.maxlon - self.minlon)
        y = 1 - (point['lat'] - self.minlat) / (self.maxlat - self.minlat)

        x2 = x - 0.35 * y
        y2 = y + 0.35 * x

        return Point(400 + 2000 * x2, 2000 * y2 - 600)

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def str(self):
        return str(self.x) + ',' + str(self.y)

data = json.load(open(sys.argv[1]))
print('<?xml version="1.0" encoding="UTF-8" ?>')
print('<svg xmlns="http://www.w3.org/2000/svg" version="1.1" width="2300" height="1500">')

bounds = Bounds()
for shape in data['paths']:
    string = ''
    points = shape['points']
    for point in points:
        string += bounds.scale(point).str() + ' '
    print('<polyline fill="none" stroke="rgba(0,0,0,0.2)" stroke-width="1" points="%s"/>' % string)

for endpoint in data['endpoints']:
    p0 = bounds.scale(endpoint)
    col = color(len(endpoint['path_ids']))
    print('<circle cx="%s" cy="%s" r="2" fill="%s"/>' % (p0.x, p0.y, col))

print('</svg>')

