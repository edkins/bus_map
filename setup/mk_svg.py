import sys
import json

shapes = json.load(open(sys.argv[1]))

class Bounds:
    def __init__(self, shapes):
        minlat = 1000
        minlon = 1000
        maxlat = -1000
        maxlon = -1000
        for shape in shapes:
            for point in shape['points']:
                lat = point['lat']
                lon = point['lon']
                if lat < minlat: minlat = lat
                if lon < minlon: minlon = lon
                if lat > maxlat: maxlat = lat
                if lon > maxlon: maxlon = lon
        self.minlat = minlat
        self.minlon = minlon
        self.maxlat = maxlat
        self.maxlon = maxlon

    def scale(self, point):
        x = (point['lon'] - self.minlon) / (self.maxlon - self.minlon)
        y = (point['lat'] - self.minlat) / (self.maxlat - self.minlat)
        return Point(1000 * x, 1000 * (1-y))

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def str(self):
        return str(self.x) + ',' + str(self.y)

print('<?xml version="1.0" encoding="UTF-8" ?>')
print('<svg xmlns="http://www.w3.org/2000/svg" version="1.1">')

bounds = Bounds(shapes)
for shape in shapes:
    string = ''
    for point in shape['points']:
        string += bounds.scale(point).str() + ' '
    print('<polyline fill="none" stroke="rgba(0,0,0,0.1)" points="%s"/>' % string)

print('</svg>')

