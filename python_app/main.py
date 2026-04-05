import rasterio
import numpy as np
import matplotlib.pyplot as plt
import ndvi_module  # type: ignore # Importing our newly compiled C++ module
from data_utils import load_bands  # Import the core logic


# Define file paths (make sure to replace with your actual file names!)
RED_BAND_PATH = '../data/T32UQD_20260318T100741_B04_10m.jp2'
NIR_BAND_PATH = '../data/T32UQD_20260318T100741_B08_10m.jp2'

if __name__ == "__main__":
    #load data from data_utils 
    red, nir = load_bands(RED_BAND_PATH, NIR_BAND_PATH)
    
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