import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap, BoundaryNorm
import ndvi_module  # type: ignore # Our compiled C++ module
from data_utils import load_bands

# Set page configuration
st.set_page_config(page_title="Satellite Analysis Engine", layout="wide")

st.title("Satellite Imagery Analysis Engine 🌍")
st.markdown("Advanced remote sensing analysis powered by a custom C++ Zero-copy engine.")

# File paths (Assuming B03 is your newly added green band)
GREEN_BAND_PATH = '../data/T32UQD_20260318T100741_B03_10m.jp2'
RED_BAND_PATH = '../data/T32UQD_20260318T100741_B04_10m.jp2'
NIR_BAND_PATH = '../data/T32UQD_20260318T100741_B08_10m.jp2'

# Cache the data loading to avoid reading from disk on every UI update
@st.cache_data(show_spinner=False) # no need for another loading icon
def get_cached_satellite_data(green_path, red_path, nir_path):
    return load_bands(green_path, red_path, nir_path)

# Sidebar controls for user interaction
st.sidebar.header("Control Panel")
analysis_type = st.sidebar.radio(
    "Select Analysis Mode:",
    ("NDVI (Vegetation Index)", "NDWI (Water Index)", "Pixel Classification")
)
run_calculation = st.sidebar.button("Run Analysis", type="primary")

info_placeholder = st.empty() #prevent the old info element from being stuck

# Main execution block
if run_calculation:
    # 1. Force the placeholder to clear itself instantly
    info_placeholder.empty()
    with st.spinner("Loading data and executing C++ Engine..."):
        
        # 1. Load Data (Green, Red, NIR)
        green, red, nir = get_cached_satellite_data(GREEN_BAND_PATH, RED_BAND_PATH, NIR_BAND_PATH)
        
        # 2. Setup Plot Canvas
        fig, ax = plt.subplots(figsize=(10, 8))
        
        # 3. Execute the requested analysis based on user selection
        if analysis_type == "NDVI (Vegetation Index)":
            result = ndvi_module.calculate_ndvi(red, nir)
            # RdYlGn: Red (low) to Yellow (medium) to Green (high NDVI)
            im = ax.imshow(result, cmap='RdYlGn', vmin=-1, vmax=0.9)
            fig.colorbar(im, ax=ax, label='NDVI Value')
            
            st.subheader("Vegetation Index (NDVI)")
            st.markdown("Highlights healthy vegetation in **green** and barren/water areas in **red/yellow**.")
            
        elif analysis_type == "NDWI (Water Index)":
            result = ndvi_module.calculate_ndwi(green, nir)
            # RdBu: Red (land/negative) to White (zero) to Blue (water/positive)
            im = ax.imshow(result, cmap='RdBu', vmin=-1, vmax=0.7)
            fig.colorbar(im, ax=ax, label='NDWI Value')
            
            st.subheader("Water Index (NDWI)")
            st.markdown("Highlights water bodies in **blue** and dry land in **red**.")
            
        elif analysis_type == "Pixel Classification":
            result = ndvi_module.classify_pixels(green, red, nir)
            
            # Create a custom discrete colormap for our specific classes:
            # 0 = Black (No Data), 1 = Blue (Water), 2 = Green (Vegetation), 3 = Gray (Urban/Bare)
            colors = ['black', 'blue', 'forestgreen', 'lightgray']
            cmap = ListedColormap(colors)
            
            # Define boundaries so Matplotlib knows where one class ends and another begins
            bounds = [-0.5, 0.5, 1.5, 2.5, 3.5] 
            norm = BoundaryNorm(bounds, cmap.N)
            
            im = ax.imshow(result, cmap=cmap, norm=norm)
            
            # Customize the colorbar to show class names instead of numbers
            cbar = fig.colorbar(im, ax=ax, ticks=[0, 1, 2, 3])
            cbar.ax.set_yticklabels(['No Data', 'Water', 'Vegetation', 'Urban / Bare Soil'])
            
            st.subheader("Land Cover Classification")
            st.markdown("Uses a Decision Tree in C++ to classify each pixel based on spectral signatures.")

        # 4. Final Display Settings
        ax.axis('off') # Hide coordinates axes
        st.pyplot(fig) # Render the Matplotlib figure in Streamlit
        st.success("Execution completed in Zero-copy mode!")
        
else:
    info_placeholder.info("Select an analysis mode from the sidebar and click 'Run Analysis'.")