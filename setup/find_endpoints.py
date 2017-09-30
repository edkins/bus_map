import json
import sys
from multiset import Multiset

endpoints = {}

paths = json.load(open(sys.argv[1]))

for path in paths:
    path_id = path['path_id']
    points = path['points']
    p0 = (points[0]['lat'], points[0]['lon'])
    p1 = (points[-1]['lat'], points[-1]['lon'])
    if p0 not in endpoints: endpoints[p0] = Multiset()
    if p1 not in endpoints: endpoints[p1] = Multiset()

    endpoints[p0].add(path_id)
    endpoints[p1].add(path_id)

e = []
i = 0
for key in endpoints:
    endpoint_id = str(i)
    i += 1
    path_ids = list(sorted(endpoints[key]))
    e.append({'endpoint_id':endpoint_id, 'path_ids':path_ids, 'lat':key[0], 'lon':key[1]})

json.dump({'endpoints':e, 'paths':paths}, sys.stdout)

