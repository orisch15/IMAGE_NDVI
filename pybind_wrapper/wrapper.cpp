#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include "../src/ndvi_calculator.hpp"
#include <stdexcept>

namespace py = pybind11;

// פונקציית העטיפה שתתקשר ישירות עם פייתון
py::array_t<float> calculate_ndvi_wrapper(py::array_t<float> red_array, py::array_t<float> nir_array) {
    // 1. We request the "Buffer Info" from the Python object
    py::buffer_info red_buf = red_array.request();
    py::buffer_info nir_buf = nir_array.request();

    // וידוא בטיחות - בדיקה ששתי המטריצות באותו גודל
    if (red_buf.size != nir_buf.size) {
        throw std::runtime_error("Red and NIR arrays must have the same size");
    }

    // יצירת מערך NumPy ריק עבור התוצאה, באותו גודל של הקלט
    auto result_array = py::array_t<float>(red_buf.size);
    py::buffer_info result_buf = result_array.request();

    // 2. We extract the raw Memory Pointer
    float* red_ptr = static_cast<float*>(red_buf.ptr);
    float* nir_ptr = static_cast<float*>(nir_buf.ptr);
    float* result_ptr = static_cast<float*>(result_buf.ptr);

    // 3. We pass these pointers to the math function
    calculate_ndvi(red_ptr, nir_ptr, result_ptr, red_buf.size);

    // עיצוב התוצאה כמטריצה דו-ממדית (כדי שתתאים להצגה כתמונה)
    result_array.resize({red_buf.shape[0], red_buf.shape[1]});

    return result_array;
}

// פקודת המאקרו שיוצרת את המודול הסופי עבור פייתון
PYBIND11_MODULE(ndvi_module, m) {
    m.doc() = "NDVI Calculation Module written in C++";
    m.def("calculate_ndvi", &calculate_ndvi_wrapper, "Calculates NDVI from Red and NIR NumPy arrays");
}