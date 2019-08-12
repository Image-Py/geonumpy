# geonumpy
geonumpy 是一个 GIS，遥感影像处理库，实现了矢量，遥感影像读取，存储，预处理，拼接，重采样，常规指标计算，地图绘制等功能。



### 安装

依赖库：numpy，scipy, matplotlib, pandas

地理依赖库：gdal, fiona, shapely, geopandas

几个地理依赖库不太好装，请参阅 geopandas 官网，有详细的安装方法。

geonumpy 暂时没有上传pypi, 请下载后使用 pip install -e 命令加入PythonPath




### 文档
[**geonumpy 文档**]()

1. [geonumpy api 文档](doc/index.md#geonumpy-API-文档)
2. [geonumpy 用户手册](doc/index.md#geonumpy-用户手册)



## 功能简介

这里简单介绍 geonumpy 的部分功能，可以让读者快速有一个认识，更多，具体功能，请参阅文档。



### 影像读取

```python
path = '../data/landsat/LC08_L1TP_122033_20190506_20190506_01_RT_B5.TIF'
landsat = gio.read_tif(path)

# landsat is a GeoArray object which subclass the numpy.ndarray
>>> landsat.shape
(7821, 7691)

# but with crs
>>> landsat.crs   
4326

# and transform matrix
>>> landsat.mat  
array([[ 4.556850e+05,  3.000000e+01,  0.000000e+00],
       [ 4.423215e+06,  0.000000e+00, -3.000000e+01]])

plt.imshow(landsat, cmap='gray')
plt.show()
```

![landsat](./geonumpy/doc/imgs/02.png)



### 去条带

```python
path = '../data/landsat-gap/LE07_L1TP_123037_20180721_20180816_01_T1_sr_ndvi.tif'
img = gio.read_tif(path)
# 去条带, img==-999 是掩膜，-999为无效值
degapimg = gpt.degap(img.copy(), img==-9999, 10)

# plot two images ...
```
![](./geonumpy/doc/imgs/16.png)



### 影像拼接

![](./geonumpy/doc/imgs/06.png)

```python
# 读取山东省 shapefile
shandong = gio.read_shp('../data/shape/shandong.shp')
# 转为 web 墨卡托 投影
shandong = shandong.to_crs(3857)
# 缩放到 2048*1536大小，边距0.05，计算相关空间信息
box = gutil.shp2box(shandong, (2048,1536), 0.05, 1)
# 用空间信息实例化 GeoArray 对象
paper = gnp.frombox(*box, dtype=np.int16)
# 读取所有影像的 0 通道
fs = glob('../data/modis/*.hdf')
rasters = [gio.read_hdf(i, 0) for i in fs]
# 将 rasters 投影到 paper
gmt.match_multi(rasters, paper, out='in')

plt.imshow(paper)
plt.show()
```

![](./geonumpy/doc/imgs/04.png)

这里我们使用一个 shapefile 转换到 web 墨卡托坐标系，并用矢量图形确定了图像空间信息，然后将图像块投影到目标图像上，从而实现拼接。



### 矢量图绘制

```python
import geonumpy.io as gio
import geonumpy.draw as gdraw

# 读取山东省矢量图
shandong = gio.read_shp('../data/shape/shandong.shp')
# 投影成 web 墨卡托
shandong = shandong.to_crs(3857)
# 从矢量图计算图像空间信息，尺寸3600*2400，边距十分之一
box = gutil.shp2box(shandong, (3600, 2400), 0.1, 1)
# 从空间信息实例化 GeoArray 对象
paper = gnp.frombox(*box, dtype=np.uint8)
# 底图赋值为白色
paper[:] = 255
# 绘制多边形，颜色为0，线条宽度为2
gdraw.draw_polygon(paper, shandong, 0, 2)
# 绘制刻度，左右80，上下50，单位间隔1，坐标系4326，使用times字体，32好，颜色0，线条宽度2，刻度高5
gdraw.draw_ruler(paper, 80, 50, -80, -50, 1, 4326, ('times', 32), 0, 2, 5)
# 绘制文字标签，用name字段，颜色0，黑体，32好，中心对齐
gdraw.draw_lab(paper, shandong, 'name', 0, ('simhei', 32), 'ct')
# 绘制比例尺，右侧180，底部100的位置，宽度占十分之三宽度，高度30，times字体，48号，颜色0，单位km，线条宽度3， 右对齐
gdraw.draw_unit(paper, -180, -100, 0.3, 30, ('times', 48), 0, 'km', 3, anc='r')
# 绘制标题文字，在180， 120的位置，颜色0，楷体，128号，绘制山东省
gdraw.draw_text(paper, '山东省', 180, 120, 0, ('simkai', 128))
# 在右上角240，240的位置，黑体，100号，线条宽度2，箭头中心线高度100，颜色0，绘制指北针
gdraw.draw_N(paper, -240, 240, ('simhei', 100), 2, 100, 0)

from PIL import Image
Image.formarray(paper).show()
```

![](./geonumpy/doc/imgs/08.png)

geonumpy 提供了为地图定制的一套绘图函数，可以方便的绘制比例尺，指北针，图例等元素。



## 更多功能

geopandas 还在开发过程中，更多功能请查阅文档，也欢迎提交 issue 或贡献代码。