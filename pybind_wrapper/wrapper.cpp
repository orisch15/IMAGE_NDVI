#include <pybind11/pybind11.h> 
#include <pybind11/numpy.h>
#include "../src/ndvi_calculator.hpp"
#include <stdexcept>

namespace py = pybind11;

// Wrapper for NDVI
py::array_t<float> py_calculate_ndvi(py::array_t<float> red_array, py::array_t<float> nir_array) {
    // 1. Request access to the memory buffers of the NumPy arrays
    py::buffer_info buf_red = red_array.request();
    py::buffer_info buf_nir = nir_array.request();

    // 2. Validate that the arrays have the same size
    if (buf_red.size != buf_nir.size) {
        throw std::runtime_error("Input arrays must have the same size");
    }

    // 3. Extract raw pointers to the memory blocks (Zero-copy)
    const float* ptr_red = static_cast<const float*>(buf_red.ptr);
    const float* ptr_nir = static_cast<const float*>(buf_nir.ptr);
    int total_pixels = buf_red.size;

    // 4. Allocate a new NumPy array for the output Array
    py::array_t<float> result_array(total_pixels);
    py::buffer_info buf_result = result_array.request();
    float* ptr_result = static_cast<float*>(buf_result.ptr);

    // 5. Call the pure C++ engine
    calculate_ndvi(ptr_red, ptr_nir, ptr_result, total_pixels);

    // 6. Reshape the 1D output array back to the original 2D image dimensions
    result_array.resize({buf_red.shape[0], buf_red.shape[1]});

    return result_array;
}

// Wrapper for NDWI
py::array_t<float> py_calculate_ndwi(py::array_t<float> green_array, py::array_t<float> nir_array) {
    py::buffer_info buf_green = green_array.request();
    py::buffer_info buf_nir = nir_array.request();

    if (buf_green.size != buf_nir.size) {
        throw std::runtime_error("Input arrays must have the same size");
    }

    const float* ptr_green = static_cast<const float*>(buf_green.ptr);
    const float* ptr_nir = static_cast<const float*>(buf_nir.ptr);
    int total_pixels = buf_green.size;

    py::array_t<float> result_array(total_pixels);
    py::buffer_info buf_result = result_array.request();
    float* ptr_result = static_cast<float*>(buf_result.ptr);

    calculate_ndwi(ptr_green, ptr_nir, ptr_result, total_pixels);

    result_array.resize({buf_green.shape[0], buf_green.shape[1]});

    return result_array;
}

// Wrapper for Pixel Classification
// Note the return type is uint8_t, matching our memory optimization!
py::array_t<uint8_t> py_classify_pixels(py::array_t<float> green_array, py::array_t<float> red_array, py::array_t<float> nir_array) {
    py::buffer_info buf_green = green_array.request();
    py::buffer_info buf_red = red_array.request();
    py::buffer_info buf_nir = nir_array.request();

    if (buf_green.size != buf_red.size || buf_red.size != buf_nir.size) {
        throw std::runtime_error("All input arrays must have the same size");
    }

    const float* ptr_green = static_cast<const float*>(buf_green.ptr);
    const float* ptr_red = static_cast<const float*>(buf_red.ptr);
    const float* ptr_nir = static_cast<const float*>(buf_nir.ptr);
    int total_pixels = buf_green.size;

    // Allocate an 8-bit unsigned integer array for the classification result
    py::array_t<uint8_t> result_array(total_pixels);
    py::buffer_info buf_result = result_array.request();
    uint8_t* ptr_result = static_cast<uint8_t*>(buf_result.ptr);

    classify_pixels(ptr_green, ptr_red, ptr_nir, ptr_result, total_pixels);

    result_array.resize({buf_green.shape[0], buf_green.shape[1]});

    return result_array;
}

// 7. Pybind11 Module Definition
// This creates the actual Python module named 'ndvi_module'
PYBIND11_MODULE(ndvi_module, m) {
    m.doc() = "C++ Engine for Satellite Imagery Analysis"; // Optional module docstring
    
    // Bind the functions so Python can call them
    m.def("calculate_ndvi", &py_calculate_ndvi, "Calculate NDVI from Red and NIR bands");
    m.def("calculate_ndwi", &py_calculate_ndwi, "Calculate NDWI from Green and NIR bands");
    m.def("classify_pixels", &py_classify_pixels, "Classify pixels into Water, Vegetation, or Urban/Bare");
}