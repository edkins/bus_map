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

    def p0(self):
        return (self.lat0, self.lon0)
    def p1(self):
        return (self.lat1, self.lon1)

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.lat0 == other.lat0 and self.lon0 == other.lon0 and self.lat1 == other.lat1 and self.lon1 == other.lon1
    def __ne__(self, other):
        return not (self == other)
    def __hash__(self):
        return hash((self.lat0,self.lon0,self.lat1,self.lon1))

class RoutePoint:
    def __init__(self, route, i):
        self.route = route
        self.i = i

    def next(self):
        return RoutePoint(self.route, self.i + 1)

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.route == other.route and self.i == other.i
    def __ne__(self, other):
        return not (self == other)
    def __hash__(self):
        return hash((self.route,self.i))

class RouteSet:
    def __init__(self):
        self.set = set()

    def add(self, route, i):
        self.set.add(RoutePoint(route, i))

    def add_point(self, rp):
        self.set.add(rp)

    def next(self):
        result = RouteSet()
        for rp in self.set:
            result.add_point(rp.next())
        return result

    def str(self):
        return ','.join(sorted([rp.route for rp in self.set]))

    def forward_routes(self):
        return sorted([rp.route for rp in self.set if not rp.route.endswith("'")])

    def reverse_routes(self):
        return sorted([rp.route for rp in self.set if rp.route.endswith("'")])

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.set == other.set
    def __ne__(self, other):
        return not (self == other)

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

    def linelets(self):
        return self.info.keys()

    def split_shape(self, shape):
        points = shape['points']
        length = len(points)-1
        routeset = None
        paths = []
        path = [(points[0]['lat'],points[0]['lon'])]
        for i in range(length):
            linelet = Linelet(points[i]['lat'], points[i]['lon'], points[i+1]['lat'], points[i+1]['lon'])
            next_routeset = self.info[linelet]
            if routeset != None and routeset.next() != next_routeset:
                paths.append((tuple(path),routeset))
                path = [linelet.p0()]
            path.append(linelet.p1())
            routeset = next_routeset
        paths.append((tuple(path),routeset))
        return paths

def pairs(list):
    result = []
    for i in range(len(list)-1):
        result.append((list[i],list[i+1]))
    return result

def reverse_shape(shape):
    return {'id':shape['id']+"'", 'points':list(reversed(shape['points']))}

def to_shape(path,forward,reverse,path_id):
    result = []
    for p in path:
        result.append({'lat':p[0], 'lon':p[1]})
    return {'points':result,'forward_routes':forward,'reverse_routes':reverse,'path_id':path_id}

def main():
    shapes = json.load(open(sys.argv[1]))
    info = LineletInfo()
    for shape in shapes:
        info.add_shape(shape)
        info.add_shape(reverse_shape(shape))

    paths = []
    encountered = set()
    i = 0
    for shape in shapes:
        for (path,routeset) in info.split_shape(shape):
            if path not in encountered:
                paths.append(to_shape(path, routeset.forward_routes(), routeset.reverse_routes(), str(i)))
                i += 1
                encountered.add(path)
                encountered.add(tuple(reversed(path)))

    json.dump(paths, sys.stdout)

main()

