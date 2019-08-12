# geonumpy.download

遥感影像获取是一切分析的前提，好在目前有一些开放的卫星，免费向大家提供下载服务，download 模块主要功能就是实现从各大开放网站上下载遥感影像数据。



## modis_search

search(product, level, areas, terms)

**product:** modis 的产品类型，例如['MOD09Q1', 'MOD11A2'], level=6, areas=['h25v05', 'h27v05', 'h28v05'], terms=[(2019, (0,30))]

**level:**  level=6，代表影像等级

**areas:** 要下载区域进行行列编号，例如 ['h25v05', 'h27v05', 'h28v05']

**terms:** 周期，[(2019, (0,30)), ...]，年份跟着变数，支持多个。

```python
files = search(['MOD09Q1', 'MOD11A2'], 
               level=6, 
               areas=['h25v05', 'h27v05', 'h28v05'], 
               terms=[(2019, (0,30))])

>>>
searching... MOD09Q1 level 6 2019
	001 day ... done
	009 day ... done
	017 day ... done
	025 day ... done

searching... MOD11A2 level 6 2019
	001 day ... done
	009 day ... done
	017 day ... done
	025 day ... done

24 new files found!
```



## modis_download

modis_download(files, des):

**files:** 上一步search到的结果，要下载的文件名

**des:** 存储目录

```python
files = search(['MOD09Q1', 'MOD11A2'], level=6, areas=['h25v05', 'h27v05', 'h28v05'], terms=[(2019, (0,30))])

download(files, '')

>>> MOD09Q1.A2019001.h25v05.006.2019010205323.hdf ... 
```



## landsat_search

landsat_search(product, crs, start, end, month=None, lcloud='', scloud='', page=1)

**product:** 选项，7，8，45，表示不同代的产品

**crs:** 要下载的行列号序列

**start:** 要下载的开始时间

**end:** 要下载的结束时间

**month:** 下载的月份列表

**lcloud:** 陆地云量小于该值

**scloud:** 卫星影像云量小于该值

**pare:** 下载的页数，满页后不再改变

```python
records = get_record(7, blocks, '06/30/2018', '07/30/2019', None, 10, 10, 1)
>>>
searching 123 043, ...
1
searching 119 037, ...
3
searching 122 037, ...
6

>>>
LE07_L1TP_123043_20181126_20181222_01_T1
LE07_L1TP_119037_20190509_20190604_01_T1
LE07_L1TP_119037_20181029_20181124_01_T1
LE07_L1TP_119037_20181013_20181108_01_T1
LE07_L1TP_122037_20190701_20190727_01_T1
LE07_L1TP_122037_20190311_20190406_01_T1
LE07_L1TP_122037_20190122_20190217_01_T1
LE07_L1TP_122037_20181018_20181113_01_T1
LE07_L1TP_122037_20181002_20181030_01_T1
LE07_L1TP_122037_20180714_20180809_01_T1
```



# landsat_download

...