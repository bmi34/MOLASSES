import os
import sys
import numpy as np
import pandas as pd
from osgeo import gdal, osr

def csv_to_raster(csv_path, output_raster, pixel_size=1):
    """Converts a CSV file to a raster format."""
    try:
        data = pd.read_csv(csv_path)
    except Exception as e:
        print(f"Error reading CSV file {csv_path}: {e}")
        return
    
    if not {'EAST', 'NORTH', 'THICKNESS'}.issubset(data.columns):
        raise ValueError(f"CSV file {csv_path} is missing required columns.")

    x_min, x_max = data['EAST'].min(), data['EAST'].max()
    y_min, y_max = data['NORTH'].min(), data['NORTH'].max()
    x_res = int((x_max - x_min) / pixel_size) + 1
    y_res = int((y_max - y_min) / pixel_size) + 1

    driver = gdal.GetDriverByName('GTiff')
    raster = driver.Create(output_raster, x_res, y_res, 1, gdal.GDT_Float32)

    if raster is None:
        print(f"Error creating raster file {output_raster}.")
        return
    
    raster.SetGeoTransform((x_min, pixel_size, 0, y_max, 0, -pixel_size))

    srs = osr.SpatialReference()
    srs.ImportFromEPSG(2193)  # Set this to your EPSG projection code
    raster.SetProjection(srs.ExportToWkt())

    thickness_grid = np.full((y_res, x_res), np.nan)
    for _, row in data.iterrows():
        x_index = int((row['EAST'] - x_min) / pixel_size)
        y_index = int((y_max - row['NORTH']) / pixel_size)
        thickness_grid[y_index, x_index] = row['THICKNESS']

    band = raster.GetRasterBand(1)
    band.WriteArray(thickness_grid)
    band.SetNoDataValue(np.nan)
    raster.FlushCache()
    print(f"Raster created successfully at {output_raster}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python csv_to_raster.py <input_csv> <output_raster>")
        sys.exit(1)

    input_csv = sys.argv[1]
    output_raster = sys.argv[2]
    csv_to_raster(input_csv, output_raster)
