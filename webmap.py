import ee
from ee import image
import folium
import webbrowser

#################### Earth Engine Configuration #################### 
# ########## Earth Engine Setup
# Triggering authentification to earth engine services
# Uncomment then execute only once > auth succecfull > put back as a comment:
#ee.Authenticate()

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



#################### IMAGERY ANALYSIS ####################
# Area of Interest
aoi = ee.Geometry.Point([2.34059, 36.614425]).buffer(7500)

# Sentinel-2 L2A: August 12th 2022 - Pre-fire
pre_fire = ee.Image('COPERNICUS/S2_SR/20220812T103031_20220812T103132_T31SDA')

# Sentinel-2 L2A: August 20th 2022 - Post-fire
post_fire = ee.Image('COPERNICUS/S2_SR/20220820T103629_20220820T104927_T31SDA')

# True Color Image (TCI) 
pre_fire_tci = pre_fire.clip(aoi).divide(10000)
post_fire_tci = post_fire.clip(aoi).divide(10000)

# TCI visual parameters
tci_params = {
  'bands': ['B4',  'B3',  'B2'],
  'min': 0,
  'max': 1,
  'gamma': 2
}

#################### COMPUTED RASTER LAYERS ####################
##### TCI
m.add_ee_layer(pre_fire_tci, tci_params, 'Sentinel-2 TCI (Pre-fire)')

m.add_ee_layer(post_fire_tci, tci_params, 'Sentinel-2 TCI (Post-fire)')

##### Folium Map Layer Control
folium.LayerControl(collapsed=False).add_to(m)

#################### Generating map file #################### 

# Generating a file for the map and setting it to open on default browser
m.save('webmap.html')

# Opening the map file in default browser on execution
webbrowser.open('webmap.html')