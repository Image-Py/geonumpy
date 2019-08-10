# pygis 地理数据工具包

pygis的编写目的是提供一套开源，易用，高效的地理数据处理库。包括矢量数据，图像数据的读取与处理。



## pygis的几个重要依赖

1. Numpy：作为科学计算库，自然离不开numpy

2. pandas, scipy, scikit-image，这几个常用库为我们提供了表格与图像处理功能

3. gdal，fiona：gdal是一套功能强大的地理数据处理库，可以读取矢量，图像数据，但功能相对比较底层，代码不够pythonic，而fiona是基于gdal的更方便的数据读取库。

4. shapely，geopandas：shapely是python的计算几何库，实现了矢量算法，geopandas是shapely与pandas的结合，可以方便的带着属性进行几何运算，实现类似arcgis里的图形关系运算。

   

