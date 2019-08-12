# geonumpy.io

io 提供了一系列常用数据类型的读取，除了影像数据之外，也重命名了geopandas读取shapefile的方法。



## 读写shapefile

```python
import geonumpy.io as gio

gdf = gio.read_shp('../data/shape/shandong.shp')

print(gdf.crs)
>>> {'proj': 'longlat', 'ellps': 'GRS80', 'no_defs': True}

print(gdf)
>>> gdf
   name                                           geometry
0   济南市  POLYGON ((116.5148065247014 36.38448656000679,...
1   青岛市  (POLYGON ((120.9778956949305 36.42131830969231...
2   淄博市  POLYGON ((117.7029971845725 36.65135262502366,...
3   枣庄市  POLYGON ((117.1832330898353 34.82091945456921,...
4   东营市  (POLYGON ((118.2108902247041 37.38519372011416...
5   烟台市  (POLYGON ((120.2516180601255 37.11630801969937...
6   潍坊市  POLYGON ((118.2356711848773 36.41432422458337,...
7   济宁市  POLYGON ((116.1290081102362 35.63315157458555,...
8   泰安市  POLYGON ((116.2236255245983 36.16986052983964,...
9   威海市  (POLYGON ((121.7099395947366 37.12126350001057...
10  日照市  POLYGON ((118.8712478898783 35.39324951465341,...
11  莱芜市  POLYGON ((117.6633433146424 36.52794210504419,...
12  临沂市  POLYGON ((117.6154824151814 35.13172327500916,...
13  德州市  POLYGON ((115.8603655451338 37.07219694962959,...
14  聊城市  POLYGON ((115.3349590553162 36.37903970541811,...
15  滨州市  POLYGON ((117.3156585848759 37.50292387473706,...
16  菏泽市  POLYGON ((115.1253803253418 34.99438765516618,...

gdf.plot()
plt.show()
```
![](imgs/01.png)

read_shp 是调用 geopandas 的 read_file 方法，返回的是 GeoDataFrame 对象，带有 crs 以及一个 geometry 列。

```python
gdf_wgs = gdf.to_crs(4326)
gio.write_shp(gdf_wgs, '../data/result/shandong_wgs.shp')
```

这里我们将 gdf 转为wgs1984 坐标，并重新存储。（更多用法请参见geopandas的文档）



## 读写 tif/hdf

```python
path = '../data/landsat/LC08_L1TP_122033_20190506_20190506_01_RT_B5.TIF'
landsat = gio.read_tif(path)

>>> landsat.shape
(7821, 7691)

>>> landsat.crs   
'PROJCS["WGS 84 / UTM zone 50N",GEOGCS["WGS 84",DATUM["WGS_1984",SPHEROID["WGS 84",6378137,298.257223563,AUTHORITY["EPSG","7030"]],AUTHORITY["EPSG","6326"]],PRIMEM["Greenwich",0,AUTHORITY["EPSG","8901"]],UNIT["degree",0.0174532925199433,AUTHORITY["EPSG","9122"]],AUTHORITY["EPSG","4326"]],PROJECTION["Transverse_Mercator"],PARAMETER["latitude_of_origin",0],PARAMETER["central_meridian",117],PARAMETER["scale_factor",0.9996],PARAMETER["false_easting",500000],PARAMETER["false_northing",0],UNIT["metre",1,AUTHORITY["EPSG","9001"]],AXIS["Easting",EAST],AXIS["Northing",NORTH],AUTHORITY["EPSG","32650"]]'

>>> landsat.mat  
array([[ 4.556850e+05,  3.000000e+01,  0.000000e+00],
       [ 4.423215e+06,  0.000000e+00, -3.000000e+01]])

plt.imshow(landsat, cmap='gray')
plt.show()
```

![landsat](./imgs/02.png)

我们可以用 read_tif 方法将 tif 文件读取为 GeoArray 对象，对于多通道，可以加入chan参数读取指定通道，默认读取全部通道。

```python
gio.write_tif(landsat, '../data/result/landsat_new.tif')
```

同样我们可以将 GeoArray 对象写成 tif 文件。

```python
# read the hdf's first channel, if pass a list, means read these channels
modis = gio.read_hdf('../data/modis/MOD09Q1.A2019017.h28v05.006.2019030120612.hdf', 0)
# read_raster can select the reader by filename, read both tif and hdf
modis = gio.read_raster('../data/modis/MOD09Q1.A2019017.h28v05.006.2019030120612.hdf') 
```

同样的，我们可以用 read_hdf, write_hdf 对hdf文件进行读写，read_raster 可以同时读取 tif/hdf。



## 读写影像基础信息

```python
path = '../data/landsat/LC08_L1TP_122033_20190506_20190506_01_RT_B5.TIF'
box = gio.read_tif_box(path)

print(box)
>>> ((7821, 7691), 
'PROJCS["WGS 84 / UTM zone 50N",GEOGCS["WGS 84",DATUM["WGS_1984",SPHEROID["WGS 84",6378137,298.257223563,AUTHORITY["EPSG","7030"]],AUTHORITY["EPSG","6326"]],PRIMEM["Greenwich",0,AUTHORITY["EPSG","8901"]],UNIT["degree",0.0174532925199433,AUTHORITY["EPSG","9122"]],AUTHORITY["EPSG","4326"]],PROJECTION["Transverse_Mercator"],PARAMETER["latitude_of_origin",0],PARAMETER["central_meridian",117],PARAMETER["scale_factor",0.9996],PARAMETER["false_easting",500000],PARAMETER["false_northing",0],UNIT["metre",1,AUTHORITY["EPSG","9001"]],AXIS["Easting",EAST],AXIS["Northing",NORTH],AUTHORITY["EPSG","32650"]]',
array([[ 4.556850e+05,  3.000000e+01,  0.000000e+00],
       [ 4.423215e+06,  0.000000e+00, -3.000000e+01]]), 
['Channel:0'])
```

read_tif_box 并不直接读取像素信息，只读取相关的空间信息，它的好处是，速度快，并且不会占用大量内存，而用空间信息，我们可以进行简单的位置判断(比如match模块下的 build_idx 创建空间索引)，在必要的时候再读取像素信息，或者使用 gnp.frombox 实例化。与之类似的，我们也可以使用 read_hdf_box 读取 hdf 的空间信息。或者使用 read_raster_box 自动识别类型。