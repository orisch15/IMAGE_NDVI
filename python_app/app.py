import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap, BoundaryNorm
import ndvi_module  # type: ignore # Our compiled C++ module
from data_utils import load_bands

# Set page configuration
st.set_page_config(page_title="Satellite Analysis Engine", layout="wide")

# ==========================================
# Main Header Layout
# ==========================================
# Using Streamlit's column layout to create a visually appealing header with a title and an image side by side
header_col1, header_col2 = st.columns([4, 1])

with header_col1:
    st.title("Satellite Imagery Analysis Engine 🌍")
    st.markdown("Advanced remote sensing analysis powered by a custom C++ Zero-copy engine.")

with header_col2:
    #width is set to 120 to keep the logo compact and aligned with the title height
    st.image("/Users/ori/Projects/Image_NDVI/src/img_src/sat_logo.png", width=120)
    
st.markdown("---")

#initialize prams
weight_veg = 0
weight_water = 0
weight_urban = 0

# File paths (Assuming B03 is your newly added green band)
GREEN_BAND_PATH = '../data/T32UQD_20260318T100741_B03_10m.jp2'
RED_BAND_PATH = '../data/T32UQD_20260318T100741_B04_10m.jp2'
NIR_BAND_PATH = '../data/T32UQD_20260318T100741_B08_10m.jp2'

# Cache the data loading to avoid reading from disk on every UI update
@st.cache_data(show_spinner=False) # no need for another loading icon
def get_cached_satellite_data(green_path, red_path, nir_path):
    return load_bands(green_path, red_path, nir_path)

# ==========================================
# Sidebar Configuration
# ==========================================

st.sidebar.title("⚙️ Control Panel")

st.sidebar.divider() # A modern visual separator

# Main Analysis Selector
analysis_type = st.sidebar.radio(
    "🔎 Select Analysis Mode:",
    ("Livability Score","NDVI (Vegetation Index)", "NDWI (Water Index)"),
    help="Choose the algorithmic model to apply to the satellite bands."
)

# Livability Preferences
if analysis_type == "Livability Score":
    st.sidebar.divider()
    
    st.sidebar.subheader("🎯 Livability Preferences")
    st.sidebar.markdown("<small>Set your ideal neighborhood profile (0-10):</small>", unsafe_allow_html=True)
    
    weight_veg = st.sidebar.slider(
        "🌲 Vegetation & Parks", 
        min_value=0, max_value=10, value=8, 
        help="Importance of green areas, forests, and parks."
    )
    weight_water = st.sidebar.slider(
        "💧 Proximity to Water", 
        min_value=0, max_value=10, value=5, 
        help="Importance of nearby lakes, rivers, or sea."
    )
    weight_urban = st.sidebar.slider(
        "🏢 Urban Services", 
        min_value=0, max_value=10, value=7, 
        help="Importance of built-up areas, roads, and infrastructure."
    )

st.sidebar.divider()

# 4. Action Button (Full width)
run_calculation = st.sidebar.button("🚀 Run Analysis", type="primary", use_container_width=True)

# 5. Custom Footer
st.sidebar.markdown("""
    <div style="text-align: center; margin-top: 30px; font-size: 13px; color: gray;">
        Powered by C++ Zero-Copy Engine<br>
        <i>&copy; Ori Schild 2026</i> ⚡
    </div>
""", unsafe_allow_html=True)

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
            
        elif analysis_type == "Livability Score":

            # 1. Get the image array and the statistics dictionary from the C++ engine
            result, counts = ndvi_module.classify_pixels(green, red, nir)           

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
            

            #liviability score calculation based on user-defined weights
            st.markdown("### Livability Score Calculation")

            total_valid = counts['water'] + counts['vegetation'] + counts['urban']
            no_data = counts['no_data']
            total_pixels = total_valid + no_data

            if total_valid == 0:
                st.error("No valid pixels found for livability score calculation.")
            else:
                # Data quality check (transparent alert for the user)
                total_pixels = total_valid + no_data
                pct_no_data = (no_data / total_pixels) * 100
                if pct_no_data > 20:
                    st.warning(f"⚠️ Note: {pct_no_data:.1f}% of the image is classified as 'No Data' (cloud cover or scan edges). The following metrics are calculated based only on the visible area.")

                # Calculate coverage percentages from the valid area
                pct_water = (counts['water'] / total_valid) * 100
                pct_veg = (counts['vegetation'] / total_valid) * 100
                pct_urban = (counts['urban'] / total_valid) * 100
                
                # Display percentages with streamlit metrics for a clear and engaging presentation
                col1, col2, col3 = st.columns(3)
                col1.metric("💧 Water Bodies", f"{pct_water:.1f}%", f"{counts['water']:,} px", delta_arrow="off",delta_color="off")
                col2.metric("🌲 Vegetation & Parks", f"{pct_veg:.1f}%", f"{counts['vegetation']:,} px", delta_arrow="off",delta_color="off")
                col3.metric("🏢 Urban / Built-up Area", f"{pct_urban:.1f}%", f"{counts['urban']:,} px", delta_arrow="off",delta_color="off")

                st.markdown(f"Total valid pixels: {total_valid:,}")

                
                # Calculate the desired percentages (Target) based on user weights
                total_weight = weight_veg + weight_water + weight_urban
                
                if total_weight == 0:
                    score = 0.0 # Prevent division by zero if all sliders are at 0
                else:
                    target_veg = (weight_veg / total_weight) * 100
                    target_water = (weight_water / total_weight) * 100
                    target_urban = (weight_urban / total_weight) * 100
                    
                    # Calculate the distance (error) between actual and target for each class
                    error_veg = abs(target_veg - pct_veg)
                    error_water = abs(target_water - pct_water)
                    error_urban = abs(target_urban - pct_urban)
                    
                    # Total error divided by 2 (since an over-representation in one class 
                    # exactly equals the under-representation in the others)
                    total_error = (error_veg + error_water + error_urban) / 2
                    
                    # Final score is 100 minus the distance
                    score = 100 - total_error

                # Display the score
                st.markdown("---")
                st.subheader(f"🏆 Personal Livability Score: {score:.1f}/100")
                st.progress(int(score) / 100) # Visual progress bar
                
                # Smart textual output based on the score
                if score >= 80:
                    st.success("✨ Excellent area! The land cover distribution highly matches your preferences.")
                elif score >= 50:
                    st.info("👍 Acceptable area. There is a partial match to your preferences.")
                else:
                    st.error("⚠️ Less suitable area. Consider exploring other regions or adjusting your preferences.")
            
            
            st.subheader("Land Cover Classification")
            st.markdown("Uses a Decision Tree in C++ to classify each pixel based on spectral signatures.")


        # 4. Final Display Settings
        ax.axis('off') # Hide coordinates axes
        st.pyplot(fig) # Render the Matplotlib figure in Streamlit
        st.success("Execution completed in Zero-copy mode!")
        
else:
    info_placeholder.info("Select an analysis mode from the sidebar and click 'Run Analysis'.")