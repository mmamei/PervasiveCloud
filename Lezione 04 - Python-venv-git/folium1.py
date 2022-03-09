import folium

# https://python-visualization.github.io/folium/quickstart.html

m = folium.Map(location=[45.5236, -122.6750])
folium.Marker([45.3288, -121.6625], popup="<i>Mt. Hood Meadows</i>").add_to(m)
folium.Marker([45.3311, -121.7113], popup="<b>Timberline Lodge</b>").add_to(m)
folium.PolyLine([[45.3288, -121.6625],[45.3311, -121.7113]], color="red", weight=2.5, opacity=1).add_to(m)

m.save("index.html")
