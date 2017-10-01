import xml.parsers.expat
import json
import sys

class NdState:
    def __init__(self):
        self.ref = None

    def attrs(self, name, attrs):
        self.ref = attrs['ref']

    def enter(self, name, attrs):
        return None

    def process(self, name, value):
        return None

    def end(self):
        return self.ref

class TagState:
    def __init__(self):
        self.k = None
        self.v = None

    def attrs(self, name, attrs):
        self.k = attrs['k']
        self.v = attrs['v']

    def enter(self, name, attrs):
        return None

    def process(self, name, value):
        return None

    def end(self):
        return (self.k, self.v)

class WayState:
    def __init__(self):
        self.nd = NdState()
        self.tag = TagState()

    def attrs(self, name, attrs):
        self.id = attrs['id']
        self.node_ids = []
        self.name = None
        self.highway = None

    def enter(self, name, attrs):
        if name == 'nd':
            return self.nd
        elif name == 'tag':
            return self.tag
        else:
            return None

    def process(self, name, value):
        if name == 'nd':
            self.node_ids.append(value)
        elif name == 'tag':
            if value[0] == 'name':
                self.name = value[1]
            elif value[0] == 'highway':
                self.highway = value[1]

    def end(self):
        if self.highway in ['motorway','trunk','primary','secondary','tertiary']:
            return {'way_id':self.id,'node_ids':self.node_ids,'name':self.name,'highway':self.highway}
        else:
            return None

class NodeState:
    def __init__(self):
        pass

    def attrs(self, name, attrs):
        self.id = attrs['id']
        self.lat = float(attrs['lat'])
        self.lon = float(attrs['lon'])

    def enter(self, name, attrs):
        return None

    def process(self, name, value):
        return None

    def end(self):
        return {'node_id':self.id, 'lat':self.lat, 'lon':self.lon}

class OsmState:
    def __init__(self):
        self.way = WayState()
        self.node = NodeState()
        self.ways = []
        self.nodes = []
        self.interesting_node_ids = set()
        self.care = 'way'

    def attrs(self, name, attrs):
        pass

    def enter(self, name, attrs):
        if name == 'way' and self.care == 'way':
            return self.way
        elif name == 'node' and self.care == 'node':
            return self.node
        else:
            return None

    def process(self, name, value):
        if value == None:
            return
        elif name == 'way':
            self.ways.append(value)
            for node_id in value['node_ids']:
                self.interesting_node_ids.add(node_id)
        elif name == 'node':
            if value['node_id'] in self.interesting_node_ids:
                self.nodes.append(value)
    
    def end(self):
        return None

class RootState:
    def __init__(self):
        self.osm = OsmState()

    def attrs(self, name, attrs):
        pass

    def enter(self, name, attrs):
        if name == 'osm':
            return self.osm
        else:
            return None

    def process(self, name, value):
        pass

    def end(self):
        return None

class State:
    def __init__(self):
        self.way = WayState()
        self.root = RootState()
        self.stack = [self.root]

    def start_element(self, name, attrs):
        sub = None
        if self.stack[-1] != None:
            sub = self.stack[-1].enter(name, attrs)
        self.stack.append(sub)
        if sub != None:
            sub.attrs(name, attrs)

    def end_element(self, name):
        value = None
        if self.stack[-1] != None:
            value = self.stack[-1].end()
        self.stack[-1:] = []
        if self.stack[-1] != None:
            self.stack[-1].process(name, value)

state = State()

file = open(sys.argv[1], 'rb')
p = xml.parsers.expat.ParserCreate()
p.StartElementHandler = state.start_element
p.EndElementHandler = state.end_element
p.ParseFile(file)

state.root.osm.care = 'node'

file = open(sys.argv[1], 'rb')
p = xml.parsers.expat.ParserCreate()
p.StartElementHandler = state.start_element
p.EndElementHandler = state.end_element
p.ParseFile(file)

json.dump({'ways':state.root.osm.ways, 'nodes':state.root.osm.nodes}, sys.stdout)

