import streamlit as st
import ee
import geemap
import folium
from streamlit_folium import folium_static
from datetime import datetime, timedelta
import json

st.set_page_config(
    page_title="Wildfire Burn Severity Analysis",
    page_icon="https://cdn-icons-png.flaticon.com/512/7204/7204183.png",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
    'Get help': "https://github.com/IndigoWizard/wildfire-burn-severity",
    'Report a bug': "https://github.com/IndigoWizard/wildfire-burn-severity/issues",
    'About': "This app was developped by [IndigoWizard](https://github.com/IndigoWizard/wildfire-burn-severity) for the purpose of environmental monitoring and geospatial analysis"
    }
)

# Initializing the Earth Engine library
# Use ee.Initialize() only on local machine! Comment back before deployement (Unusable on deployment > use geemap init+auth bellow)
#ee.Initialize()
# geemap auth + initialization for cloud deployment
@st.cache_data(persist=True)
def ee_authenticate(token_name="EARTHENGINE_TOKEN"):
    geemap.ee_initialize(token_name=token_name)

# Earth Engine drawing method setup
def add_ee_layer(self, ee_image_object, vis_params, name):
    map_id_dict = ee.Image(ee_image_object).getMapId(vis_params)
    layer = folium.raster_layers.TileLayer(
        tiles=map_id_dict['tile_fetcher'].url_format,
        attr='Map Data &copy; <a href="https://earthengine.google.com/">Google Earth Engine</a>',
        name=name,
        overlay=True,
        control=True
    )
    layer.add_to(self)
    return layer

# Configuring Earth Engine display rendering method in Folium
folium.Map.add_ee_layer = add_ee_layer

# Defining a function to create and filter a GEE image collection for results
def satCollection(cloudRate, initialDate, updatedDate, aoi):
    collection = ee.ImageCollection('COPERNICUS/S2_SR') \
        .filter(ee.Filter.lt("CLOUDY_PIXEL_PERCENTAGE", cloudRate)) \
        .filterDate(initialDate, updatedDate) \
        .filterBounds(aoi)
    
    # Defining a function to clip the colleciton to the area of interst
    def clipCollection(image):
        return image.clip(aoi).divide(10000)
    # clipping the collection
    collection = collection.map(clipCollection)
    return collection

# Upload function
last_uploaded_centroid = None

def upload_files_proc(upload_files):
    # A global variable to track the latest geojson uploaded
    global last_uploaded_centroid
    # Setting up a variable that takes all polygons/geometries within the same/different geojson
    geometry_aoi_list = []

    for upload_file in upload_files:
        bytes_data = upload_file.read()
        geojson_data = json.loads(bytes_data)

        if 'features' in geojson_data and isinstance(geojson_data['features'], list):
            # Handle GeoJSON files with a 'features' list
            features = geojson_data['features']
        elif 'geometries' in geojson_data and isinstance(geojson_data['geometries'], list):
            # Handle GeoJSON files with a 'geometries' list
            features = [{'geometry': geo} for geo in geojson_data['geometries']]
        else:
            # handling cases of unexpected file format or missing 'features' or 'geometries'
            continue

        for feature in features:
            if 'geometry' in feature and 'coordinates' in feature['geometry']:
                coordinates = feature['geometry']['coordinates']
                geometry = ee.Geometry.Polygon(coordinates) if feature['geometry']['type'] == 'Polygon' else ee.Geometry.MultiPolygon(coordinates)
                geometry_aoi_list.append(geometry)

                # Update the last uploaded centroid
                last_uploaded_centroid = geometry.centroid(maxError=1).getInfo()['coordinates']

    if geometry_aoi_list:
        geometry_aoi = ee.Geometry.MultiPolygon(geometry_aoi_list)
    else:
        geometry_aoi = ee.Geometry.Point([16.25, 36.65])

    return geometry_aoi


