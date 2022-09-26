import ee
from ee import image
import folium
from branca.element import Template, MacroElement
import geemap
import webbrowser
# importing aos.py that contains the "AOS" variable with long geojson
import aos

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
m = folium.Map(location = [36.606500, 2.352500], tiles='OpenStreetMap', zoom_start = 12, control_scale = True)

basemap2 = folium.TileLayer('cartodbdark_matter', name='Dark Matter')
basemap2.add_to(m)

#################### IMAGERY ANALYSIS ####################
# Area of Interest
# fetching the aos (area of study) variable from roi.py where the very long geojson is strored as to not occupy a lot of space in this main webmap.py file
#aoi = ee.Geometry.Point([2.34059, 36.614425]).buffer(7500)
aoi = aos.aos

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
  'max': 0.3,
  'gamma': 0.8
}

####################  INDECES #################### 
# ##### NBR (Normalized Burn Ratio)
# Computing both pre-fire and post-fire NBR data while using the same visual parameters to display both as greyscale
def get_NBR(image):
  return image.normalizedDifference(['B8', 'B12'])

pre_fire_NBR = get_NBR(pre_fire.clip(aoi))
post_fire_NBR = get_NBR(post_fire.clip(aoi))

# NBR visual parameters (applies to both pre/post fire images as greyscale)
NBR_params = {
  'min': -1,
  'max': 1,
  'palette': ['black', 'white'],
}

# ##### Delta NBR (dNBR)
dNBR = pre_fire_NBR.subtract(post_fire_NBR)
# dNBR isual parameters for greyscale styling
dNBR_params = {
  'min' : -0.12,
  'max': 0.82,
  'palette': ['black', 'white']
}

# dNBR Color Ramp styling
dNBR_cr_params = {
  'min': -0.12,
  'max': 0.82,
  'palette': ['#1c742c', '#2aae29', '#a1d574', '#f8ebb0', '#f7a769', '#e86c4e', '#902cd6']
}

# ########## ANALYSIS RESULTS CLASSIFICATION
# ##### NDVI classification: 7 classes

dNBR_classified = ee.Image(dNBR) \
  .where(dNBR.gte(-0.12).And(dNBR.lt(0)), 1) \
  .where(dNBR.gte(0).And(dNBR.lt(0.1)), 2) \
  .where(dNBR.gte(0.1).And(dNBR.lt(0.27)), 3) \
  .where(dNBR.gte(0.27).And(dNBR.lt(0.37)), 4) \
  .where(dNBR.gte(0.37).And(dNBR.lt(0.44)), 5) \
  .where(dNBR.gte(0.44).And(dNBR.lt(0.66)), 6) \
  .where(dNBR.gte(0.66).And(dNBR.lt(0.82)), 7) \
  .where(dNBR.gte(0.82), 8) \

dNBR_classified_params = {
  'min': 1,
  'max': 7,
  'palette': ['#1c742c', '#2aae29', '#a1d574', '#f8ebb0', '#f7a769', '#e86c4e', '#902cd6']
}

dNBR_classified_masked = dNBR_classified.updateMask(dNBR_classified.gte(4))

#################### Custom Visual Displays ####################
dem = ee.Image('CGIAR/SRTM90_V4').clip(aoi)
contours = geemap.create_contours(dem, 0, 905, 25, region=aoi)
contours_params = {
  'min': 0,
  'max': 1000,
  'palette': ['#440044', '#00FFFF', '#00FFFF', '#00FFFF'],
  'opacity': 0.3
}


#################### MAP LEGEND ####################

