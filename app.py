"""
Original Project Author: IndigoWizard, Sep 24, 2022.
Project Name: Wildfire Burn Severity Analysis
License: GPL-3.0 (See LICENSE file for details)
"""

import streamlit as st
import ee
from ee import oauth
from google.oauth2 import service_account
import folium
from streamlit_folium import folium_static
from streamlit_elements import elements, mui
from streamlit_elements import nivo
from datetime import datetime, timedelta
import json
import pandas as pd
import calendar
import altair as alt
import fiona
import tempfile

st.set_page_config(
    page_title="Wildfire Burn Severity Analysis",
    page_icon="https://cdn-icons-png.flaticon.com/512/7204/7204183.png",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
    'Get help': "https://github.com/IndigoWizard/wildfire-burn-severity",
    'Report a bug': "https://github.com/IndigoWizard/wildfire-burn-severity/issues",
    'About': "This app was developped by [IndigoWizard](https://github.com/IndigoWizard/wildfire-burn-severity) (original author) for the purpose of environmental monitoring and geospatial analysis. Give proper credit when forking/using the open source code/piece of code."
    }
)

### CSS STYLING 
st.markdown(
"""
<style>
    /* Header*/
    /* Dark theme version */
    .st-emotion-cache-h4xjwg, .st-emotion-cache-12fmjuu {
        height: 1rem;
        background: none;
    }
    /*Header banner*/
    .st-emotion-cache-ropwps.egexzqm2 h1#wildfire-burn-severity-analysis {
        font-size: 1.75rem;
    }

    /*Main: Smooth scrolling*/
    .stMain.st-emotion-cache-bm2z3a.eht7o1d1 {
        scroll-behavior: smooth;
    }
    
    /* main app body with less padding*/
    .st-emotion-cache-t1wise.eht7o1d4 {
        padding: 0.2rem 2rem;
    }

    /* main app body with less padding in different screen size*/
    @media (min-width: calc(736px + 8rem)) {
        .st-emotion-cache-t1wise {
            padding: 0.2rem 2rem;
        }
    }

    /* ******* Sidebar ******* */
    /* Main container */
    /*Dark theme - Light theme class names*/
    .stSidebar.st-emotion-cache-1wqrzgl.e1c29vlm0, .stSidebar.st-emotion-cache-vmpjyt.e1c29vlm0 {
        min-width: 280px;
        max-width: fit-content;
    }

    /*Light theme sidbar background color*/
    .stSidebar.st-emotion-cache-vmpjyt, .stSidebar.st-emotion-cache-wgfafi.e1c29vlm0 {
        background-color: rgb(38, 39, 48);
        color: #fafafa;
    }
    /*sidebar light theme mobile view*/

    @media (max-width: 576px) {
        .stSidebar.st-emotion-cache-g8bi16.e1c29vlm0 {
            background-color: rgb(38, 39, 48);
            color: #fafafa;
        }
        .stVerticalBlock.st-emotion-cache-10e86g4.e6rk8up3, .stVerticalBlock.st-emotion-cache-1vn87qs.e6rk8up3 {
            gap: 1.6rem;
        }
    }


    /*Sidebar header*/
    .st-emotion-cache-kgpedg {
        padding: 0;
    }
    .st-emotion-cache-1mi2ry5.eczjsme6 {
        height: 0;
    }

    /* Logo */
    .st-emotion-cache-1kyxreq.e115fcil2 {
        justify-content: center;
    }

    /* Sidebar : inside container */
    .css-ge7e53 {
        width: fit-content;
    }

    /*Sidebar : image*/
    .st-emotion-cache-vew1uq.e6rk8up1 {
        display: flex;
        justify-content: center;
    }

    /*Sidebar : Navigation list*/
    div.element-container:nth-child(4) > div:nth-child(1) > div:nth-child(1) > ul:nth-child(1) {
        margin: 0;
        padding: 0;
        list-style: none;
    }
    div.element-container:nth-child(4) > div:nth-child(1) > div:nth-child(1) > ul:nth-child(1) > li {
        padding: 0;
        margin: 0;
        padding: 0;
        font-weight: 600;
    }
    div.element-container:nth-child(4) > div:nth-child(1) > div:nth-child(1) > ul:nth-child(1) > li > a {
        text-decoration: none;
        transition: 0.2s ease-in-out;
        padding-inline: 10px;
    }
    
    div.element-container:nth-child(4) > div:nth-child(1) > div:nth-child(1) > ul:nth-child(1) > li > a:hover {
        color: rgb(46, 206, 255);
        transition: 0.2s ease-in-out;
        background: #131720;
        border-radius: 4px;
    }
    
    /* Sidebar: socials*/
    div.css-rklnmr:nth-child(6) > div:nth-child(1) > div:nth-child(1) > p {
        display: flex;
        flex-direction: row;
        gap: 1rem;
    }

    /*Socials flex properties: dark & light theme*/
    .st-emotion-cache-1espb9k p, .st-emotion-cache-1mw54nq p {
        display: flex;
        flex-direction: row;
        justify-content: start;
        gap: 0.8rem;
        padding-inline: 10px;
    }
    
    /* Linkedin logo*/
    .st-emotion-cache-1espb9k.egexzqm0 p a img, .st-emotion-cache-1mw54nq.egexzqm0 p a img {
        width: 32px;
    }

    /*GitHub logo:  Dark Theme - Light Theme*/
    .st-emotion-cache-14j6x93:nth-child(6) > div:nth-child(1) > div:nth-child(1) > p:nth-child(1) > a:nth-child(2) > img:nth-child(1) {
        background-color: #26273040;
        border-radius: 50%;
    }
    /*GitHub logo:  Dark Theme - Light Theme - Mobile version*/
    div.st-emotion-cache-vew1uq:nth-child(6) > div:nth-child(1) > div:nth-child(1) > p:nth-child(1) > a:nth-child(2) > img:nth-child(1) {
        background-color: #26273040;
        border-radius: 50%;
    }

    /*Main body Title*/
    .st-emotion-cache-ropwps.egexzqm2 h1#wildfire-burn-severity-analysis, .st-emotion-cache-18netey.egexzqm2 h1#wildfire-burn-severity-analysis {
        font-size: 2rem;
        padding: 1.8rem 0 0.5rem;
    }
    
    /* ******* Upload Section ******* */
    /* ***** Upload info box */
    /* Light theme version */
    .st-emotion-cache-1gulkj5.e1blfcsg0 {
        background-color: rgb(215, 210, 225);
        color: rgb(40, 40, 55);
        display: flex;
        flex-direction: column;
        align-items: inherit;
        font-size: 14px;
    }

    /* ***** Upload SVG: Mobile view */
    @media (max-width: 576px) {
        /* Dark theme version*/
        .st-emotion-cache-wn8ljn.e1b2p2ww13 {
            display: unset;
        }

        /* Light theme version*/
        .st-emotion-cache-nwtri.e1b2p2ww13 {
            display: unset;
        }
    }
    
    /* ***** Upload button: dark theme*/
    .st-emotion-cache-1erivf3.e1blfcsg0 {
        display: flex;
        flex-direction: column;
        align-items: inherit;
        font-size: 14px;
    }
    .st-emotion-cache-19rxjzo.ef3psqc12 {
        display: flex;
        flex-direction: row;
        margin-inline: 0;
    }
    
    /* ***** Upload button: light theme*/
    .st-emotion-cache-1gulkj5.e1b2p2ww15 {
        display: flex;
        flex-direction: column;
        align-items: inherit;
        font-size: 14px;
    }

    .st-emotion-cache-7ym5gk.ef3psqc12 {
        display: flex;
        flex-direction: row;
        margin-inline: 0;
        background: rgba(0, 3, 172, 0.15);
    }

    /* ******* Form Submit ******* */
    /* ***** Generate Map */
    /* Dark theme version */
    .st-emotion-cache-19rxjzo.ef3psqc7 {
        width: 100%;
    }
    /* Light Theme Version */
    .st-emotion-cache-7ym5gk.ef3psqc7 {
        width: 100%;
        background: rgba(0, 3, 172, 0.25);
    }

    /* Buttons */
    /* Light theme verison; hober effect */
    .st-emotion-cache-7ym5gk:hover {
        border-color: rgb(255, 0, 110);
        color: rgb(255, 0, 110);
    }

    /* ******* Legend style ******* */

    .ndwilegend {
        transition: 0.2s ease-in-out;
        border-radius: 5px;
        box-shadow: 0 0 5px rgba(0, 0, 0, 0.2);
        background: rgba(0, 0, 0, 0.05);
    }
    .ndwilegend:hover {
        transition: 0.3s ease-in-out;
        box-shadow: 0 0 5px rgba(0, 0, 0, 0.8);
        background: rgba(0, 0, 0, 0.12);
        cursor: pointer;
    }
    .reclassifieddNBR {
        transition: 0.2s ease-in-out;
        border-radius: 5px;
        box-shadow: 0 0 5px rgba(0, 0, 0, 0.2);
        background: rgba(0, 0, 0, 0.05);
    }
    .reclassifieddNBR:hover {
        transition: 0.3s ease-in-out;
        box-shadow: 0 0 5px rgba(0, 0, 0, 0.8);
        background: rgba(0, 0, 0, 0.12);
        cursor: pointer;
    }
    

</style>
""", unsafe_allow_html=True)

