import sys
import json

class Linelet:
    def __init__(self, lat0, lon0, lat1, lon1):
        self.lat0 = lat0
        self.lon0 = lon0
        self.lat1 = lat1
        self.lon1 = lon1

    def shape(self):
        return {'points':[{'lat':self.lat0,'lon':self.lon0},{'lat':self.lat1,'lon':self.lon1}]}

    def reverse(self):
        return Linelet(self.lat1, self.lon1, self.lat0, self.lon0)

    def __eq__(self, other):
        return self.lat0 == other.lat0 and self.lon0 == other.lon0 and self.lat1 == other.lat1 and self.lon1 == other.lon1
    def __ne__(self, other):
        return not (self == other)
    def __hash__(self):
        return hash((self.lat0,self.lon0,self.lat1,self.lon1))

class RoutePoint:
    def __init__(self, route, i):
        self.route = route
        self.i = i

    def __eq__(self, other):
        return self.route == other.route and self.i == other.i
    def __ne__(self, other):
        return not (self == other)
    def __hash__(self):
        return hash((self.route,self.i))

class RouteSet:
    def __init__(self):
        self.set = set()

    def add(self, route, i):
        self.set.add(RoutePoint(route, i))

class LineletInfo:
    def __init__(self):
        self.info = {}

    def add_linelet(self, route, i, point0, point1):
        linelet = Linelet(point0['lat'], point0['lon'], point1['lat'], point1['lon'])
        if linelet not in self.info:
            self.info[linelet] = RouteSet()
        self.info[linelet].add(route,i)

    def add_shape(self, shape):
        route = shape['id']
        points = shape['points']
        length = len(points)-1
        for i in range(length):
            self.add_linelet(route, i, points[i], points[i+1])
            self.add_linelet(route,-1-i, points[length-i], points[length-i-1])

    def linelets(self):
        return self.info.keys()

def pairs(list):
    result = []
    for i in range(len(list)-1):
        result.append((list[i],list[i+1]))
    return result

def main():
    shapes = json.load(open(sys.argv[1]))
    info = LineletInfo()
    for shape in shapes:
        info.add_shape(shape)

    paths = []
    encountered = set()
    for key in info.linelets():
        if key not in encountered:
            paths.append(key.shape())
            encountered.add(key.reverse())

    json.dump(paths, sys.stdout)

main()

