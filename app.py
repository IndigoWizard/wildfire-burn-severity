import streamlit as st
import folium
from streamlit_folium import folium_static

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

# Main function to run the Streamlit app
def main():
    #### Map section - START
    m = folium.Map(location=[36.60, 2.32], tiles=None, zoom_start=5, control_scale=True)

    ## Primary basemaps
    b0 = folium.TileLayer('Open Street Map', name="Open Street Map")
    b0.add_to(m)

    # Folium Map Layer Control: we can see and interact with map layers
    folium.LayerControl(collapsed=True).add_to(m)
    # Display the map
    folium_static(m)

    #### Map result display - END

# Run the app
if __name__ == "__main__":
    main()
