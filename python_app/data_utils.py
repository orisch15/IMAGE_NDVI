import rasterio
import numpy as np

def load_bands(red_path, nir_path):
    # Open and read the Red band
    with rasterio.open(red_path) as src_red:
        red_band = src_red.read(1).astype(np.float32)
        
    # Open and read the Near-Infrared (NIR) band
    with rasterio.open(nir_path) as src_nir:
        nir_band = src_nir.read(1).astype(np.float32)
        
    return red_band, nir_band