import csv
import sys
import json

shape = None
shapes = []
with open(sys.argv[1]) as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        shape_id = str(row['shape_id'])
        lat = float(row['shape_pt_lat'])
        lon = float(row['shape_pt_lon'])
        if shape == None or shape['id'] != shape_id:
            if shape != None: shapes.append(shape)
            shape = {'id':shape_id, 'points':[]}

        shape['points'].append({'lat':lat, 'lon':lon})
shapes.append(shape)

json.dump(shapes, sys.stdout)
