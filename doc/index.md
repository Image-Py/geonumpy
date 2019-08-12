# geonumpy 地理数据工具包

geonumpy的编写目的是提供一套开源，易用，高效的地理数据处理库。包括矢量数据，图像数据的读取，图像拼接，重采样，地图绘制等。



## pygis的几个重要依赖

1. Numpy：作为科学计算库，自然离不开numpy
2. pandas, scipy, scikit-image，这几个常用库为我们提供了表格与图像处理功能
3. gdal，fiona：gdal是一套功能强大的地理数据处理库，可以读取矢量，图像数据，但功能相对比较底层，代码不够pythonic，而fiona是基于gdal的更方便的数据读取库。
4. shapely，geopandas：shapely是python的计算几何库，实现了矢量算法，geopandas是shapely与pandas的结合，可以方便的带着属性进行几何运算，实现类似arcgis里的图形关系运算。
5. pyproj：著名的地图投影项目，提供各种地理坐标系转换。



## geonumpy API 文档

**[GeoArray: 带投影的数组](api_geoarray.md)**

1. [GeoArray](api_geoarray.md#Class GeoArray)
2. [geoarray](api_geoarray.md#geoarray)
3. [frombox](api_geoarray.md#frombox)

**[io: 数据读取与存储](api_io.md)**

1. [read_shp](api_io.md#read_shp)
2. [write_shp](api_io.md#write_shp)
3. [read_tif ](api_io.md#read_tif)
4. [read_hdf](api_io.md#read_hdf)
5. [write_tif](api_io.md#write_tif)
6. [write_hdf(未实现)](api_io.md#write_hdf)
7. [read_tif_info ](api_io.md#read_tif_info)
8. [read_hdf_info](api_io.md#read_hdf_info)
9. [read_raster](api_io.md#read_raster)
10. [read_raster_info](api_io.md#read_raster_info)

**[util: 几个辅助函数](api_util.md)**

1. [shp2box](api_util.md#shp2box)
2. [box2shp](api_util.md#box2shp)

**[match: 配准与拼接](api_match.md)**

1. [match_one](api_match.md#match_one)
2. [match_multi](api_match.md#match_multi)
3. [build_index](api_match.md#build_index)
4. [match_idx](api_match.md#match_idx)

**[draw: 地图绘制](api_draw.md)**

1. [draw_polygon](api_draw.md#draw_polygon)

2. [draw_line](api_draw.md#draw_line)

3. [draw_text](api_draw.md#draw_text)

4. [draw_lab](api_draw.md#draw_lab)

5. [draw_unit](api_draw.md#draw_unit)

6. [draw_N](api_draw.md#draw_N)

7. [draw_bound](api_draw.md#draw_bound)

8. [draw_ruler](api_draw.md#draw_ruler)

9. [draw_style](api_draw.md#draw_style)

**[pretreat: 预处理](pretreat.md)**

1. [大气校正(未实现)](pretreat.md)
2. [degap](pretreat.md#degap)

**[indicate: 常规指标](indicate.md)**

1. [ndvi](indicate.md#ndvi)

2. what should be added here! any issue is welcom!


**[download: 影像下载](api_download.md)**

1. [modis_search](api_download.md#modis_search)
2. [modis_download](api_download.md#modis_download)
3. [landsat_search](lapi_download.md#landsat_search)
4. [landsat_download(未实现)](api_download.md#landsat_download)
5. [sentinal_search(未实现)](lapi_download.md)
6. [sentinal_download(未实现)](api_download.md)



## geonumpy 用户手册

**[GeoArray: 带投影的数组](dem_geoarray.md)**

1. [创建 GeoArray 对象](dem_geoarray.md#创建-GeoArray-对象)
2. [GeoArray 的运算](dem_geoarray.md#GeoArray-的运算)
3. [切片自动处理投影矩阵](dem_geoarray.md#GeoArray-的切片)
4. [生成方法](dem_geoarray.md#获取-box-及从-box-创建)
5. [多通道处理](dem_geoarray.md#多通道处理)

**[io: 数据读取与存储](dem_io.md)**

1. [读写shapefile](dem_io.md#读写shapefile)
2. [读写 tif/hdf](dem_io.md#读写-tif/hdf)
3. [读写影像空间信息](dem_io.md#读写影像空间信息)

**[match: 拼接与配准](dem_match.md)**

1. [素材展示](dem_match.md#素材展示)
2. [单图投影](dem_match.md#单图投影)
3. [多图投影](dem_match.md#多图投影)
4. [创建空间索引](dem_match.md#创建空间索引)
5. [通过索引批量匹配](dem_match.md#通过索引批量匹配)
6. [投影转换](dem_match.md#单图投影转换)

**[draw: 地图绘制](dem_draw.md)**

1. [矢量图绘制](dem_draw.md#矢量图绘制)
2. [图例的使用](dem_draw.md#图例的使用)
3. [根据面积进行等级划分](dem_draw.md#根据面积进行等级划分)
4. [土地利用类型图绘制](dem_draw.md#土地利用类型图绘制)

**[pretreat: 预处理](dem_pretreat.md)**

1. [去条带](dem_pretreat.md#去条带)

**[综合应用：森林覆盖率统计](dem_forest_statistic.md)**

1. [用地类型拼接](dem_forest_statistic.md#用地类型拼接)
2. [市级行政区标记](dem_forest_statistic.md#市级行政区标记)
3. [用地类型及标记展示](dem_forest_statistic.md#用地类型及标记展示)
4. [各个城市森林覆盖率计算](dem_forest_statistic.md#各个城市森林覆盖率计算)
5. [绘制森林覆盖率专题图](dem_forest_statistic.md#绘制森林覆盖率专题图)



