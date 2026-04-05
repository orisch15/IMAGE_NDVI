import streamlit as st
import rasterio
import numpy as np
import matplotlib.pyplot as plt
import ndvi_module  # type: ignore # Our compiled C++ module
from data_utils import load_bands  # Import the core logic

# Set page configuration
st.set_page_config(page_title="Satellite Analysis", layout="wide")

st.title("Satellite Imagery Analysis Engine 🌍")
st.markdown("Vegetation index (NDVI) calculation from Sentinel-2 imagery powered by a C++ Zero-copy (Fast) engine.")

# File paths (based on your folder structure)
RED_BAND_PATH = '../data/T32UQD_20260318T100741_B04_10m.jp2'
NIR_BAND_PATH = '../data/T32UQD_20260318T100741_B08_10m.jp2'

# Cache the data loading to avoid reading from disk on every UI update
@st.cache_data
def get_cached_satellite_data(red_path, nir_path):
    return load_bands(red_path, nir_path)

# Create a sidebar for user controls
st.sidebar.header("Control Panel")
run_calculation = st.sidebar.button("Calculate NDVI", type="primary")

# Main display area
if run_calculation:
    with st.spinner("Loading JP2 files and executing C++ Engine..."):
        # Call the cached wrapper
        red, nir = get_cached_satellite_data(RED_BAND_PATH, NIR_BAND_PATH)
        
        # 2. Execute C++ calculation
        ndvi_result = ndvi_module.calculate_ndvi(red, nir)
        
        st.success("Calculation completed successfully!")
        
        # 3. Prepare the visualization using Matplotlib
        fig, ax = plt.subplots(figsize=(10, 8))
        cax = ax.imshow(ndvi_result, cmap='RdYlGn', vmin=-1, vmax=1)
        fig.colorbar(cax, label='NDVI Value')
        ax.axis('off') # Hide axes for a cleaner look
        
        # Display the plot in the Streamlit interface
        st.pyplot(fig)
else:
    st.info("👈 Click 'Calculate NDVI' in the sidebar to start the engine.")