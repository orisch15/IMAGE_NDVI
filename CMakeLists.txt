# הגדרת הגרסה המינימלית הנדרשת
cmake_minimum_required(VERSION 3.12)
project(Image_NDVI)

# מציאת פייתון (גרסה 3) בתוך הסביבה הווירטואלית שלנו
find_package(Python3 COMPONENTS Interpreter Development REQUIRED)

# הרצת פקודת פייתון קצרה כדי למצוא איפה pybind11 מותקנת בתוך ה-venv
execute_process(
    COMMAND "${Python3_EXECUTABLE}" -c "import pybind11; print(pybind11.get_cmake_dir())"
    OUTPUT_VARIABLE PYBIND11_CMAKE_DIR
    OUTPUT_STRIP_TRAILING_WHITESPACE
)

# צירוף הנתיב שמצאנו כדי ש-CMake יכיר אותו
list(APPEND CMAKE_PREFIX_PATH "${PYBIND11_CMAKE_DIR}")
find_package(pybind11 REQUIRED)

# הפקודה המרכזית: קימפול קבצי ה-C++ למודול שפייתון יודעת לקרוא
pybind11_add_module(ndvi_module 
    src/ndvi_calculator.cpp 
    pybind_wrapper/wrapper.cpp
)

# הגדרה נוחה: זריקת הקובץ המוכן ישירות לתוך תיקיית הפייתון שלנו
set_target_properties(ndvi_module PROPERTIES LIBRARY_OUTPUT_DIRECTORY "${CMAKE_SOURCE_DIR}/python_app")