import rasterio
import numpy as np
import matplotlib.pyplot as plt
import ndvi_module  # Importing our newly compiled C++ module

# Define file paths (make sure to replace with your actual file names!)
RED_BAND_PATH = '../data/T32UQD_20260318T100741_B04_10m.jp2'
NIR_BAND_PATH = '../data/T32UQD_20260318T100741_B08_10m.jp2'

def load_satellite_data():
    print("start loading sattelite data...")
    
    # פתיחת קובץ הערוץ האדום
    with rasterio.open(RED_BAND_PATH) as src_red:
        # קריאת הנתונים למטריצה והמרתם למספרים עשרוניים (Float)
        red_band = src_red.read(1).astype(np.float32) # read - rasterio comment, astype - numpy commend for turning each matirx block to a float
        print(f"red channel loaded succelsfully! size is :{red_band.shape}") # prints the dimantions (shape is a numpy commend)
        
    # פתיחת קובץ ערוץ האינפרה-אדום הקרוב
    with rasterio.open(NIR_BAND_PATH) as src_nir:
        nir_band = src_nir.read(1).astype(np.float32)
        print(f" NIR channel loaded succelsfully! size is :{nir_band.shape}")
        
    return red_band, nir_band

if __name__ == "__main__":
    # 1. Load the massive arrays in Python
    red, nir = load_satellite_data()
    
    print("Sending data to the C++ engine for NDVI calculation...")
    
    # 2. Call the C++ function
    # This executes at peak efficiency over the memory block and returns a new NumPy array
    ndvi_result = ndvi_module.calculate_ndvi(red, nir)
    
    print("Calculation completed successfully! Preparing the visualization...")
    
    # 3. Visualize the result
    plt.figure(figsize=(10, 10))
    
    # Render the matrix as an image. 
    # vmin and vmax bound the valid NDVI range (-1.0 to 1.0).
    # cmap='RdYlGn' applies a Red-Yellow-Green continuous color map.
    plt.imshow(ndvi_result, cmap='RdYlGn', vmin=-1, vmax=1)
    
    # Add a color legend and title
    plt.colorbar(label='NDVI Value')
    plt.title('NDVI Map calculated with C++ Engine')
    
    # Hide the axes for a cleaner visual representation
    plt.axis('off')
    
    # Display the final plot
    plt.show()