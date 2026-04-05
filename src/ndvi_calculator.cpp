#include "ndvi_calculator.hpp"

// Function: NDVI Calculation
void calculate_ndvi(const float* red_band, const float* nir_band, float* output_ndvi, int total_pixels) {
    for (int i = 0; i < total_pixels; ++i) {
        float red = red_band[i];
        float nir = nir_band[i];
        
        // Prevent division by zero (handling image borders or null pixels)
        if (nir + red == 0.0f) {
            output_ndvi[i] = -2.0f; // Arbitrary out-of-bounds value indicating 'No Data'
        } else {
            // Formula: (NIR - Red) / (NIR + Red)
            output_ndvi[i] = (nir - red) / (nir + red);
        }
    }
}

// Function: NDWI Calculation - water detaction
void calculate_ndwi(const float* green_band, const float* nir_band, float* output_ndwi, int total_pixels) {
    for (int i = 0; i < total_pixels; ++i) {
        float green = green_band[i];
        float nir = nir_band[i];
        
        // Prevent division by zero
        if (green + nir == 0.0f) {
            output_ndwi[i] = -2.0f; // 'No Data' marker
        } else {
            // Formula: (Green - NIR) / (Green + NIR)
            output_ndwi[i] = (green - nir) / (green + nir);
        }
    }
}

// Function: Pixel Classification Engine
void classify_pixels(const float* green_band, const float* red_band, const float* nir_band, uint8_t* output_class, int total_pixels) {
    for (int i = 0; i < total_pixels; ++i) {
        float green = green_band[i];
        float red = red_band[i];
        float nir = nir_band[i];

        // Check for missing data in any of the required bands
        if (green + nir == 0.0f || nir + red == 0.0f) {
            output_class[i] = 0; // Class 0: No Data
            continue; // Skip to the next pixel
        }

        // Compute indices on-the-fly for the current pixel
        float ndvi = (nir - red) / (nir + red);
        float ndwi = (green - nir) / (green + nir);

        // Simple Decision Tree Logic
        if (ndwi > 0.0f) {
            output_class[i] = 1; // Class 1: Water (Water reflects green, absorbs NIR)
        } 
        else if (ndvi > 0.3f) {
            output_class[i] = 2; // Class 2: Vegetation (Vegetation highly reflects NIR)
        } 
        else {
            output_class[i] = 3; // Class 3: Urban / Bare Soil / Other
        }
    }
}