import geopandas as gpd
from osgeo import gdal, osr, ogr
from osgeo import gdal_array
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pyproj
from ..base import GeoArray

def read_shp(path, encoding='utf-8'):
    return gpd.read_file(path, encoding=encoding)

def write_shp(shp, path, encoding='utf-8'): 
    shp.to_file(path, encoding)

def read_hdf(path, chans=None):
    ds = gdal.Open(path)
    sds = ds.GetSubDatasets()
    imgs = []
    if chans is None: chans = range(len(sds))
    if isinstance(chans, int): chans = [chans]
    for i in chans:
        ds = gdal.Open(sds[i][0])
        img = ds.ReadAsArray()
        m = ds.GetGeoTransform()
        m = np.array(m).reshape((2,3))
        prj = ds.GetProjection()
        imgs.append(img)
    if len(chans) == 1: imgs = imgs[0]
    else: imgs = np.array(imgs).transpose((1,2,0))
    return GeoArray(imgs, prj, m)

def read_tif(path, chans=None):
    ds = gdal.Open(path)
    if chans is None: chans = range(ds.RasterCount)
    if isinstance(chans, int): chans = [chans]
    prj = ds.GetProjection()
    m = ds.GetGeoTransform()
    m = np.array(m).reshape((2,3))
    imgs = [ds.GetRasterBand(i+1).ReadAsArray() for i in chans]
    if len(chans)==1: imgs = imgs[0]
    else: imgs = np.array(imgs).transpose((1,2,0))
    return GeoArray(imgs, prj, m)

def read_raster(path, chans=None):
    if 'hdf' in path.lower(): return read_hdf(path, chans)
    if 'tif' in path.lower(): return read_tif(path, chans)

def read_tif_box(path):
    ds = gdal.Open(path)
    prj = ds.GetProjection()
    m = ds.GetGeoTransform()
    m = np.array(m).reshape((2,3))
    #chans = ['Channel:%d'%i for i in range(ds.RasterCount)]
    rs = range(ds.RasterCount)
    chans = [ds.GetRasterBand(i+1).GetDescription() for i in rs]
    shape = (ds.RasterYSize, ds.RasterXSize)
    return (shape, prj, m, chans)

def read_hdf_box(path):
    ds = gdal.Open(path)
    sds = ds.GetSubDatasets()
    rs = gdal.Open(sds[0][0])
    prj = rs.GetProjection()
    m = rs.GetGeoTransform()
    m = np.array(m).reshape((2,3))
    chans = [i[1] for i in sds]
    shape = (rs.RasterYSize, rs.RasterXSize)
    return (shape, prj, m, chans)

def read_raster_box(path):
    if 'hdf' in path.lower(): return read_hdf_box(path)
    if 'tif' in path.lower(): return read_tif_box(path)


def write_tif(raster, path, compress=None, nodata=None):
    #if isinstance(raster, tuple): raster = [raster]
    driver = gdal.GetDriverByName("GTiff")
    tps = {np.uint8:gdal.GDT_Byte, np.int16:gdal.GDT_Int16,
           np.int32:gdal.GDT_Int32, np.uint16:gdal.GDT_UInt16,
           np.uint32:gdal.GDT_UInt32, np.float32:gdal.GDT_Float32,
           np.float64:gdal.GDT_Float64}
    options = [] if compress is None else ['COMPRESS=%s'%compress]
    tif = driver.Create(path, raster.shape[1], raster.shape[0],
                        raster.channels(), tps[raster.dtype.type], options=options)
    tif.SetGeoTransform(raster.mat.ravel())
    crs = osr.SpatialReference()
    crs.ImportFromProj4(pyproj.CRS(raster.crs).to_proj4())
    tif.SetProjection(crs.ExportToWkt())
    for i in range(raster.channels()):
        b = tif.GetRasterBand(i+1)
        b.WriteArray(raster.channels(i))
        if not nodata is None: b.SetNoDataValue(nodata)

def array_as_shp(raster, path, field='class'):
    tif = gdal_array.OpenArray(raster)
    tif.SetGeoTransform(raster.mat.ravel())
    crs = osr.SpatialReference()
    crs.ImportFromProj4(pyproj.CRS(raster.crs).to_proj4())
    tif.SetProjection(crs.ExportToWkt())
    for i in range(raster.channels()):
        tif.GetRasterBand(i+1).WriteArray(raster.channels(i))
    band = tif.GetRasterBand(1)
    driver = ogr.GetDriverByName("ESRI Shapefile")
    outDatasource = driver.CreateDataSource(path)
    srs = osr.SpatialReference()
    srs.ImportFromWkt( tif.GetProjectionRef() )
    outLayer = outDatasource.CreateLayer(path, srs)
    newField = ogr.FieldDefn(field, ogr.OFTInteger)
    outLayer.CreateField(newField)
    gdal.Polygonize(band, None, outLayer, 0, [],callback=None)  
    outDatasource.Destroy()

def show_raster(raster, c=0):
    plt.imshow(raster.imgs[c])

def show_shp(shp):
    shp.plot()
    plt.show()
    
if __name__ == '__main__':
    shp = read_shp('../../tasks/country_china_wheat_2018/region.shp')
    #plot_shp(shp)
