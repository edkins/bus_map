import sys
import json

shapes = json.load(open(sys.argv[1]))

class Linelet:
    def __init__(self, point0, point1):
        if (point0['lat'], point0['lon']) < (point1['lat'], point1['lon']):
            self.lat0 = point0['lat']
            self.lon0 = point0['lon']
            self.lat1 = point1['lat']
            self.lon1 = point1['lon']
        else:
            self.lat1 = point0['lat']
            self.lon1 = point0['lon']
            self.lat0 = point1['lat']
            self.lon0 = point1['lon']

    def str(self):
        return str(self.lat0)+','+str(self.lon0)+','+str(self.lat1)+','+str(self.lon1)

    def shape(self):
        return {'points':[{'lat':self.lat0,'lon':self.lon0},{'lat':self.lat1,'lon':self.lon1}]}

def pairs(list):
    result = []
    for i in range(len(list)-1):
        result.append((list[i],list[i+1]))
    return result

linelets = {}
for shape in shapes:
    for (point0,point1) in pairs(shape['points']):
        linelet = Linelet(point0,point1)
        linelets[linelet.str()] = linelet

paths = []
for key in linelets:
    paths.append(linelets[key].shape())

json.dump(paths, sys.stdout)
