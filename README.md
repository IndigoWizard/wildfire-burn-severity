# wildfire-burn-severity
Webapp link: [Wlidfire Burn Severity project](https://indigowizard.github.io/wildfire-burn-severity/webmap.html)

## Project description:
A GEE project that aims to generate a burn severity map to assess surface areas affected by wildfires. The project relyes on **Normalized Burn Ratio (NBR)** to highlight the affected areas and estimate burn severity levels.

### Use-case:
The wildifre that erupted in Mount Chenoua, Tipaza, Algeria on August 14th-16th 2022 is used as main use-case.
For more details on this wildfire, read the related medium article: [Mt Chenoua Forest Fires Analysis with Remote Sensing.](https://medium.com/@Indigo.Wizard/mt-chenoua-forest-fires-analysis-with-remote-sensing-614681f468e9)

### Info:
The project uses Google Earth Engine python api, combined with folium and geemap to render the map, calculate the index ratio and compute raster data results.

### Preview

![](https://gifyu.com/image/S990Z)

### User guide
End users can navigate to the web page and access the results easily: [Burn Severity Analysis](https://indigowizard.github.io/wildfire-burn-severity/webmap.html)

If you want to fork and work on the project, you need the following:

1. To use this script, you must first [sign up](https://earthengine.google.com/signup/) for a [Google Earth Engine](https://earthengine.google.com/) account.
2. Install [gcloud CLI](https://cloud.google.com/cli) for the Google Earth Engine account authentication.
3. Install the rest of project dependencies from `requirement.txt` file, just run:

`conda install --file requirements.txt`
> use python 3.9 and up.

Consider starring the project ʕ •ᴥ•ʔ ... ʕ　·ᴥ·ʔ

#### Credit
Project created using: [Google Earth Engine (GEE)](https://github.com/google/earthengine-api), [geemap](https://github.com/giswqs/geemap), [Folium](https://github.com/python-visualization/folium) - Project by [Ahmed I. Mokhtari](https://www.linkedin.com/in/ahmed-islem-mokhtari/).