legend_setup = """
{% macro html(this, kwargs) %}
<!doctype html>
<html lang="en">
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <meta name="robots" content="index,follow,max-image-preview:large" />
        <title>Wildfire Burn Severity Analysis</title>
        <link rel="stylesheet" href="//code.jquery.com/ui/1.12.1/themes/base/jquery-ui.css">
        <link rel="stylesheet" href="src/ui.css">
        <script src="https://code.jquery.com/jquery-1.12.4.js"></script>
        <script src="https://code.jquery.com/ui/1.12.1/jquery-ui.js"></script>

        <script>
            $(function() {
                $("#ui-container, #title-container, #project-container").draggable({
                    start: function(event, ui) {
                        $(this).css({
                            right: "auto",
                            top: "auto",
                            bottom: "auto"
                        });
                    }
                });
            });
        </script>
    </head>

  <body>
  <div class="ui-container" id="title-container">
    <div class="map-title">
      <p>Wildfire Burn Severity Analysis</p>
    </div>
  </div>

  <div id="ui-container" class="ui-container">

        <div class="project-source">
          <div class="project-logo">
              <a href="https://github.com/IndigoWizard/mega-port-environment/tree/develop" title="Go to repository" target="_blank">
                <i class="fa fa-github" aria-hidden="true" id="icons"></i>
              </a>
          </div>

          <div class="project-info">
            <a href="https://github.com/IndigoWizard/wildfire-burn-severity" title="Go to repository" target="_blank"><p  class="project-link"  id="icons">IndigoWizard/mega-port-environment</p></a>
            <div class="project-stats">
              <a href="https://github.com/IndigoWizard/wildfire-burn-severity/" target="_blank"><i class="fa fa-link" aria-hidden="true" id="icons"><span class="ghtext"> Check it!</span></i></a>
              <a href="https://github.com/IndigoWizard/wildfire-burn-severity/stargazers" target="_blank"><i class="fa fa-star" aria-hidden="true" id="icons"><span class="ghtext"> Star it!</span></i></a>
              <a href="https://github.com/IndigoWizard/wildfire-burn-severity/network/members" target="_blank"><i class="fa fa-code-fork" aria-hidden="true" id="icons"><span class="ghtext"> Fork it!</span></i></a>
            </div>
          </div>
        </div>

        <div class="leaflet-control-layers-separator"></div>

      <div class='legend-title'>Legend</div>

      <div class="index-container">

        <div class='legend-scale' id="dNBR">
            <h4>Classified dNBR</h4>
            <ul class='legend-labels'>
              <li><span style='background:#902cd6;opacity:0.8;'></span>High Severity Burns</li>
              <li><span style='background:#e86c4e;opacity:0.8;'></span>Moderate-High Severity Burns</li>
              <li><span style='background:#f7a769;opacity:0.8;'></span>Moderate-Low Severity Burns</li>
              <li><span style='background:#f8ebb0;opacity:0.8;'></span>Low Severity Burns</li>
              <li><span style='background:#a1d574;opacity:0.8;'></span>Unburned</li>
              <li><span style='background:#2aae29;opacity:0.8;'></span>Enhanced Regrowth (Low)</li>
              <li><span style='background:#1c742c;opacity:0.8;'></span>Enhanced Regrowth (High)</li>
            </ul>
        </div>

        <div class="index-gradient">

          <div class="index-gradient-container">
            <div class='legend-scale' id="NBRGS">
              <h4>NBR Greyscale</h4>
              <ul class='legend-labels'>
                <li id="greyscale">-1<span id="nbr-greyscale"></span>1</li>
              </ul>
          </div>
        </div>

      </div>
  </div>

  </body>
</html>
{% endmacro %}
"""
# configuring the legend
legend = MacroElement()
legend._template = Template(legend_setup)

# adding legend to the map
m.get_root().add_child(legend)

#################### COMPUTED RASTER LAYERS ####################
##### TCI
m.add_ee_layer(pre_fire_tci, tci_params, 'Sentinel-2 TCI (Pre-fire)')
m.add_ee_layer(post_fire_tci, tci_params, 'Sentinel-2 TCI (Post-fire)')

##### NBR
m.add_ee_layer(pre_fire_NBR, NBR_params, 'Pre-Fire NBR')
m.add_ee_layer(post_fire_NBR, NBR_params, 'Post-Fire NBR')

##### Delta NBR
m.add_ee_layer(dNBR, dNBR_params, 'dNBR')
m.add_ee_layer(dNBR, dNBR_cr_params, 'dNBR - Burn Severity')
m.add_ee_layer(dNBR_classified, dNBR_classified_params, 'Classified dNBR')
m.add_ee_layer(dNBR_classified_masked, dNBR_classified_params, 'Burned Surface Area')

##### Contours
m.add_ee_layer(contours, contours_params, 'Contour lines')

##### Folium Map Layer Control
folium.LayerControl(collapsed=False).add_to(m)

#################### Generating map file #################### 

# Generating a file for the map and setting it to open on default browser
m.save('webmap.html')

# Opening the map file in default browser on execution
webbrowser.open('webmap.html')