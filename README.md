# Raster Band Time-Series Stack Builder

This repository provides a **Python workflow** for automatically extracting a specified band from a collection of multi-band GeoTIFFs and combining the extracted layers into a single **chronologically ordered multi-band GeoTIFF**.

The script is designed for remote sensing and geospatial workflows where a single variable (e.g., NDVI, EVI, land surface temperature, precipitation, or any other raster band) must be assembled into a time-series dataset for subsequent analysis.

---

## 📌 Overview

* **Input:** Multiple multi-band GeoTIFF files
* **Operation:** Extract a user-specified band from each file
* **Temporal organization:** One output band per input image
* **Band metadata:** Acquisition dates automatically parsed from filenames and stored as band descriptions
* **Output:** Multi-band time-series GeoTIFF

The resulting raster preserves the original spatial reference, resolution, and georeferencing information, making it suitable for time-series analysis, phenology studies, change detection, machine learning, and other geospatial applications.

---

## 📂 Input Data Requirements

The input directory should contain GeoTIFF files with filenames that include an acquisition date in **YYYYMMDD** format.

Example:

```text
S2_Stack_20210318.tif
S2_Stack_20210402.tif
S2_Stack_20210417.tif
```

The script assumes that:

* All GeoTIFFs have identical dimensions.
* All GeoTIFFs share the same coordinate reference system (CRS).
* All GeoTIFFs use the same affine transform.
* The target variable is stored in the same band index across all files.

---

## 🧰 Python Dependencies

Install the required packages:

```bash
pip install rasterio numpy
```

---

## 🧪 Workflow

The script performs the following steps:

1. Searches the input directory for GeoTIFF files.
2. Sorts the files chronologically.
3. Extracts the acquisition date from each filename.
4. Reads the specified raster band from every file.
5. Stacks all extracted bands into a three-dimensional array.
6. Writes the stacked array to a multi-band GeoTIFF.
7. Stores the acquisition date as the description of each output band.

---

## 🧾 Output

The output is a single multi-band GeoTIFF in which each band represents the selected variable at one acquisition date.

Example band descriptions:

| Band | Description   |
| ---- | ------------- |
| 1    | NDVI_20210318 |
| 2    | NDVI_20210402 |
| 3    | NDVI_20210417 |

The output can be directly used in GIS software or Python libraries such as Rasterio, GDAL, xarray, or machine learning workflows.

---

## ⚙️ Customization

Only two parameters typically need to be modified:

```python
input_folder = r"path/to/input_folder"
NDVI_BAND = 22
```

Replace `NDVI_BAND` with the index of the band you wish to extract. The script works with any raster variable as long as it occupies the same band position in every input file.

---

## 📄 License

MIT License

---

## Author
**Armin Nakhjiri**

Remote Sensing Scientist

Nakhjiri.Armin@gmail.com

---

*Simple tools for efficient geospatial data processing.*
