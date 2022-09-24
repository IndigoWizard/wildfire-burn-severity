import ee
from ee import image
import folium
import webbrowser

#################### Earth Engine Configuration #################### 
# ########## Earth Engine Setup
# Triggering authentification to earth engine services
# Uncomment then execute only once > auth succecfull > put back as a comment:
ee.Authenticate()

# initializing the earth engine library
ee.Initialize()

# ##### earth-engine drawing method setup
def add_ee_layer(self, ee_image_object, vis_params, name):
  map_id_dict = ee.Image(ee_image_object).getMapId(vis_params)
  folium.raster_layers.TileLayer(
      tiles = map_id_dict['tile_fetcher'].url_format,
      attr = 'Map Data &copy; <a href="https://earthengine.google.com/">Google Earth Engine</a>',
      name = name,
      overlay = True,
      control = True
  ).add_to(self)

# configuring earth engine display rendering method in folium
folium.Map.add_ee_layer = add_ee_layer

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