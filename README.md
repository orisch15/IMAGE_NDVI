# 🌍 Satellite Imagery Analysis Engine

## Overview
This project calculates the Normalized Difference Vegetation Index (NDVI) from Sentinel-2 satellite imagery. It leverages a high-performance **Hybrid Zero-Copy Architecture**:
*   **Data Management:** Python handles data loading (`rasterio`, `numpy`) and visualizations (`matplotlib`).
*   **Heavy Computation:** A C++ engine processes memory pointers directly to achieve maximum efficiency, bridged to Python via `pybind11` and compiled with `CMake`.
*   **User Interface:** A Web UI built with `Streamlit` for real-time interaction and visualization.

---

## Directory Structure

```plaintext
IMAGE_NDVI/
├── venv/
├── build/                 # CMake build directory
├── data/                  # Contains Sentinel-2 .jp2 files (Band 04 and Band 08)
├── src/
│   ├── ndvi_calculator.hpp 
│   └── ndvi_calculator.cpp # Core C++ logic: NDVI = (NIR - Red) / (NIR + Red)
├── pybind_wrapper/
│   └── wrapper.cpp        # pybind11 integration layer
├── python_app/
│   ├── app.py             # Streamlit Web UI entry point
│   ├── main.py            # CLI entry point (headless execution)
│   ├── data_utils.py      # Shared logic and data loaders
│   └── ndvi_module...so   # Compiled C++ binary
└── CMakeLists.txt         # Compilation instructions

Architectural Decisions & Best Practices
The Separation of Logic (data_utils.py)
In this project, the core logic for loading satellite bands is isolated in data_utils.py. We explicitly avoid importing functions directly from main.py into the app.py Web UI for the following architectural reasons:

1. Separation of Entry Points
main.py is designed to be the main execution script for the Command Line Interface (CLI). app.py is the entry point for the Streamlit Web Application. Mixing the two creates tight coupling. By extracting shared functions into a neutral data_utils.py file, both the CLI and the Web UI can utilize the same tools without depending on each other.

2. Python import Execution Behavior
When Python imports a module, it executes the file from top to bottom. If app.py were to import from main.py, any global variables, environment configurations, or executable code outside of the if __name__ == "__main__": block in main.py would run unintentionally. This can cause redundant processing, unexpected pop-ups (like matplotlib windows), and degraded performance.

3. Preventing Circular Imports
As the application scales, components often need to share data. If app.py imports from main.py, and later main.py needs a utility from app.py, Python will enter an infinite loading loop, resulting in a fatal ImportError. Keeping data handling in data_utils.py completely breaks this dependency cycle and ensures a stable hierarchy:

Data & Logic Layer: ndvi_module (C++) and data_utils.py (Python).

Execution & UI Layer: main.py (CLI) and app.py (Web UI).

## How to Run

Before running the application, you must activate the virtual environment to ensure all dependencies (such as `rasterio`, `streamlit`, and the compiled C++ module) are loaded correctly.

**1. Activate the Virtual Environment (Mac/Linux)**  
Open your terminal, navigate to the root directory of the project (`IMAGE_NDVI/`), and run:
```bash
source venv/bin/activate
```

**2. Command Line Execution (Headless)**  
Once the environment is active, you can run the core engine without the UI:
```bash
cd python_app
python main.py
```

**3. Launch the Streamlit Web UI**  
To start the interactive web application, run:
```bash
cd python_app
streamlit run app.py
```

**4. Deactivate the Environment**  
When you are finished working on the project, you can exit the virtual environment by running:
```bash
deactivate
```
```