from PIL import Image
import numpy
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

width = 2000
height = 1000
img = numpy.empty([height,width],'i4')
proximity = numpy.empty([height,width],'i4')

node_ways = {}
for way in data['ways']:
    way_id = hash(way['name'])
    for node_id in way['node_ids']:
        if node_id not in node_ways:
            node_ways[node_id] = set()
        node_ways[node_id].add(way_id)

def color(way_ids):
    if len(way_ids) == 1:
        for way_id in way_ids:
            return [(255,0,0),(0,255,0),(0,0,255)][way_id % 3]
    else:
        return (255,255,255)

def scale_color(color, scale):
    scale = max(0, min(1, scale))
    return int(color[0] * scale) | int(color[1] * scale) << 8 | int(color[2] * scale) << 16 | 0xff000000

for node in data['nodes']:
    node_id = node['node_id']
    node_color = color(node_ways[node_id])
    p0 = bounds.scale(node)
    x0 = int(p0[0])
    y0 = int(p0[1])
    for y in range(max(0,y0-10), min(height,y0+11)):
        for x in range(max(0,x0-10), min(width,x0+11)):
            prox = max(0, 100 - (x - x0) * (x - x0) - (y - y0) * (y - y0))

            col = scale_color(node_color, prox / 100)
            if prox > proximity[y][x]:
                proximity[y][x] = prox
                img[y][x] = col;

Image.fromarray(img, 'RGBA').show()

