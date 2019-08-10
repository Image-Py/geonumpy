import pyproj
import osr
import numpy as np
from pygis.io import read_tif, read_shp


wkt1 = 'PROJCS["WGS_1984_Albers",GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137.0,298.257223563]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]],PROJECTION["Albers"],PARAMETER["False_Easting",4000000.0],PARAMETER["False_Northing",0.0],PARAMETER["Central_Meridian",105.0],PARAMETER["Standard_Parallel_1",25.0],PARAMETER["Standard_Parallel_2",47.0],PARAMETER["Latitude_Of_Origin",0.0],UNIT["Meter",1.0]]'
wkt2 = 'PROJCS["China_Lambert_Conformal_Conic",GEOGCS["GCS_Beijing_1954",DATUM["D_Beijing_1954",SPHEROID["Krasovsky_1940",6378245.0,298.3]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]],PROJECTION["Lambert_Conformal_Conic"],PARAMETER["False_Easting",0.0],PARAMETER["False_Northing",0.0],PARAMETER["Central_Meridian",105.0],PARAMETER["Standard_Parallel_1",30.0],PARAMETER["Standard_Parallel_2",62.0],PARAMETER["Latitude_Of_Origin",0.0],UNIT["Meter",1.0]]'
wkt1 = read_tif('../data/class/070E30N.tif')[0][1]
#prj2 = read_shp('../data/shape/area.shp')[1]
prj1 = osr.SpatialReference()
prj1.ImportFromWkt(wkt1)
prj2 = osr.SpatialReference()
prj2.ImportFromWkt(open('../data/shape/area.prj').readline())

'''
prj1 = osr.SpatialReference()
prj1.ImportFromWkt(wkt1)

prj2 = osr.SpatialReference()
prj2.ImportFromWkt(wkt2)

ct = osr.CoordinateTransformation(prj1, prj2)
# 116.41063642056693]), array('d', [39.91194298039171
pts = np.array([(116,39)])
rst = ct.TransformPoints(pts)


prj1 = pyproj.CRS(wkt1)
prj2 = pyproj.CRS(wkt2)
ct = pyproj.Transformer.from_crs(prj1, prj2)
print(ct.transform(116, 39))
'''