# Time input processing function
def date_input_proc(input_date, time_range):
    end_date = input_date
    start_date = input_date - timedelta(days=time_range)
    
    str_start_date = start_date.strftime('%Y-%m-%d')
    str_end_date = end_date.strftime('%Y-%m-%d')
    return str_start_date, str_end_date

# Main function to run the Streamlit app
def main():
    # initiate gee 
    ee_authenticate(token_name="EARTHENGINE_TOKEN")

    #### User input section - START
    # columns for input - map
    c1, c2 = st.columns([3, 1])

    with st.container():
        with c2:
        ## Cloud coverage input
            st.info("Cloud Coverage 🌥️")
            cloud_pixel_percentage = st.slider(label="cloud pixel rate", min_value=5, max_value=100, step=5, value=75 , label_visibility="collapsed")

        ## File upload
            # User input GeoJSON file
            st.info("Upload Area Of Interest file:")
            upload_files = st.file_uploader("Crete a GeoJSON file at: [geojson.io](https://geojson.io/)", accept_multiple_files=True)
            # calling upload files function
            geometry_aoi = upload_files_proc(upload_files)


    with st.container():
        ## Time range input
        with c1:
            col1, col2 = st.columns(2)
            col1.warning("Pre-Fire NBR Date 📅")
            initial_date = col1.date_input("initial", datetime(2023, 7, 12), label_visibility="collapsed")

            col2.success("Post-Fire NBR Date 📅")
            updated_date = col2.date_input("updated", datetime(2023, 7, 27), label_visibility="collapsed")

            time_range = 7

            # Process initial date
            str_initial_start_date, str_initial_end_date = date_input_proc(initial_date, time_range)

            # Process updated date
            str_updated_start_date, str_updated_end_date = date_input_proc(updated_date, time_range)
    
    #### User input section - END

            #### Map section - START
            global last_uploaded_centroid

            # Create the initial map
            if last_uploaded_centroid is not None:
                latitude = last_uploaded_centroid[1]
                longitude = last_uploaded_centroid[0]
                m = folium.Map(location=[latitude, longitude], tiles=None, zoom_start=11, control_scale=True)
            else:
                # Default location if no file is uploaded
                m = folium.Map(location=[36.60, 16.00], tiles=None, zoom_start=5, control_scale=True)

            ## Primary basemap
            # OSM
            b0 = folium.TileLayer('Open Street Map', name="Open Street Map")
            b0.add_to(m)

            #### Satellite imagery Processing Section - START

            ## Defining and clipping image collections for both dates:
            # Pre-fire
            pre_fire_collection = satCollection(cloud_pixel_percentage, str_initial_start_date, str_initial_end_date, geometry_aoi)
            # Post-fire
            post_fire_collection = satCollection(cloud_pixel_percentage, str_updated_start_date, str_updated_end_date, geometry_aoi)

            # setting a sat_imagery variable that could be used for various processes later on (tci, NBR... etc)
            pre_fire = pre_fire_collection.median()
            post_fire = post_fire_collection.median()

            ####################  Remote Sensing Index #################### 

            # Satellite image
            pre_fire_satImg = pre_fire
            post_fire_satImg = post_fire

            # Sat image visual parameters
            satImg_params = {
            'bands': ['B12',  'B11',  'B4'],
            'min': 0,
            'max': 1,
            'gamma': 1.1
            }

            # NDWI (Normalized Difference Water Index)
            def get_NDWI(image):
                return image.normalizedDifference(['B3', 'B11'])

            pre_fire_ndwi = get_NDWI(pre_fire)
            post_fire_ndwi = get_NDWI(post_fire)

            ndwi_params = {
            'min': -1,
            'max': 0,
            'palette': ["caf0f8", "00b4d8", "023e8a"]
            }

            # NBR (Normalized Burn Ratio)
            def get_NBR(image):
                return image.normalizedDifference(['B8', 'B12'])

            # claculating NBR for pre/post fire
            pre_fire_NBR = get_NBR(pre_fire_satImg)
            post_fire_NBR = get_NBR(post_fire_satImg)

            # Delta NBR (dNBR)
            dNBR = pre_fire_NBR.subtract(post_fire_NBR)

            dNBR_params = {
            'min': -0.5,
            'max': 1.3,
            'palette': ['#1c742c', '#2aae29', '#a1d574', '#f8ebb0', '#f7a769', '#e86c4e', '#902cd6']
            }

            img_classifier = dNBR

            dNBR_classified = ee.Image(img_classifier) \
                .where(img_classifier.gte(-0.5).And(img_classifier.lt(-0.251)), 1) \
                .where(img_classifier.gte(-0.250).And(img_classifier.lt(-0.101)), 2) \
                .where(img_classifier.gte(-0.100).And(img_classifier.lt(0.99)), 3) \
                .where(img_classifier.gte(0.100).And(img_classifier.lt(0.269)), 4) \
                .where(img_classifier.gte(0.270).And(img_classifier.lt(0.439)), 5) \
                .where(img_classifier.gte(0.440).And(img_classifier.lt(0.659)), 6) \
                .where(img_classifier.gte(0.660).And(img_classifier.lte(1.300)), 7) \

            # Classified dNBR visual parameters
            dNBR_classified_params = {
            'min': 1,
            'max': 7,
            'palette': ['#1c742c', '#2aae29', '#a1d574', '#f8ebb0', '#f7a769', '#e86c4e', '#902cd6']
            }

            ## Image masking
            # making the NDWI show only water part on NDWI layer
            masked_pre_fire_ndwi = pre_fire_ndwi.updateMask(pre_fire_ndwi.gt(-0.12))
            # post_fire_ndwi = post_fire_ndwi.updateMask(post_fire_ndwi.gt(-0.12))

            # The following masks are not depandant/tied to the masked_pre_fire_ndwi variable/layer

            # Creating a binary mask based on original NDWI: water = black = 0 | land = white = 1
            binaryMask = pre_fire_ndwi.lt(-0.1)

            # Creating a water mask based on NDWI binarmy mask using the land area (1)
            waterMask = binaryMask.selfMask()

            ## Clipping raster images to the water mask

            # masked_dNBR = dNBR.updateMask(waterMask)
            masked_dNBR_classified = dNBR_classified.updateMask(waterMask)

            #### Satellite imagery Processing Section - END

            ### Layers section - START
            # Check if the initial and updated dates are the same
            if initial_date == updated_date:
                m.add_ee_layer(post_fire_satImg, satImg_params, 'Satellite Imagery')
            else:
                m.add_ee_layer(pre_fire_satImg, satImg_params, f'Pre-Fire Satellite Imagery: {initial_date}')
                m.add_ee_layer(post_fire_satImg, satImg_params, f'Post-Fire Satellite Imagery: {updated_date}')

                # m.add_ee_layer(dNBR_classified, dNBR_classified_params, 'dNBR Classes')

                m.add_ee_layer(masked_pre_fire_ndwi, ndwi_params, f'NDWI: {initial_date}')

                # m.add_ee_layer(updateMask, dNBR_params, 'NBR "_masked')
                # m.add_ee_layer(binaryMask, {}, 'binaryMask')
                # m.add_ee_layer(waterMask, {}, 'SelfMak')
                m.add_ee_layer(masked_dNBR_classified, dNBR_classified_params, 'Reclassified dNBR')

            #### Layers section - END


            #### Map result display - START
            # Folium Map Layer Control: we can see and interact with map layers
            folium.LayerControl(collapsed=True).add_to(m)
            # Display the map
            folium_static(m)

            #### Map result display - END

    ##### Custom Styling
    st.markdown(
    """
    <style>
        /*Map iframe*/
        iframe {
            width: 100%;
        }
        .css-1o9kxky.e1f1d6gn0 {
            border: 2px solid #ffffff4d;
            border-radius: 4px;
            padding: 1rem;
        }
    </style>
    """, unsafe_allow_html=True)

# Run the app
if __name__ == "__main__":
    main()

