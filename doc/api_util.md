# geonumpy.util

一些常用函数



### shp2box

------

shp2box(shape, scale, margin=0.05, chan=1)

**shape:** GeoDataFrame 对象，要计算边界的矢量数据

**scale:** 比例尺，有如下情况

* 浮点数或整数，使用给定比例尺生成box
* 二元tuple，按照指定尺寸的box，比例尺自动计算

**margin:** 边距，输入比例，0.05表示上下左右各留出5%空间

**chan:** 指定 box 的通道数

**return:** 图像基础信息，(shape, crs, mat, chans)



### box2shp

---

box2shp(shape, crs, mat, chans)

**shape:** GeoArray 对象的尺寸

**crs:** 坐标系

**mat:** 映射矩阵

**chans:** 通道数

**return:** 返回边界多边形，带着crs，构成一个 GeoSeries 对象