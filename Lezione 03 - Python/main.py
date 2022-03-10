
'''
read file data.json

create a structure containing 'activitySegments' with:
[
{
'day':2017-11-01
'start time':10:18:40
'end time':10:23:00
'distance':100
'path':[[lat1,lng1],[lat2,lng2],...]
},...
]

create a leaflet map showing activity segments with different colors

create a bar graph with total distance per day

'''
import json

def d7(x):
    return x/10000000

with open('data.json') as f:
    dati = json.load(f)

segm = []
for x in dati['timelineObjects']:
    if 'activitySegment' in x and 'distance' in x['activitySegment']:
        x = x['activitySegment']
        day,start_time = x['duration']['startTimestamp'].split('T')
        start_time = start_time.split('.')[0]
        end_time = x['duration']['endTimestamp'].split('T')[1].split('.')[0]
        path = [[d7(x['startLocation']['latitudeE7']),
                 d7(x['startLocation']['longitudeE7'])]]
        if 'waypointPath'in x:
            for p in x['waypointPath']['waypoints']:
                path.append([d7(p['latE7']),d7(p['lngE7'])])
        path.append([d7(x['endLocation']['latitudeE7']),
                     d7(x['endLocation']['longitudeE7'])])
        segm.append({
            'day':day,
            'start time':start_time,
            'end time': end_time,
            'distance': x['distance'],
            'path': path
        })
print(segm)



def convert_line(path):
    line = ''
    for p in path:
        line += convert_point(p) + ', '
    return line

def convert_point(p):
    return f'new L.LatLng({p[0]}, {p[1]})'

colors = ['red','blue','yellow','green','black']
i = 0
polyline = ''
for s in segm:
    polyline += 'new L.Polyline(['+convert_line(s['path'])+'], {color: \''+colors[i]+'\',weight: 3,opacity: 0.5,smoothFactor: 1}).addTo(map);\n'
    i = (i + 1) % len(colors)

with open('leaflet.template') as f:
    temp = f.read()
temp = temp.replace('{{polyline}}',polyline).replace('{{center}}',str(segm[0]['path'][0]))
with open('map.html','w') as f:
    f.write(temp)

distXday = [[i,0] for i in range(31)]
distXday[0] = ['day', 'dist (m)']
for s in segm:
    day = int(s['day'].split('-')[-1])
    distXday[day][1] += s['distance']
print(distXday)


with open('bar.template') as f:
    temp = f.read()
temp = temp.replace('{{data}}',str(distXday))
with open('distXday.html','w') as f:
    f.write(temp)