# Initializing the Earth Engine library
# GEE Servuce Account Auth+init for cloud deployment
@st.cache_data(persist=True)
def ee_authenticate():
    # Check for json key in Streamlit Secrets
    if "json_key" in st.secrets:
        json_creds = st.secrets["json_key"]
        service_account_info = json.loads(json_creds)
        # Catching eventual email related error
        if "client_email" not in service_account_info:
            raise ValueError("Service account email address missing in json key")
        creds = service_account.Credentials.from_service_account_info(service_account_info, scopes=oauth.SCOPES)
        # Initializing gee for each run of the app
        ee.Initialize(creds)
    else:
        # Fallback to normal init method if no json key/st secrets available. (local machine)
        ee.Initialize()

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

def parse_gpkg_coords_to_ee_geometry(file):
    # load GPKG file data to fiona collection
    with fiona.open(fp=file) as f:
        # convert coordinate data to Google earth engine geometry multipolygon
        return ee.Geometry.MultiPolygon(
            [e['geometry']['coordinates'] for e in f if e['geometry']['type'] in ('Polygon', 'MultiPolygon')]
        )

# Upload function
last_uploaded_centroid = None
def upload_files_proc(upload_files):
    # A global variable to track the latest geojson uploaded
    global last_uploaded_centroid
    # Setting up a variable that takes all polygons/geometries within the same/different geojson
    geometry_aoi_list = []

    for upload_file in upload_files:
        file_name = getattr(upload_file, 'name').lower()
        upload_file.seek(0)

        # Parse GPKG file
        if file_name.endswith('.gpkg'):
            with tempfile.NamedTemporaryFile(suffix='.gpkg') as tmp:
                tmp.write(upload_file.getbuffer())
                geometry = parse_gpkg_coords_to_ee_geometry(file=tmp.name)
            geometry_aoi_list.append(geometry)

            # Update the last uploaded centroid
            last_uploaded_centroid = geometry.centroid(maxError=1).getInfo()['coordinates']
            continue

        # Parse GeoJSON file
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

