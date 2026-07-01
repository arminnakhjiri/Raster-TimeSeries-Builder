import os
import re
import glob

import numpy as np
import rasterio

# Inputs
input_folder = r"path/to/input_folder"
output_tif = os.path.join(input_folder, "TimeSeries_Stack.tif")

# Band to extract (1-based index)
TARGET_BAND = 22

# Find input files
files = sorted(glob.glob(os.path.join(input_folder, "S2_Stack_*.tif")))

if len(files) == 0:
    raise Exception("No TIFF files found.")

# Read reference metadata
with rasterio.open(files[0]) as src:
    meta = src.meta.copy()
    height = src.height
    width = src.width
    crs = src.crs
    transform = src.transform
    dtype = src.dtypes[TARGET_BAND - 1]

# Extract target band
stack = []
band_names = []

for f in files:

    fname = os.path.basename(f)

    m = re.search(r"(\d{8})", fname)

    if m is None:
        print(f"Skipping {fname} (no date found)")
        continue

    date_str = m.group(1)

    with rasterio.open(f) as src:
        band = src.read(TARGET_BAND)

    stack.append(band)
    band_names.append(date_str)

    print(f"Added: {date_str}")

stack = np.stack(stack)

# Write output
meta.update({
    "count": len(stack),
    "dtype": dtype
})

with rasterio.open(output_tif, "w", **meta) as dst:

    for i in range(len(stack)):
        dst.write(stack[i], i + 1)
        dst.set_band_description(i + 1, band_names[i])

print("\nFinished.")
print(f"Output: {output_tif}")
print(f"Bands: {len(stack)}")
