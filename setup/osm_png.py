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
height = 1500
img = numpy.empty([height,width],'i4')
hidden = numpy.empty([height,width],'i4')

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

nodes = {}
for node in data['nodes']:
    nodes[node['node_id']] = node

for way in data['ways']:
    color = [(255,0,0),(0,255,0),(0,0,255)][hash(way['name']) % 3]
    color = scale_color(color,1)
    node_ids = way['node_ids']
    for i in range(len(node_ids)-1):
        nid0 = node_ids[i]
        nid1 = node_ids[i+1]
        (x0,y0) = bounds.scale(nodes[nid0])
        (x1,y1) = bounds.scale(nodes[nid1])
        distance = int(max(abs(x0-x1),abs(y0-y1)))+1
        for j in range(distance+1):
            x = int((x0 * (distance-j) + x1 * j) / distance)
            y = int((y0 * (distance-j) + y1 * j) / distance)
            for y1 in range(y-1,y+2):
                for x1 in range(x-1,x+2):
                    if x1 >= 0 and x1 < width and y1 >= 0 and y1 < height:
                        hidden[y1][x1] = color

data2 = json.load(open(sys.argv[2]))
for shape in data2['paths']:
    for point in shape['points']:
        p0 = bounds.scale(point)
        x = int(p0[0])
        y = int(p0[1])
        if x >= 0 and x < width and y >= 0 and y < height:
            if hidden[y][x] != 0:
                img[y][x] = hidden[y][x]
            else:
                img[y][x] = 0xffffffff

Image.fromarray(img, 'RGBA').show()