# Raster Area calculation function
def calculate_class_area(classified_image, geometry_aoi, class_value):
    class_pixel_area = classified_image.eq(class_value).multiply(ee.Image.pixelArea())
    class_area = class_pixel_area.reduceRegion(
        reducer=ee.Reducer.sum(),
        geometry=geometry_aoi,
        scale=10,
        maxPixels=1e12
    )
    area_value = class_area.getInfo()
    return area_value.get(list(area_value.keys())[0], 0)  # Get the value dynamically

# Geojson Area calculation function
def geojson_area(aoi):
    # geojson area: (geometry area)
    aoi_area_sqm = aoi.area()
    # Convert the area to square kilometers
    aoi_area_info = aoi_area_sqm.getInfo()/1e6
    aoi_area_rounded = round(aoi_area_info, 4)
    return aoi_area_rounded

# Main function to run the Streamlit app
def main():
    # initialize gee 
    ee_authenticate()

    # sidebar
    with st.sidebar:
        st.logo(image="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAAC0lEQVQIW2NgAAIAAAUAAR4f7BQAAAAASUVORK5CYII=", link=None, icon_image="https://cdn-icons-png.flaticon.com/512/7204/7204183.png")
        st.image("https://cdn-icons-png.flaticon.com/512/7204/7204183.png", width=90)
        st.markdown("#### Wildfire Burn Severity Analysis")
        st.subheader("Navigation:")
        st.markdown(
            """
                - [Wildfire Map](#wildfire-burn-severity-analysis)
                - [Map Legend](#map-legend)
                - [Analysis Report](#analysis-report)
                - [Interpreting the Results](#interpreting-the-results)
                - [Environmental Index](#usage-the-environmental-index-nbr-dnbr)
                - [Data](#data)
                - [Credit](#credit)
            """)
    
        st.subheader("Contact:")
        st.markdown("[![LinkedIn](https://cdn-icons-png.flaticon.com/512/174/174857.png)](https://linkedin.com/in/ahmed-islem-mokhtari) [![GitHub](https://github.githubassets.com/favicons/favicon-dark.png)](https://github.com/IndigoWizard) [![Medium](https://miro.medium.com/1*m-R_BkNf1Qjr1YbyOIJY2w.png)](https://medium.com/@Indigo.Wizard/mt-chenoua-forest-fires-analysis-with-remote-sensing-614681f468e9)")

        st.caption("ʕ •ᴥ•ʔ Star⭐the [project on GitHub](https://github.com/IndigoWizard/wildfire-burn-severity/)!")

    with st.container():
        st.title("Wildfire Burn Severity Analysis")
        st.markdown("**Evaluate Wildfire Burn Severity through NBR Analysis: Assess the Impact of Wildfires Through Delta NBR Index Values Using Sentinel-2 Satellite Images!**")

    #### User input section - START
    # columns for input - map
    with st.form("input_form"):
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

            ## Accessibility: Color palette input
                st.info("Custom Color Palettes")
                accessibility = st.selectbox("Accessibility: Colorblind-friendly Palettes", ["Normal", "Deuteranopia", "Protanopia", "Tritanopia", "Achromatopsia"])

                # Define default color palettes: used in map layers & map legend
                default_dnbr_palette = ["#ffffe5", "#f7fcb9", "#78c679", "#41ab5d", "#238443", "#005a32"]
                default_dNBR_classified_palette = ['#1c742c', '#2aae29', '#a1d574', '#f8ebb0', '#f7a769', '#e86c4e', '#902cd6']
                default_ndwi_palette = ["#caf0f8", "#00b4d8", "#023e8a"]

                # a copy of default colors that can be reaffected
                ndwi_palette = default_ndwi_palette.copy() 
                dnbr_palette = default_dnbr_palette.copy() 
                dNBR_classified_palette = default_dNBR_classified_palette.copy()

                if accessibility == "Deuteranopia":
                    dnbr_palette = ["#fffaa1","#f4ef8e","#9a5d67","#573f73","#372851","#191135"]
                    dNBR_classified_palette = ["#95a600","#92ed3e","#affac5","#78ffb0","#69d6c6","#22459c","#000e69"]
                elif accessibility == "Protanopia":
                    dnbr_palette = ["#a6f697","#7def75","#2dcebb","#1597ab","#0c677e","#002c47"]
                    dNBR_classified_palette = ["#95a600","#92ed3e","#affac5","#78ffb0","#69d6c6","#22459c","#000e69"]
                elif accessibility == "Tritanopia":
                    dnbr_palette = ["#cdffd7","#a1fbb6","#6cb5c6","#3a77a5","#205080","#001752"]
                    dNBR_classified_palette = ["#ed4700","#ed8a00","#e1fabe","#99ff94","#87bede","#2e40cf","#0600bc"]
                elif accessibility == "Achromatopsia":
                    dnbr_palette = ["#407de0", "#2763da", "#394388", "#272c66", "#16194f", "#010034"]
                    dNBR_classified_palette = ["#004f3d", "#338796", "#66a4f5", "#3683ff", "#3d50ca", "#421c7f", "#290058"]

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
                latitude=36.60
                longitude=16.00
                # Default location if no file is uploaded
                m = folium.Map(location=[36.60, 16.00], tiles=None, zoom_start=5, control_scale=True)

            ## Primary basemap
            # OSM
            b0 = folium.TileLayer('OpenStreetMap', name="Open Street Map", attr="OSM")
            b0.add_to(m)
            b1 = folium.TileLayer('cartodbdark_matter', name='Dark Basemap', attr='CartoDB')
            b1.add_to(m)

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
            'palette': ndwi_palette
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
            'palette': dnbr_palette
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
            'palette': dNBR_classified_palette
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

            ### Burn scar area - vector
            # Define arbitrary thresholds on the classified dNBR image.
            dNBR_classified = dNBR_classified.gte(4)
            dNBR_classified = dNBR_classified.updateMask(dNBR_classified.neq(0))

            # Convert the zones of the thresholded burn areas to vectors.
            vectors = dNBR_classified.addBands(dNBR_classified).reduceToVectors(
                **{
                    'geometry': geometry_aoi,
                    'crs': dNBR_classified.projection(),
                    'scale': 10,
                    'geometryType': 'polygon',
                    'eightConnected': False,
                    'labelProperty': 'zone',
                    'reducer': ee.Reducer.mean(),
                    'bestEffort': True
                })
            # Burn scar based on converted rasters to vectors> Is displayed as its own layer
            burn_scar = ee.Image(0).updateMask(0).paint(vectors, '000000', 2)

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
                m.add_ee_layer(burn_scar, {'palette': '#87043b'}, 'Burn Scar')

            #### Layers section - END

            #### Map result display - START
            # Folium Map Layer Control: we can see and interact with map layers
            folium.LayerControl(collapsed=True).add_to(m)
            # Display the map
        submitted = c2.form_submit_button("Generate map")
        if submitted:
            with c1:
                folium_static(m)
        else:
            with c1:
                folium_static(m)

            #### Map result display - END

    #### Legend - START
    with st.container():
        st.subheader("Map Legend:")
        col3, col4, col5 = st.columns([1,2,1])
        with col3:            
            # Create an HTML legend for NDWI classes
            ndwi_legend_html = """
                <div class="ndwilegend">
                    <h5>NDWI</h5>
                    <div style="display: flex; flex-direction: row; align-items: flex-start; gap: 1rem; width: 100%;">
                        <div style="width: 30px; height: 200px; background: linear-gradient({0},{1},{2}); border-radius: 2px;"></div>
                        <div style="display: flex; flex-direction: column; justify-content: space-between; height: 200px;">
                            <span>-1</span>
                            <span style="align-self: flex-end;">1</span>
                        </div>
                    </div>
                </div>
            """.format(*ndwi_palette)

            # Display the NDWI legend using st.markdown
            st.markdown(ndwi_legend_html, unsafe_allow_html=True)

        with col4:            
            # Create an HTML legend for dNBR classes
            reclassified_dNBR_legend_html = """
                <div class="reclassifieddNBR">
                    <h5>Reclassified Delta NBR</h5>
                    <ul style="list-style-type: none; padding: 0;">
                        <li style="margin: 0.2em 0px; padding: 0;"><span style="background-color: {0}; opacity: 0.75; display: inline-block; width: 15px; height: 15px; border-radius: 50%; margin-right: 5px;"></span> Enhanced Regrowth (High).</li>
                        <li style="margin: 0.2em 0px; padding: 0;"><span style="background-color: {1}; opacity: 0.75; display: inline-block; width: 15px; height: 15px; border-radius: 50%; margin-right: 5px;"></span> Enhanced Regrowth (Low).</li>
                        <li style="margin: 0.2em 0px; padding: 0;"><span style="background-color: {2}; opacity: 0.75; display: inline-block; width: 15px; height: 15px; border-radius: 50%; margin-right: 5px;"></span> Unburned.</li>
                        <li style="margin: 0.2em 0px; padding: 0;"><span style="background-color: {3}; opacity: 0.75; display: inline-block; width: 15px; height: 15px; border-radius: 50%; margin-right: 5px;"></span> Low Severity Burns.</li>
                        <li style="margin: 0.2em 0px; padding: 0;"><span style="background-color: {4}; opacity: 0.75; display: inline-block; width: 15px; height: 15px; border-radius: 50%; margin-right: 5px;"></span> Moderate-Low Severity Burns.</li>
                        <li style="margin: 0.2em 0px; padding: 0;"><span style="background-color: {5}; opacity: 0.75; display: inline-block; width: 15px; height: 15px; border-radius: 50%; margin-right: 5px;"></span> Moderate-High Severity Burns.</li>
                        <li style="margin: 0.2em 0px; padding: 0;"><span style="background-color: {6}; opacity: 0.75; display: inline-block; width: 15px; height: 15px; border-radius: 50%; margin-right: 5px;"></span> High Severity Burns.</li>
                    </ul>
                </div>
            """.format(*dNBR_classified_palette)

            # Display the Reclassified dNBR legend using st.markdown
            st.markdown(reclassified_dNBR_legend_html, unsafe_allow_html=True)

    #### Legend - END

    #### Analysis Report - START
    st.write("#### Analysis Report")
    with st.form("report_form"):
    
        #### Area Calculation - START

        # geojson area: (geometry area)
        geometry_area = geojson_area(geometry_aoi)

        # Calculate and display the areas of each dNBR class
        dNBR_class_areas = []
        for i in range(1, 8):
            area = calculate_class_area(masked_dNBR_classified, geometry_aoi, i)
            dNBR_class_areas.append(area / 1e6)  # Convert to square kilometers
        
        class_names = [ # dNBR class names
            "Enhanced Regrowth (High)",
            "Enhanced Regrowth (Low)",
            "Unburned",
            "Low Severity Burns",
            "Moderate-Low Severity Burns",
            "Moderate-High Severity Burns",
            "High Severity Burns",
        ]

        # Report submit button
        report_form = st.form_submit_button("Generate report", type="primary")

        if report_form:
            st.write("#### Wildfire Burn Severity Analysis Report:")
            # Stats layout
            col1, col2 = st.columns([1,1])
            col3, col4 = st.columns([1.5,2])

            # setting up stats to print
            centroid_info = f"**ROI Location:** [:blue[{round(latitude, 4)}], :blue[{round(longitude, 4)}]]"
            area_of_interest = f"**Surface Area of Region of Interest: ~:blue[{geometry_area}] (Km²)**"
            initial_date_range = f"**Pre-Fire date range:** :blue-background[{str_initial_start_date}], :blue-background[{str_initial_end_date}]"
            updated_date_range = f"**Post-Fire date range:** :blue-background[{str_updated_start_date}], :blue-background[{str_updated_end_date}]"
            col1.success(centroid_info) # location
            col1.success(area_of_interest) # size of aoi
            col2.success(initial_date_range) # pre-fire date range
            col2.success(updated_date_range) # post-fire date range

            # print area of individual dNBR classes
            for i, area in enumerate(dNBR_class_areas, start=1):
                class_sq = f"**{class_names[i-1]}: ~** :green[{round(area, 4)}] **(Km²)**"
                col3.info(class_sq)

            # Display Interactive Pie Chart
            with col4:
                # Display stat visuals
                DATA_PIE = [
                    { "id": class_names[i-1], "label": class_names[i-1], "value": round(area, 4), "color": dNBR_classified_palette[i-1] }
                    for i, area in enumerate(dNBR_class_areas, start=1)
                ]

                # Render the nivo.Pie component with the defined theme
                with elements("nivo_pie_chart"):
                    with mui.Box(sx={"height": 500}):
                        nivo.Pie(
                            data=DATA_PIE,
                            margin={"top": 20, "right": 100, "bottom": 150, "left": 100},
                            innerRadius=0.5,
                            padAngle=0.7,
                            cornerRadius=3,
                            activeOuterRadiusOffset=8,
                            borderWidth=1,
                            borderColor={"from": "color", "modifiers": [["darker", 0.8]]},
                            arcLinkLabelsSkipAngle=2,
                            arcLinkLabelsTextColor={"from": "color"},
                            arcLinkLabelsColor={"from": "color"},
                            colors={"datum": 'data.color'},
                            arcLinkLabel="value",
                            arcLinkLabelsThickness=2,
                            arcLabelsSkipAngle=10,
                            arcLinkLabelsDiagonalLength=10,
                            arcLinkLabelsStraightLength=10,
                            arcLinkLabelsTextOffset=4,
                            arcLabelsTextColor={"from": "color", "modifiers": [["darker", 4]]},
                            defs = [
                                {
                                    "id": "EnhancedRegrowthHigh",
                                    "type": "patternLines",
                                    # "color": "#1c742cbf",
                                    "color": f"{dNBR_classified_palette[0]}",
                                    "background": f"{dNBR_classified_palette[0]}bf",
                                    "rotation": 105,
                                    "lineWidth": 3,
                                    "spacing": 10,
                                },
                                {
                                    "id": "EnhancedRegrowthLow",
                                    "type": "patternLines",
                                    # "color": "#2aae29bf",
                                    "color": f"{dNBR_classified_palette[1]}",
                                    "background": f"{dNBR_classified_palette[1]}bf",
                                    "rotation": -15,
                                    "lineWidth": 4,
                                    "spacing": 9,
                                },
                                {
                                    "id": "Unburned",
                                    "type": "patternSquares",
                                    # "color": "#a1d574bf",
                                    "color": f"{dNBR_classified_palette[2]}",
                                    "background": f"{dNBR_classified_palette[2]}bf",
                                    "size": 4,
                                    "padding": 1.5,
                                    "stagger": True,
                                },
                                {
                                    "id": "LowSeverityBurns",
                                    "type": "patternSquares",
                                    # "color": "#f8ebb0bf",
                                    "color": f"{dNBR_classified_palette[3]}",
                                    "background": f"{dNBR_classified_palette[3]}bf",
                                    "size": 5,
                                    "padding": 3,
                                    "stagger": True,
                                },
                                {
                                    "id": "ModerateLowSeverityBurns",
                                    "type": "patternDots",
                                    # "color": "#f7a769bf",
                                    "color": f"{dNBR_classified_palette[4]}",
                                    "background": f"{dNBR_classified_palette[4]}bf",
                                    "size": 4.5,
                                    "padding": 4.5,
                                    "stagger": True,
                                },
                                {
                                    "id": "ModerateHighSeverityBurns",
                                    "type": "patternDots",
                                    # "color": "#e86c4ebf",
                                    "color": f"{dNBR_classified_palette[5]}",
                                    "background": f"{dNBR_classified_palette[5]}bf",
                                    "size": 4,
                                    "padding": 3,
                                    "stagger": True,
                                },
                                {
                                    "id": "HighSeverityBurns",
                                    "type": "patternDots",
                                    # "color": "#902cd6bf",
                                    "color": f"{dNBR_classified_palette[6]}",
                                    "background": f"{dNBR_classified_palette[6]}bf",
                                    "size": 3,
                                    "padding": 2,
                                    "stagger": True,
                                },
                            ],
                            fill=[
                                {"match": {"id": "Enhanced Regrowth (High)"}, "id": "EnhancedRegrowthHigh"},
                                {"match": {"id": "Enhanced Regrowth (Low)"}, "id": "EnhancedRegrowthLow"},
                                {"match": {"id": "Unburned"}, "id": "Unburned"},
                                {"match": {"id": "Low Severity Burns"}, "id": "LowSeverityBurns"},
                                {"match": {"id": "Moderate-Low Severity Burns"}, "id": "ModerateLowSeverityBurns"},
                                {"match": {"id": "Moderate-High Severity Burns"}, "id": "ModerateHighSeverityBurns"},
                                {"match": {"id": "High Severity Burns"}, "id": "HighSeverityBurns"},
                            ],
                            theme={
                                "tooltip": {
                                    "container": { # container within the tooltip
                                        "background": "white",  # background of the tooltip inside container
                                        "fontSize": 14,
                                        "font-family": "sans-serif",
                                        "padding": 2,
                                        "border-radius": 4
                                    },
                                    "basic": { # the box within the container within the tooltip
                                        "whiteSpace": "pre",
                                        "display": "flex",
                                        "flex-direction": "row",
                                        "alignItems": "center",
                                        "justify-content": "space-around",
                                        "background": "#0e1117",
                                        "margin": 1,
                                        "padding": 5,
                                        "width": "fit-content",
                                        "height": "fit-content",
                                        "color": "white",
                                    },
                                }
                            }
                        )
        #### Area Calculation - END

        #### Precipitation Claculation - START
           
            with st.container():

                # Define CHIRPS image collection function
                def chirpsCollection(initialDate, updatedDate, aoi):
                    chirps = (
                        ee.ImageCollection("UCSB-CHG/CHIRPS/DAILY")
                        .filterDate(initialDate, updatedDate)
                        .filterBounds(aoi)
                        .select("precipitation")
                    )
                    return chirps

                # Generate precipitation data for full months
                def full_month_precipitation(initialDate, endDate, aoi):
                    # Convert input dates to datetime objects
                    initial_date = datetime.strptime(initialDate, "%Y-%m-%d")
                    end_date = datetime.strptime(endDate, "%Y-%m-%d")

                    # Determine start and end of the full months
                    start_of_month = initial_date.replace(day=1)
                    _, end_of_month_day = calendar.monthrange(end_date.year, end_date.month)
                    end_of_month = end_date.replace(day=end_of_month_day)

                    # Ensure non-duplicate timeline
                    if initial_date.month == end_date.month and initial_date.year == end_date.year:
                        # If same month/year, use full month only once
                        start_of_month = initial_date.replace(day=1)
                        end_of_month = end_date.replace(day=end_of_month_day)

                    # Generate precipitation data
                    raincol = chirpsCollection(start_of_month.strftime("%Y-%m-%d"), end_of_month.strftime("%Y-%m-%d"), aoi)
                    
                    daily_precipitation = raincol.map(
                        lambda img: ee.Feature(
                            aoi,
                            {
                                "date": img.date().format("YYYY-MM-dd"),
                                "precipitation": img.reduceRegion(
                                    reducer=ee.Reducer.mean(),
                                    geometry=aoi,
                                    scale=30
                                ).get("precipitation"),
                            }
                        )
                    )

                    # Convert to Python list
                    daily_list = daily_precipitation.getInfo()["features"]
                    
                    # Extracting dates & precipitation values
                    dates = [entry["properties"]["date"] for entry in daily_list]
                    values = [entry["properties"]["precipitation"] for entry in daily_list]

                    # Create a DataFrame
                    rdf = pd.DataFrame({"Date": dates, "Precipitation": [round(value, 2) if value is not None else None for value in values]})
                    return rdf

                # Data frame / viz layout
                col5, col6 = st.columns([1,2])
                
                # Fetch precipitation data
                rdf = full_month_precipitation(str_initial_start_date, str_updated_end_date, geometry_aoi)

                # Display the DataFrame in Streamlit
                col5.subheader("Data table:")
                col5.dataframe(
                    rdf,
                    column_config={
                        "Date": "Date",
                        "Precipitation": st.column_config.ProgressColumn(
                            "Rainfall (mm)", format=" %f mm", min_value=0, max_value=100, width="medium", help='Precipitation (mm)'
                        ),
                    },
                    hide_index=True, width=400, height=420
                )

                # Chart visualization
                def precipitation_chart(rdf):
                    # Converting Date column to compatible Altair datetime
                    rdf["Date"] = pd.to_datetime(rdf["Date"])

                    # Altair graph: bar chart with a line chart
                    viz_chart = alt.Chart(rdf).mark_bar(color="#88c0d0").encode(
                        x=alt.X("Date:T", axis=alt.Axis(title="Time (Days)", ticks=True, tickMinStep=1)),
                        y=alt.Y("Precipitation:Q", axis=alt.Axis(title=None, ticks=True, tickMinStep=1)),
                        tooltip=["Date:T", "Precipitation:Q"]
                    ) + alt.Chart(rdf).mark_line(color="#004dc6", point=True, interpolate="monotone").encode(
                        x="Date:T",
                        y="Precipitation:Q"
                    ).properties(
                        title="Precipitation (mm)",
                        height=500
                    )
                    return viz_chart

                # Generate and display Altair chart
                viz_chart = precipitation_chart(rdf)
                col6.subheader("Daily Precipitation")
                col6.altair_chart(viz_chart, use_container_width=True)

        #### Precipitation Claculation - END


        #### Temperature calculation - START

                # Define the Temperature Image Collection function
                def temperatureCollection(initialDate, updatedDate, aoi):
                    temp_collection = (
                        ee.ImageCollection("ECMWF/ERA5_LAND/HOURLY")  # GCOM-C/SGLI dataset
                        .filterDate(initialDate, updatedDate)
                        .filterBounds(aoi)
                        .select("temperature_2m")  # Correct band: Average Land Surface Temperature
                    )
                    return temp_collection

                # Generate temperature data for full months
                def full_month_temperature(initialDate, endDate, aoi):
                    # Convert input dates to datetime objects
                    initial_date = datetime.strptime(initialDate, "%Y-%m-%d")
                    end_date = datetime.strptime(endDate, "%Y-%m-%d")

                    # Determine start and end of the full months
                    start_of_month = initial_date.replace(day=1)
                    _, end_of_month_day = calendar.monthrange(end_date.year, end_date.month)
                    end_of_month = end_date.replace(day=end_of_month_day)

                    # Avoiding duplicate timespan
                    if initial_date.month == end_date.month and initial_date.year == end_date.year:
                        start_of_month = initial_date.replace(day=1)
                        end_of_month = end_date.replace(day=end_of_month_day)

                    # Generate temperature data
                    tempcol = temperatureCollection(start_of_month.strftime("%Y-%m-%d"), end_of_month.strftime("%Y-%m-%d"), aoi)

                    daily_temperature = tempcol.map(
                        lambda img: ee.Feature(
                            aoi,
                            {
                                "date": img.date().format("YYYY-MM-dd"),
                                "temperature": img.reduceRegion(
                                    reducer=ee.Reducer.mean(),
                                    geometry=aoi,
                                    scale=11132
                                ).get("temperature_2m"),
                            }
                        )
                    )

                    # Convert to Python list
                    daily_temp_list = daily_temperature.getInfo()["features"]

                    # Extracting dates & temperature values (scaled to °C if necessary)
                    dates_t = [entry["properties"]["date"] for entry in daily_temp_list]
                    values_t = [entry["properties"]["temperature"] for entry in daily_temp_list]
                    scaled_values = [round(value - 273.15, 2) if value is not None else None for value in values_t]  # Scale values from dataset

                    # Create a DataFrame
                    temp_df = pd.DataFrame({"Date": dates_t, "Temperature": scaled_values})

                    # Remove duplicates by averaging values for each date
                    temp_df = temp_df.groupby("Date", as_index=False).mean()
                    return temp_df


                # Data frame / visualization layout
                col5, col6 = st.columns([1, 2])

                # Fetch temperature data
                temp_df = full_month_temperature(str_initial_start_date, str_updated_end_date, geometry_aoi)

                # Display the DataFrame in Streamlit
                col5.subheader("Temperature Data Table:")
                col5.dataframe(
                    temp_df,
                    column_config={
                        "Date": "Date",
                        "Temperature": st.column_config.NumberColumn(
                            "Temperature (°C)", format="%.2f °C", min_value=-50, max_value=50, width="medium", help="Temperature in Celsius"
                        ),
                    },
                    hide_index=True, width=400, height=420
                )

                # Chart visualization
                def temperature_chart(temp_df):
                    # Converting Date column to compatible Altair datetime
                    temp_df["Date"] = pd.to_datetime(temp_df["Date"])

                    # Altair graph: bar chart with a line chart
                    viz_chart = alt.Chart(temp_df).mark_bar(color="#e65780").encode(
                        x=alt.X("Date:T", axis=alt.Axis(title="Time (Days)", ticks=True, tickMinStep=1)),
                        y=alt.Y("Temperature:Q", axis=alt.Axis(title=None, ticks=True, tickMinStep=1)),
                        tooltip=["Date:T", "Temperature:Q"]
                    ) + alt.Chart(temp_df).mark_line(color="#e63946", point=True, interpolate="monotone").encode(
                        x="Date:T",
                        y="Temperature:Q"
                    ).properties(
                        title="Daily Temperature (°C)",
                        height=500
                    )
                    return viz_chart

                # Generate and display Altair chart
                temp_viz_chart = temperature_chart(temp_df)
                col6.subheader("Daily Temperature")
                col6.altair_chart(temp_viz_chart, use_container_width=True)
            
        #### Temperature calculation - END
    
    #### Analysis Report - END



    ##### Miscs Infos - START
    with st.container():
        st.divider()
        # Results interpretation
        st.write("#### Interpreting the Results")

        st.write("This app is designed to provide an accessible tool for both technical and non-technical users to explore and interpret burn severity and land surface changes.")
        st.write("The burn severity map is a valuable tool, its interpretation requires consideration of various factors. When exploring the dNBR map, keep in mind:")

        st.write("- Clouds, atmospheric conditions, and water bodies can affect the map's appearance and so the surface area.")
        st.write("- Satellite sensors have limitations in distinguishing surface types, leading to color variations.")
        st.write("- NBR/dNBR values may subtley vary with type of vegetation and land cover changes.")
        st.write("- The map provides visual insights rather than precise representations.")

        st.write("Understanding these factors will help you interpret the results more effectively. This application aims to provide you with an informative visual aid for vegetation burn severity analysis.")

        ## NBR/Environmental Index
        st.write("#### Usage the Environmental Index: NBR / dNBR")
        st.write("The [Normalized Burn Ratio (NBR)](https://www.earthdatascience.org/courses/earth-analytics/multispectral-remote-sensing-modis/normalized-burn-index-dNBR/) is used to emphasize charred areas after a fire. The NBR vegetation index equation takes into account observations at both NIR and SWIR wavelengths: healthy vegetation has a high reflectance in the NIR spectrum, whereas recently burned sections of vegetation reflect strongly in the SWIR spectrum.")

        st.write("NBR is calculated using satellite imagery that captures both Near-Infrared **(NIR)** and Short-Wave Infrared **(SWIR)** wavelengths. The formula is:")
        st.latex(r'''
        \text{NBR} = \frac{\text{NIR} - \text{SWIR}}{\text{NIR} + \text{SWIR}}
        ''')

        st.write("dNBR (Difference NBR) is calculated by the difference of Pre-Fire NBR and Post-Fire-NBR values. The formula is:")
        st.latex(r'''
        \text{dNBR} = \text{NBR}_{pre-fire} - \text{NBR}_{post-fire}
        ''')


        st.write("NBR values range from **[-1** to **1]**, with higher values indicating higher severity burns. Lower values represent unburned vegetated surfaces or enhanced regrowth.")

        ## Data
        st.write("#### Data")
        st.write("This app utilizes **Sentinel-2 Level-2A atmospherically corrected Surface Reflectance images**. The [Sentinel-2 satellite constellation](https://sentinels.copernicus.eu/web/sentinel/user-guides/sentinel-2-msi/applications) consists of twin satellites (Sentinel-2A and Sentinel-2B) that capture high-resolution multispectral imagery of the Earth's surface.")

        st.write("The [Level-2A](https://sentinels.copernicus.eu/web/sentinel/user-guides/sentinel-2-msi/product-types/level-2a) products have undergone atmospheric correction, enhancing the accuracy of surface reflectance values. These images are suitable for various land cover and vegetation analyses, including NBR calculations.")

        ## Credits
        st.write("##### Credit:")
        st.caption("""The app was developped by [IndigoWizard](https://github.com/IndigoWizard) using; [Streamlit](https://streamlit.io/), [Google Earth Engine](https://github.com/google/earthengine-api) Python API and [Folium](https://github.com/python-visualization/folium). Wildfire icons created by <a href="https://www.flaticon.com/free-icons/wildfire" title="wildfire icons">Pomicon - Flaticon</a>""", unsafe_allow_html=True)

        #### Miscs Info - END
        

    ##### Custom Styling
    st.markdown(
    """
    <style>
        /*Map iframe*/
        iframe {
            width: 100%;
        }
    </style>
    """, unsafe_allow_html=True)

# Run the app
if __name__ == "__main__":
    main()

