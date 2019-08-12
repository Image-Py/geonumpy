# geonumpy.match

坐标系转换，拼接，重采样是遥感影像中常见的问题



### mp2pm

------

mp2pm(pts, m1, prj1, prj2, m2）

**pts:** 要投影的点，ndarray n*2

**mat1, crs1:** 第一张图的投影矩阵及坐标系

**crs2, mat2:** 第二张图的坐标系及投影矩阵

**return: ** 投射后的结果，ndarray n*2



### match_one

---

match_one(raster, des, step=10, out='auto', order=1)

**raster:** 被投射图像，GeoArray对象

**des:** 投射目标，GeoArray对象

**step:** 真实采样间距，只有这些点真实计算投射位置，剩下的用双线性插值获得，注意并非是色彩的插值，而是对投射位置的插值，所以只要不是很大，对结果影响很小，但性能会增加许多。

**out:** 输出参数，具体如下

* dtype: 例如 np.uint8, np.int16，指明输出类型
* auto：投影成与 raster 相同的类型
* in: 结果投影到 des，当des的维度或数据类型与raster不同的时候，则退化为auto

**order:** 插值方式，0表示最邻近，1表示双线性

**return:** 返回投影后的图像



### match_multi

---

match_multi(rasters, des, step=10, out='auto', order=1)

**rasters:** 被投射图像，GeoArray 的 list

**des:** 投射目标，GeoArray对象

**step:** 真实采样间距，只有这些点真实计算投射位置，剩下的用双线性插值获得，注意并非是色彩的插值，而是对投射位置的插值，所以只要不是很大，对结果影响很小，但性能会增加许多。

**out:** 输出参数，具体如下

- dtype: 例如 np.uint8, np.int16，指明输出类型
- auto：投影成与 raster 相同的类型
- in: 结果投影到 des，当des的维度或数据类型与raster不同的时候，则退化为auto

**order:** 插值方式，0表示最邻近，1表示双线性

**return:** 返回投影后的图像



### build_index

---

build_index(fs)

**fs:** 文件路径列表，函数为每个文件建立基础信息及空间索引关系。

**return:** 根据文件路径创建一个GeoDataFrame对象，列如下：['geometry', 'shape', 'mat', 'channels', 'path']，里面存有图像边界矢量对象，图像尺寸，图像投影矩阵，通道列表，以及文件目录。



### match_idx

---

match_idx(idx, des, step=10, out='auto', order=1, chan=None)

类似于 match_multi, 但文件并不事先加载，而是在通过索引确定需要的块，然后及时读取，用完及时释放。

**idx:** 文件集索引，通常是build_index的结果，用于快速判断有交集的块，只在需要时候读取。

**des:** 投射目标，GeoArray对象

**step:** 真实采样间距，只有这些点真实计算投射位置，剩下的用双线性插值获得，注意并非是色彩的插值，而是对投射位置的插值，所以只要不是很大，对结果影响很小，但性能会增加许多。

**out:** 输出参数，具体如下

- dtype: 例如 np.uint8, np.int16，指明输出类型
- auto：投影成与 raster 相

**chan:** 要投影的通道列表，None表示所有通道