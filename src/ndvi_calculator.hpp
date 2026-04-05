#pragma once

// פונקציה המקבלת מצביעים למערכי הפיקסלים ואת כמות הפיקסלים הכוללת
void calculate_ndvi(const float* red_band, const float* nir_band, float* output_ndvi, int total_pixels);