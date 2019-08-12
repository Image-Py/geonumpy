# geonumpy.draw

地图绘制是成果的重要展现形式，虽然 matplotlib 内置了丰富的绘图函数，但是要绘制地图的比例尺，指北针等特定元素，依然不是一个简单工作，而 geonumpy 的 draw 模块，提供了定制化的地图绘制函数。



## 矢量图绘制

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

![](http://idoc.imagepy.org/gis/08.png)



## 图例的使用

```python
paper = gnp.geoarray(np.zeros((480,1024), dtype=np.uint8))

body = [('Style', 'simhei', 72),
        ('blank',50),
        ('line', 1,  'this is line style'),
        ('circle', 2,  'this is circle style'),
        ('rect', 3,  'this is rect style')]
# 色彩索引表
lut = np.array([[255,255,255],
                [255,0  ,0  ],
                [0  ,255,0  ],
                [0  ,0  ,255],
                [0  ,0  ,0  ]], dtype=np.uint8)

gdraw.draw_style(paper,128,-20, body, mar=(20, 30),
                 recsize=(120,60,3), font=('simsun', 60), color=4, box=5)
# 将色彩索引表套用在paper上
paper = paper.lookup(lut)

from PIL import Image
Image.formarray(paper).show()
```
![](http://idoc.imagepy.org/gis/09.png)



## 根据面积进行等级划分

```python
# 读取矢量文件及计算影像空间信息
shandong = gio.read_shp('../data/shape/shandong.shp')
shandong = shandong.to_crs(3857)
box = gutil.shp2box(shandong, (3600, 2400), 0.1, 1)
paper = gnp.frombox(*box, dtype=np.uint8)

# 取各个城市的面积
areas = shandong.area
# 制作一个长度为100的索引表，3级60个，2级30个，1级10个
grade_lut = np.array([3]*60 + [2]*30 + [1]*10, dtype=np.uint8)
# 将面积缩放到0-100
vs = (areas-areas.min())/(areas.max()-areas.min())*99
# 套用等级索引，为每个城市划分等级
grade = grade_lut[vs.astype(int)]
# 这里颜色传入一个序列，代表依次使用这些颜色绘制
gdraw.draw_polygon(paper, shandong, grade, 0)

# ===== 其他装饰信息 =====
gdraw.draw_polygon(paper, shandong, 4, 2)
gdraw.draw_ruler(paper, 80, 50, -80, -50, 1, 4326, ('times', 32), 4, 2, 5)
gdraw.draw_lab(paper, shandong, 'name', 4, ('simhei', 32), 'ct')
gdraw.draw_unit(paper, -180, -100, 0.3, 30, ('times', 48), 4, 'km', 3, anc='r')
gdraw.draw_text(paper, '山东省', 180, 120, 4, ('simkai', 128))
gdraw.draw_N(paper, -240, 240, ('simhei', 100), 2, 100, 4)

# ===== 图例绘制 =====
body = [('图例', 'simhei', 72),
        ('rect', 1,  '特大城市'),
        ('rect', 2,  '中型城市'),
        ('rect', 3,  '一般城市')]
# 底图，位置，内容，空隙，矩形尺寸及线宽，字体字号颜色，外边框宽度
gdraw.draw_style(paper, 150, -90, body, mar=(20, 30),
    recsize=(120,60,2), font=('simsun', 60, 4), color=4, box=0)

# ===== 色彩索引 =====
lut = np.array([[255,255,255],
                [255,200,100],
                [255,255,128],
                [255,255,200],
                [0  ,0  ,0  ]], dtype=np.uint8)

# ===== 套用假彩色 =====
paper = paper.lookup(lut)

from PIL import Image
Image.formarray(paper).show()
```

![](http://idoc.imagepy.org/gis/10.png)

这里我们使用一个技巧，取得每个城市的面积，然后为面积划分等级，用等级当作颜色进行多边形绘制，最后统一进行色彩映射。其实如果数据中带有等级之类的数值属性，我们也可以传入一个字符串当作颜色，函数会根据字符串查找对应的列当作颜色进行绘制。



## 土地利用类型图绘制

```python
# ===== look up table =====
lut = np.array([[0  ,0  ,0  ],
                [168,168,0  ],
                [20 ,119,73 ],
                [169,208,95 ],
                [56 ,168,0  ],
                [126,206,244],
                [0  ,86 ,154],
                [112,168,0  ],
                [147,47 ,20 ],
                [202,202,202],
                [0  ,255,197],
                [255,255,255]], dtype=np.uint8)

# ===== read shape file and make a paper =====
liaoning = gio.read_shp('../data/shape/shandong.shp')
liaoning = liaoning.to_crs(3857)
box = gutil.shp2box(liaoning, (3600, 2400), 0.15, 1)
paper = gnp.frombox(*box, dtype=np.uint8)

# ===== match the class tif into paper
fs = glob('../data/class/*.tif')
idx = gmt.build_index(fs)
gmt.match_idx(idx, paper, out='in', order=0)

# ===== draw polygon as mask =====
msk = paper * 0
gdraw.draw_polygon(msk, liaoning, 255, 0)
paper[msk==0] = 11

body = [('图例', 'simhei', 72),
        ('rect', 1,  '农田'),
        ('rect', 2,  '森林'),
        ('rect', 3,  '草地'),
        ('rect', 4,  '灌丛'),
        ('rect', 5,  '湿地'),
        ('rect', 6,  '水体'),
        ('rect', 7,  '苔原'),
        ('rect', 8,  '隔水层'),
        ('rect', 9,  '裸地'),
        ('rect', 10, '冰雪')]
# 底图，位置，内容，空隙，矩形尺寸及线宽，字体字号颜色，外边框宽度
gdraw.draw_style(paper, 60, -60, body, mar=(20, 30),
    recsize=(120,60,0), font=('simsun', 60, 0), color=0, box=0)

# ===== 其他装饰信息 =====
gdraw.draw_unit(paper, -120, -60, 0.3, 30, ('times', 48), 0, 'km', 3, anc='r')
gdraw.draw_text(paper, '山东省土地利用类型', 80, 60, 0, ('simkai', 128))
gdraw.draw_N(paper, -240, 240, ('simhei', 100), 2, 100, 0)
gdraw.draw_polygon(paper, liaoning, 0, 2)
gdraw.draw_bound(paper, 5, 5, -5, -5, 0, 2, clear=None)
    
# ===== 套用假彩色 =====
paper = paper.lookup(lut)

from PIL import Image
Image.formarray(paper).show()

```

![](http://idoc.imagepy.org/gis/11.png)

