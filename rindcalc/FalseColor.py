import os
import numpy as np
from osgeo import gdal
from glob import glob


def FalseColor(landsat_dir, out_composite):

    # Create list with file names
    green = glob(landsat_dir + "/*B3.tif")
    red = glob(landsat_dir + "/*B4.tif")
    nir = glob(landsat_dir + "/*B5.tif")

    def norm(array):
        """Normalizes numpy arrays into scale 0.0 - 1.0"""
        array_min, array_max = array.min(), array.max()
        return ((array - array_min) / (array_max - array_min))

    green_path = gdal.Open(os.path.join(landsat_dir, green[0]))
    green_band = norm(green_path.GetRasterBand(1).ReadAsArray().astype(np.float32))
    red_path = gdal.Open(os.path.join(landsat_dir, red[0]))
    red_band = norm(red_path.GetRasterBand(1).ReadAsArray().astype(np.float32))
    NIR_path = gdal.Open(os.path.join(landsat_dir, nir[0]))
    nir_band = norm(NIR_path.GetRasterBand(1).ReadAsArray().astype(np.float32))
    snap = gdal.Open(os.path.join(landsat_dir, red[0]))

    # Save Raster
    if os.path.exists(out_composite):
        raise IOError('False Color composite raster already created')
    if not os.path.exists(out_composite):
        driver = gdal.GetDriverByName('GTiff')
        metadata = driver.GetMetadata()
        shape = red_band.shape
        dst_ds = driver.Create(out_composite, xsize=shape[1], ysize=shape[0], bands=3, eType=gdal.GDT_Float32)
        proj = snap.GetProjection()
        geo = snap.GetGeoTransform()
        dst_ds.SetGeoTransform(geo)
        dst_ds.SetProjection(proj)
        dst_ds.GetRasterBand(1).WriteArray(nir_band)
        dst_ds.GetRasterBand(2).WriteArray(red_band)
        dst_ds.GetRasterBand(3).WriteArray(green_band)
        dst_ds.FlushCache()
        dst_ds = None

    return print('False Color composite created.')