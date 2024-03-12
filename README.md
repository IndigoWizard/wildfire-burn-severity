# wildfire-burn-severity

Webapp link: [Wlidfire Burn Severity project](https://indigowizard.github.io/wildfire-burn-severity/)

Open for contribution! (I see you, **Hacktoberfest** enthusiasts 👀). Consider ⭐ starring the project ʕ •ᴥ•ʔ ... ʕ　·ᴥ·ʔ

**IMPORTANT NOTE:** :warning:

The Earth Engine token **expires after few days**, so after this, the layers won't show up and the webapp may seem like not working, it's not, it's just that I don't update the token from my personal google earth engine account unless you need a live demo, otherwise check the preview section.


## Project description:

A GEE project that aims to generate a burn severity map to assess surface areas affected by wildfires. The project relies on [Normalized Burn Ratio (NBR)](https://www.earthdatascience.org/courses/earth-analytics/multispectral-remote-sensing-modis/normalized-burn-index-dNBR/) to highlight the affected areas and estimate burn severity levels.

The project uses [Google Earth Engine Python API](https://anaconda.org/conda-forge/earthengine-api), combined with **Folium** and **geemap** to render the map, calculate the index ratio and compute raster data results.

### Use-case:

The wildfire that erupted in Mount Chenoua, Tipaza, Algeria on August 14th-16th 2022 is used as main use-case.
For more details on this wildfire, read the related medium article: [Mt Chenoua Forest Fires Analysis with Remote Sensing.](https://medium.com/@Indigo.Wizard/mt-chenoua-forest-fires-analysis-with-remote-sensing-614681f468e9)

### Preview

![wildfire burn severity analysis](src/wildfire-burn-severity-analysis.gif)

### User guide

End users can navigate to the web page and access the results easily: [Burn Severity Analysis](https://indigowizard.github.io/wildfire-burn-severity/)

If you want to fork and work on the project, you need the following:

1. To use this script, you must first [sign up](https://earthengine.google.com/signup/) for a [Google Earth Engine](https://earthengine.google.com/) account.
2. Install [gcloud CLI](https://cloud.google.com/cli) for the Google Earth Engine account authentication.
3. Install the rest of project dependencies from `requirement.txt` file, just run:

`conda install --file requirements.txt`
> use python 3.9 and up.

#### Change Satellite Imagery Data

You'll need two imagery data entries, one for a pre-fire and one for post-fire period, it's better to use images with less than 10% cloud coverage.<br>
Get the image ID from [Earth Engine Data Catalog](https://developers.google.com/earth-engine/datasets/catalog/COPERNICUS_S2_SR) or from [SciHub](https://scihub.copernicus.eu/) (I'm using Sentinel-2 L2A imagery for better results, you can find other datasets from other sources.)

```python
#Sentinel-2 L2A: August 12th 2022 - Pre-fire
pre_fire = ee.Image('COPERNICUS/S2_SR/20220812T103031_20220812T103132_T31SDA')

#Sentinel-2 L2A: August 20th 2022 - Post-fire
post_fire = ee.Image('COPERNICUS/S2_SR/20220820T103629_20220820T104927_T31SDA')
```

#### Change Area of Interest (AOS)

You can use [GeoJson.io](https://geojson.io/) to draw your polygon than copy/past **only the coordinates** into the code, not the full GeoJSON (Google Earth Engine at this current time don't take GeoJSON files as a geometry input, so you can't link/access/read a local GeoJSON file).

To change the area of interest (AOS) go to **[aos.py](https://github.com/IndigoWizard/wildfire-burn-severity/blob/main/aos.py)** file and put the coordinates of your area of interest, e.g;

```python
import ee
ee.Initialize()
aos = ee.Geometry.Polygon([
  # X/Y Decimal Degrees coordinates
  [2.40, 36.60],
  [],
  []...
])
```

Your Area Of Study (AOS) **must** be a polygon geometry, not a polyline or a single point as you are studying a specific surface area affected by wildfires. Avoid water surfaces.


#### Credit

Project created using: [Google Earth Engine (GEE)](https://github.com/google/earthengine-api), [geemap](https://github.com/giswqs/geemap), [Folium](https://github.com/python-visualization/folium), [Sentinel-2 L2A Satellite Imagery Dataset](https://scihub.copernicus.eu/) - Project by [Ahmed I. Mokhtari](https://www.linkedin.com/in/ahmed-islem-mokhtari/).
