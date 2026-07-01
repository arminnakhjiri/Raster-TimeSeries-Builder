import glob
import os
import re

import numpy as np
import rasterio

# Input / Output
input_folder = r"D:\path\to\input_folder"
output_tif = os.path.join(input_folder, "TimeSeries_Stack.tif")

# Band to extract (1-based index)
TARGET_BAND = 22

files = sorted(glob.glob(os.path.join(input_folder, "S2_Stack_*.tif")))

if not files:
    raise FileNotFoundError("No TIFF files found.")

with rasterio.open(files[0]) as src:
    meta = src.meta.copy()
    dtype = src.dtypes[TARGET_BAND - 1]

stack = []
band_names = []

for file in files:

    match = re.search(r"(\d{8})", os.path.basename(file))

    if match is None:
        print(f"Skipping {os.path.basename(file)} (date not found).")
        continue

    date = match.group(1)

    with rasterio.open(file) as src:
        stack.append(src.read(TARGET_BAND))

    band_names.append(date)
    print(f"Added: {date}")

stack = np.stack(stack)

meta.update(
    count=len(stack),
    dtype=dtype
)

with rasterio.open(output_tif, "w", **meta) as dst:
    for i, band in enumerate(stack, start=1):
        dst.write(band, i)
        dst.set_band_description(i, band_names[i - 1])

print(f"\nCreated: {output_tif}")
print(f"Number of bands: {len(stack)}")
