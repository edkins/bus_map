import json
import sys

data = json.load(sys.stdin)
if not isinstance(data, list):
    raise ValueError('Expecting list')
print('[')
i = 0
for i in range(len(data)):
    string = json.dumps(data[i])
    if i == len(data)-1:
        print(string)
    else:
        print(string + ',')
print(']')

