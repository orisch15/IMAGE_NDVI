import rasterio
import numpy as np

#midlle file used to load the data and then be called in the app and main files
def load_bands(green_path, red_path, nir_path):
    # Open and read the green band
    with rasterio.open(green_path) as src_green:
        green_band = src_green.read(1).astype(np.float32)
    # Open and read the Red band
    with rasterio.open(red_path) as src_red:
        red_band = src_red.read(1).astype(np.float32)
        
    # Open and read the Near-Infrared (NIR) band
    with rasterio.open(nir_path) as src_nir:
        nir_band = src_nir.read(1).astype(np.float32)
        
    return green_band, red_band, nir_band