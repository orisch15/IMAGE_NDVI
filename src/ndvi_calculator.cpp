#include "ndvi_calculator.hpp"

void calculate_ndvi(const float* red_band, const float* nir_band, float* output_ndvi, int total_pixels) {
    // לולאה שרצה על כל הפיקסלים במערך
    for (int i = 0; i < total_pixels; ++i) {
        float red = red_band[i];
        float nir = nir_band[i];
        
        // הגנה מפני חלוקה באפס (למשל, פיקסלים ריקים בשולי התמונה)
        if (nir + red == 0.0f) {
            output_ndvi[i] = -2.0f; // ערך שרירותי שמייצג "חוסר מידע" (NDVI תמיד בין -1 ל-1)
        } else {
            // הנוסחה: (NIR - Red) / (NIR + Red)
            output_ndvi[i] = (nir - red) / (nir + red);
        }
    }
    // 1 - major forested area
    // 0 - nutral - roads
    // -1 - water resource
}