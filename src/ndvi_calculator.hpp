#ifndef NDVI_CALCULATOR_HPP
#define NDVI_CALCULATOR_HPP
#pragma once

#include <cstdint> // Required for uint8_t
#include <cstddef>

/// Data structure to hold pixel classification counts
struct ClassCounts {
    size_t no_data;
    size_t water;
    size_t vegetation;
    size_t urban;
};

// Calculate Normalized Difference Vegetation Index (NDVI)
void calculate_ndvi(const float* red_band, const float* nir_band, float* output_ndvi, int total_pixels);

// Calculate Normalized Difference Water Index (NDWI)
void calculate_ndwi(const float* green_band, const float* nir_band, float* output_ndwi, int total_pixels);

// Classify pixels based on spectral indices
// Returns an 8-bit unsigned integer per pixel + the data structure with class counts for summary statistics: 
// 0 = No Data, 1 = Water, 2 = Vegetation, 3 = Urban/Bare Soil
ClassCounts classify_pixels(const float* green_band, const float* red_band, const float* nir_band, uint8_t* output_class, int total_pixels);

#endif