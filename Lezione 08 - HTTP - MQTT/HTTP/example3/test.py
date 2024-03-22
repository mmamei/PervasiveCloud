import datetime
s = '2020-01-02 00:00:00'
d = datetime.datetime.strptime(s,'%Y-%m-%d %H:%M:%S')
print(d.timestamp() * 1000)