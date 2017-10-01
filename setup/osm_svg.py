import json
import sys

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

        return (400 + 2000 * x2, 2000 * y2 - 600)

data = json.load(open(sys.argv[1]))
bounds = Bounds()

print('<?xml version="1.0" encoding="UTF-8" ?>')
print('<svg xmlns="http://www.w3.org/2000/svg" version="1.1" width="2300" height="1500">')

for node in data['nodes']:
    p0 = bounds.scale(node)
    print('<circle cx="%s" cy="%s" r="1" fill="black"/>' % (p0[0], p0[1]))

print('</svg>')
