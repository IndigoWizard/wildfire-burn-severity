import folium
import webbrowser

#################### MAIN MAP ####################
m = folium.Map(location = [36.606519, 2.372596], tiles='OpenStreetMap', zoom_start = 12, control_scale = True)

basemap2 = folium.TileLayer('cartodbdark_matter', name='Dark Matter')
basemap2.add_to(m)


folium.LayerControl(collapsed=False).add_to(m)

#################### Generating map file #################### 

# Generating a file for the map and setting it to open on default browser
m.save('webmap.html')

# Opening the map file in default browser on execution
webbrowser.open('webmap.html')