# geonumpy 地理数据工具包

geonumpy的编写目的是提供一套开源，易用，高效的地理数据处理库。包括矢量数据，图像数据的读取，图像拼接，重采样，地图绘制等。



## pygis的几个重要依赖

1. Numpy：作为科学计算库，自然离不开numpy
2. pandas, scipy, scikit-image，这几个常用库为我们提供了表格与图像处理功能
3. gdal，fiona：gdal是一套功能强大的地理数据处理库，可以读取矢量，图像数据，但功能相对比较底层，代码不够pythonic，而fiona是基于gdal的更方便的数据读取库。
4. shapely，geopandas：shapely是python的计算几何库，实现了矢量算法，geopandas是shapely与pandas的结合，可以方便的带着属性进行几何运算，实现类似arcgis里的图形关系运算。
5. pyproj：著名的地图投影项目，提供各种地理坐标系转换。



## geonumpy API 文档

**[GeoArray: 带投影的数组](doc/markdown.md)**

1. [geoarray](doc/markdown.md#MarkDown-Demo)
2. [frombox](doc/markdown.md#MarkDown-Demo)

**[io: 数据读取与存储](doc/macros.md#Macros)**

1. [read_shp](doc/macros.md#高斯模糊再求反)
2. [write_shp](doc/macros.md#分割硬币)
3. [read_tif ]()
4. [read_hdf]()
5. [write_tif]()
6. [write_hdf(未实现)]()
7. [read_tif_info ]()
8. [read_hdf_info]()
9. [read_raster]()
10. [read_raster_info]()

**[util: 几个辅助函数](doc/workflow.md)**

1. [shp2box]()
2. [box2shp]()

**[match: 配准与拼接](doc/workflow.md)**

1. [match_one]()
2. [match_multi]()
3. [build_index]()
4. [match_idx]()

**[draw: 地图绘制](doc/workflow.md)**

1. [draw_polygon]()

2. [draw_line]()

3. [draw_text]()

4. [draw_lab]()

5. [draw_unit]()

6. [draw_N]()

7. [draw_bound]()

8. [draw_ruler]()

9. [draw_style]()

**[draw: 地图绘制](doc/workflow.md)**

1. [大气校正(未实现)]()
2. [degap]()

**[draw: 地图绘制](doc/workflow.md)**

1. [ndvi]()

2. what should be added here! any issue is welcom!

   

## geonumpy 用户手册

**[GeoArray: 带投影的数组](doc/markdown.md)**

1. [地理图像的要素](doc/markdown.md#MarkDown-Demo)
2. [运算保持类型](doc/markdown.md#MarkDown-Demo)
3. [切片自动处理投影矩阵](doc/markdown.md#MarkDown-Demo)
4. [生成方法]()

**[io: 数据读取与存储](doc/macros.md#Macros)**

1. [矢量数据的输入输出](doc/macros.md#高斯模糊再求反)
2. [Tif与Hdf数据的输入输出](doc/macros.md#分割硬币)
3. [读取指定通道]()
4. [只读取图像的信息]()

**[match: 配准与拼接](doc/workflow.md)**

1. [单图的拼接]()

2. [多图的拼接]()

3. [通过矢量索引拼接]()

4. [单图投影转换]()

**[draw: 地图绘制](doc/workflow.md)**

1. [示例1：山东省地图绘制]()
2. [示例2：根据面积分等]()
3. [示例1：用遥感图作为底图]()

**[pretreat: 预处理](doc/workflow.md)**

1. [landsat level7 degap]()

**[indicate: 常用指标](doc/workflow.md)**

1. [count ndvi]()



