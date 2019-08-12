# GeoArray

GeoArray 是地理图像处理的基础，继承于ndarray，携带坐标系与投影矩阵。



## 创建 GeoArray 对象

```python
import geonumpy as gnp
import numpy as np

mat = np.array([[0,1,0],[0,0,1]])
garr = gnp.geoarray(np.ones((5,5)), crs=4326, mat=mat)

print(garr.crs)
>>> 4326

print(garr.mat)
>>> [[0 1 0]
     [0 0 1]]
```
创建 GeoArray 对象时，需要传递一个2-3D的ndarray对象，同时指定参考系crs，以及投影矩阵mat。

* crs可以是egpn码，如同这里 4326 代表 wgs1984 投影，也可以是 wkt 字符串

* mat 是投影矩阵，指明像素坐标到投影坐标的转换关系，其中左边一列是平移项，右边 2x2 是旋转缩放。

  

## GeoArray 的运算

```python
garr2 = garr+1

print(garr2.crs)
>>> 4326

print(garr2.mat)
>>> [[0 1 0]
     [0 0 1]]
```

GeoArray 对象在进行运算，例如 +, -, *, /，或 np.sin, np.log 的时候，结果会自动保持 crs 与 mat。



## GeoArray 的切片

```python
garr3 = garr[1::2,1::2]

print(garr3.crs)
>>> 4326

print(garr3.mat)
>>> [[1 2 0]
     [1 0 2]]
```

GeoArray 在进行数组切片的时候，会自动转换 mat，这里我们从1，1点开始切片，间隔 2，所以结果左边列变成了 1，1，而右侧原本单位矩阵，扩大了两倍。



## 获取 box 及从 box 创建

```python
box = garr.getbox()
print(box)
>>> ((5, 5), 
     4326, 
     array([[0, 1, 0],
            [0, 0, 1]]), 
     1)

garr4 = gnp.frombox(*box, dtype=np.uint8)
print(garr4.crs)
>>> 4326

print(garr4.mat)
>>> [[1 2 0]
     [1 0 2]]
```

Box 可以理解为 GeoArray 的基础信息，是 (尺寸，参考，投影矩阵，通道数) 的元组。我们可以用 getbox 获取当前 GeoArray 的基础信息，也可以用 gnp.frombox 从边界信息构造 GeoArray 对象，但是注意，dtype 不属于空间信息，因而 gnp.frombox 需要传入一个 dtype 参数，默认为 np.uint8。



## 多通道处理

```python
garr_mc = gnp.geoarray(np.ones((5,5,3)), crs=4326, mat=mat)
>>> garr_mc.channels()
3
>>> garr_mc.channels(0)
GeoArray([[1., 1., 1., 1., 1.],
          [1., 1., 1., 1., 1.],
          [1., 1., 1., 1., 1.],
          [1., 1., 1., 1., 1.],
          [1., 1., 1., 1., 1.]])
```

GeoArray 对象通过 channels() 方法可以获取通道数，而channels(n) 表示获取第 n 个通道的切片。