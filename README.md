# wildfire-burn-severity

## Project description:
A GEE project that aims to generate a burn severity map to assess surface areas affected by wildfires. The project relyes on **Normalized Burn Ratio (NBR)** to highlight the affected areas and estimate burn severity levels.

### Use-case:
The wildifre that erupted in Mount Chenoua, Tipaza, Algeria on August 14th-16th 2022 is used as main use-case.
For more details on this wildfire, read the related medium article: [Mt Chenoua Forest Fires Analysis with Remote Sensing.](https://medium.com/@Indigo.Wizard/mt-chenoua-forest-fires-analysis-with-remote-sensing-614681f468e9)

### Info:
The project uses Google Earth Engine python api, combined with folium and geemap to render the map, calculate the index ratio and compute raster data results.