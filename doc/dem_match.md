# geonumpy.match

影像的重投影，拼接，采样是一个最普通的需求，match 模块提供这些功能。这里有必要说明一下match模块的设计思想，对于投影来说，总是需要两个 GeoArray 对象，一个source，一个image，match_one 函数可以实现把 source 映射到 image。而我们不总是拥有 image，所以 image 的产生有如下几种方式：

* 天然拥有，有些时候，我们可以得到要映射到的图像，拥有尺寸以及空间参考，那么直接使用。
* 通过 shapefile 产生，有些时候，我们有映射目标的矢量文件，那么读取矢量，并且使用 util.shp2box获取结果图像的空间信息，再用gnp.frombox实例化。
* 从source产生还有些时候，我们没有目标图像，也没有对应的矢量文件，那么我们需要通过source自动计算，具体方法是先计通过 util.box2shp 得到 source 的边界矢量，然后 to_crs 对边界矢量进行投影，再使用上面的方法获得 image。

对于拼接，geonumpy 是当作多图投影处理的，本质是将多张图投影到同一个目标图像上。



## 素材展示

```python
fs = glob('../data/modis/*.hdf')
ax1 = plt.subplot(131)
ax1.imshow(gio.read_hdf(fs[0], 0))
ax2 = plt.subplot(132)
ax2.imshow(gio.read_hdf(fs[1], 0))
ax3 = plt.subplot(133)
ax3.imshow(gio.read_hdf(fs[2], 0))
plt.show()
```

![](http://idoc.imagepy.org/gis/06.png)



## 单图投影

```python
import geonumpy.io as gio
import geonumpy.util as gutil
import geonumpy.match as gmt

# 读取山东省 shapefile
shandong = gio.read_shp('../data/shape/shandong.shp')
# 转为 web 墨卡托 投影
shandong = shandong.to_crs(3857)
# 缩放到 2048*1536大小，边距0.05，计算相关空间信息
box = gutil.shp2box(shandong, (2048,1536), 0.05, 1)
# 用空间信息实例化 GeoArray 对象
paper = gnp.frombox(*box, dtype=np.int16)
# 读取影像的 0 通道
path = '../data/modis/MOD09Q1.A2019017.h27v05.006.2019030120430.hdf'
raster = gio.read_hdf(path, 0)
# 将 raster 投影到 paper
gmt.match_one(raster, paper, out='in')

plt.imshow(paper)
plt.show()
```
![](http://idoc.imagepy.org/gis/03.png)

match_one 用于单图投影，out 默认为 auto, 表示返回与 raster 相同类型的结果，也可以为 dtype，指定返回结果类型，in 表示 在 des 上进行投影。 

**gutil.shp2box(shandong, (2048,1536), 0.05, 1)** 其中第二个参数是图像尺寸或比例尺，如果输入tuple，则指定最终尺寸，比例尺自动计算，如输入数字，则作为比例尺，尺寸自动计算。

## 多图投影

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

![](http://idoc.imagepy.org/gis/04.png)

与单图类似，这里读取一个 GeoArray 的序列，用 match_multi 进行投影，而 out 使用 in，重复投影点，函数会以最大值为准，因而我们得到了完整的拼接结果。



## 创建空间索引 build_idx

```python
fs = glob('../data/modis/*.hdf')
idx = gmt.build_index(fs)

>>> idx.columns
Index(['geometry', 'shape', 'mat', 'channels', 'path'], dtype='object')

idx.plot()
plt.show()
```

![landsat](http://idoc.imagepy.org/gis/05.png)

这里调用 io.read_raster_info 读取每个影像的空间信息，创建对应的多边形矢量，而不直接读取像素，而这个空间索引却包含了影像所处的位置信息，投影信息，以及对应的文件路径。遥感影像通常很大，我们无法一次性全部读取到内存，因而这个空间索引就有重要的作用。



## 通过索引批量匹配 match_idx

```python
# 读取山东省 shapefile
shandong = gio.read_shp('../data/shape/shandong.shp')
# 转为 web 墨卡托 投影
shandong = shandong.to_crs(3857)
# 缩放到 2048*1536大小，边距0.05，计算相关空间信息
box = gutil.shp2box(shandong, (2048,1536), 0.05, 1)
# 用空间信息实例化 GeoArray 对象
paper = gnp.frombox(*box, dtype=np.int16)
# 创建空间索引
fs = glob('../data/modis/*.hdf')
idx = gmt.build_index(fs)
# 根据索引将 rasters 投影到 paper
gmt.match_idx(idx, paper, out='in', chan=[0])

plt.imshow(paper)
plt.show()
```

![](http://idoc.imagepy.org/gis/04.png)

通过 match_idx 我们也拼接得到了同样的结果，与 match_multi 非常类似，但是有几点不同，match_idx 可以通过空间索引，自动查找相关的地块，在需要的时候读取，并及时释放。对于遥感数据，计算机很难将全部图像载入内存，即便载入，也需要判断需要投影的块，而使用 idx 空间索引，就可以很好解决以上问题。



## 单图投影转换

```python
# 读取图像
path = '../data/modis/MOD09Q1.A2019017.h27v05.006.2019030120430.hdf'
raster = gio.read_hdf(path, 0)
# 获取图像的边界多边形，并转换到 web 墨卡托投影
outshp = gutil.box2shp(*raster.getbox()).to_crs(3857)
# 通过边界多边形，以 1：1000 计算图像空间信息
box = gutil.shp2box(outshp, 1000, 0, 1)
# 根据空间信息创建图像
paper = gnp.frombox(*box, dtype=np.int16)
# 将 rasters 投影到 paper
gmt.match_one(raster, paper, out='in')

plt.imshow(paper)
plt.show()
```

![](http://idoc.imagepy.org/gis/07.png)