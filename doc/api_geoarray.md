# GeoArray

GeoArray 是地理图像处理的基础，继承于ndarray，携带坐标系与投影矩阵。



### Class GeoArray

---

GeoArray(array， crs=None, mat=np.array([[1,1,0],[1,0,1]])

>> **array:** image data, 2D-3D
>>
>> **crs:** egps code or wkt string
>>
>> **mat:** matrix from pixel coordinate to crs point

> >**channels(self, n=None):** 获取指定通道，不传参返回通道数
> >
> >**project(self, r, c):** 行列投影到crs坐标系
> >
> >**invpro(self, r, c):** crs坐标系获取对应行列
> >
> >**lookup(self, lut):** 套用假彩色
> >
> >**getbox(self):** 获取 (shape, crs, mat, channels)



```python
gimg = GeoArray(np.zeros(100,100, dtype=np.uint8), 4326)
print(gimg.crs)
print(gimg.mat)
```



### geoarray

---

geoarray(arr, crs=None, mat=np.array([[1,1,0],[1,0,1]]))

**array:** image data, 2d-3d

**crs:** egps code or wkt string

**mat:** matrix for pixel coordinate to crs



**return:** GeoArray object with the given data

```python
import geonumpy as gnp
gnp.geoarray(np.zeros(100,100, dtype=np.uint8), 4326)
```



### frombox

---

frombox(shp, crs=None, mat, chan=1, dtype=np.uint8):

**shp:** image shape

**crs:** egps code or wkt string

**mat:** matrix for pixel coordinate to crs

**chan:** number of channels

**dtype:** data's type



**return:** GeoArray object with the given data

```python
import geonumpy as gnp
gnp.frombox((100,100), 4326, np.array([[1,1,0],[1,0,1]]),1)
```

