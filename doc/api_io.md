# geonumpy.io

地理数据的读取，支持shapefile，tif，hdf



### read_shp

------

此函数重命名了geopandas.read_file

read_shp(path, encoding='utf-8')

**path:** 文件路径

**encoding:** 属性表字符集

**return:** GeoDataFrame 对象



### write_shp

---

此函数重命名了geopandas.to_file

write_shp(shp, path, encoding='utf-8')

**shp:** GeoDataFrame 对象

**path:** 存储目录

**encoding:** 属性表字符集



### read_tif

---

read_tif(path, chans=None)

**path:** 文件路径

**chans:** 读取的通道，None表示所有通道

**return:** GeoArray 对象，2维或3维，取决于通道



### read_hdf

------

read_hdf(path, chans=None)

所有参数意义同 read_hdf



### read_raster

------

read_raster(path, chans=None)

通过path自动判断，然后调用 read_tif 或 read_hdf



### read_tif_info

------

read_tif_info(path,)

**path:** 文件路径

**return:** 图像基础信息，(shape, crs, mat, chans)



### read_hdf_info

------

read_hdf_info(path)

所有参数意义同 read_tif_info



### read_raster_info

------

read_hdf_info(path)

通过path自动判断，然后调用 read_tif_info 或 read_hdf_info



### write_tif

---

write_tif(raster, path)

**raster:** 要写入的 GeoArray 对象

**path:** 写入地址



### write_hdf

------

write_hdf(raster, path)

所有参数意义同 write_tif



### write_raster

------

write_raster(raster, path)

通过path自动判断 write_tif 或 write_hdf