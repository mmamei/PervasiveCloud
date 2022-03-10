import json
with open('file.json') as f:
    x = json.load(f)

'''
{'Marco':[30,28],
'Matteo':[30],
'Luca':[24]}
'''
y = {}
for p,v in x:
    if p in y:
        y[p].append(v)
    else:
        y[p] = [v]

for p,v in y.items():
    print(p,'--->',sum(v)/len(v))


