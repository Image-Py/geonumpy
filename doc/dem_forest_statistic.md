# 综合应用：森林覆盖率统计

这里我们用一个综合性的例子串联 geonumpy 的各种使用方法，当然这其中离不开 numpy，scipy，pandas 等经典科学计算库的支持。



## 引入依赖

```python
import geonumpy as gnp
import geonumpy.io as gio
import geonumpy.util as gutil
import geonumpy.draw as gdraw
import geonumpy.match as gmt
import numpy as np
import scipy.ndimage as ndimg
import matplotlib.pyplot as plt
from PIL import Image
from glob import glob
```



## 用地类型拼接

```python
def match_class(df):
    shandong = df.to_crs(3857)
    box = gutil.shp2box(shandong, (3600, 2400), 0.15, 1)
    paper = gnp.frombox(*box, dtype=np.uint8)
    idx = gmt.build_index(glob('../data/class/*.tif'))
    gmt.match_idx(idx, paper, out='in', order=0)
    gio.write_tif(paper, '../data/result/shandong_class.tif')
```

![](imgs/13.png)

由于用地类型拼接是比较耗时的工作，因而我们将拼接结果保存下来。



## 市级行政区标记

```python
def city_label(df):
    shandong = df.to_crs(3857)
    box = gutil.shp2box(shandong, (3600, 2400), 0.15, 1)
    paper = gnp.frombox(*box, dtype=np.uint8)
    # 这里我们使用顺序递增的序号当作颜色依次绘制每个城市，得到标记图层
    gdraw.draw_polygon(paper, shandong, np.arange(len(shandong))+1, 0)
    gio.write_tif(paper, '../data/result/shandong_label.tif')
```

![](imgs/14.png)

这里我们用同样的尺寸绘制标记图像，我们采用多边形绘制，但颜色传入的是一个 arange 序号，同样，我们将标记结果存储，以便后续使用。



## 用地类型及标记展示

```python
def show_class_label(cls, lab):
    ax1, ax2 = plt.subplot(121), plt.subplot(122)
    ax1.imshow(cls)
    ax2.imshow(lab)
    ax1.set_title('shandong class')
    ax2.set_title('shandong label')
    plt.show()
```

![](imgs/12.png)

读取两张图，并绘制出来。



## 各个城市森林覆盖率计算

```python
def statistic(cls, lab, df):
    # 用lab作为标记，对cls==2的森林做求和统计
    forest = ndimg.sum(cls==2, lab, np.arange(lab.max())+1)
    # 像素统计，得到每个城市的面积
    total = np.bincount(lab.ravel())[1:]
    # 将城市面积，森林面积，森林覆盖率赋值到df
    df['area'] = total
    df['forest'] = forest
    df['ratio'] = forest/total
    return df

>>> name    area   forest     ratio
0   济南市  101390  11575.0  0.114163
1   青岛市  140587   6844.0  0.048682
2   淄博市   75245  12162.0  0.161632
3   枣庄市   55496   4718.0  0.085015
4   东营市   93881     80.0  0.000852
5   烟台市  179707  19820.0  0.110291
6   潍坊市  203411  11056.0  0.054353
7   济宁市  138547   3371.0  0.024331
8   泰安市   98093   8124.0  0.082819
9   威海市   73943   9339.0  0.126300
10  日照市   66440   4800.0  0.072246
11  莱芜市   28966   4380.0  0.151212
12  临沂市  214153  15699.0  0.073307
13  德州市  134892    654.0  0.004848
14  聊城市  110581    485.0  0.004386
15  滨州市  119506   1250.0  0.010460
16  菏泽市  150702    874.0  0.005800
```


## 绘制森林覆盖率专题图

```python
def draw_ratio(cls, lab, df):
    shandong = df.to_crs(3857)
    paper = cls.copy()
    paper[lab==0] = 12
    # 地类的色彩索引
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
                    [20 ,255,73 ],
                    [255,255,255]], dtype=np.uint8)
	# 地类的图例名称
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
    
    # 为了视觉效果，我们将地类假彩色映射减淡处理
    lut[1:-2] = lut[1:-2] * 0.6 + 255 * 0.4

    # 构造一个列，作为标注，我们用森林覆盖率的百分数形式
    shandong['lab'] = shandong['ratio'].apply(lambda x:'%.2f%%'%(x*100))
    gdraw.draw_lab(paper, shandong, 'lab', 0, ('simhei', 32), 'ct')
    
    # 绘制图例
    gdraw.draw_style(paper, 60, -60, body, mar=(20, 30),
        recsize=(120,60,0), font=('simsun', 60, 0), color=0, box=0)
    
    # 底图，位置，内容，空隙，矩形尺寸及线宽，字体字号颜色，外边框宽度
    gdraw.draw_unit(paper, -120, -60, 0.3, 30, ('times', 48), 0, 'km', 3, anc='r')
    gdraw.draw_text(paper, '山东省森林覆盖率统计', 80, 60, 0, ('simkai', 128))
    gdraw.draw_N(paper, -240, 240, ('simhei', 100), 2, 100, 0)
    gdraw.draw_polygon(paper, shandong, 0, 2)
    # 将覆盖率超过10%的城市用绿色描边
    gdraw.draw_polygon(paper, shandong[shandong['ratio']>0.1], 11, 8)
    gdraw.draw_bound(paper, 5, 5, -5, -5, 0, 2, clear=None)
    # 进行假彩色映射
    return paper.lookup(lut)
```

![](imgs/15.png)

最后我们绘制森林覆盖率统计结果的专题图。