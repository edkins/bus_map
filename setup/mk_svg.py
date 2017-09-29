import sys
import json

shapes = json.load(open(sys.argv[1]))

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

        return Point(200 + 1000 * x2, 1000 * y2 - 300)

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def str(self):
        return str(self.x) + ',' + str(self.y)

print('<?xml version="1.0" encoding="UTF-8" ?>')
print('<svg xmlns="http://www.w3.org/2000/svg" version="1.1">')

bounds = Bounds()
for shape in shapes:
    string = ''
    for point in shape['points']:
        string += bounds.scale(point).str() + ' '
    print('<polyline fill="none" stroke="rgba(0,0,0,0.2)" stroke-width="3" points="%s"/>' % string)

print('</svg>')

