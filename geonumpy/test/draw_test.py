import geonumpy as gnp
import geonumpy.io as gio
import geonumpy.util as gutil
import geonumpy.draw as gdraw
import geonumpy.match as gmt
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from glob import glob
    
def draw_simple():
    shandong = gio.read_shp('../data/shape/shandong.shp')
    shandong = shandong.to_crs(3857)
    box = gutil.shp2box(shandong, (3600, 2400), 0.1)
    paper = gnp.frombox(*box, chan=1, dtype=np.uint8)
    paper[:] = 255
    gdraw.draw_polygon(paper, shandong, 0, 2)
    gdraw.draw_ruler(paper, 80, 50, -80, -50, 1, 4326, ('times', 32), 0, 2, 5)
    gdraw.draw_lab(paper, shandong, 'name', 0, ('simhei', 32), 'ct')
    gdraw.draw_unit(paper, -180, -100, 0.3, 30, ('times', 48), 0, 'km', 3, anc='r')
    gdraw.draw_text(paper, '山东省', 180, 120, 0, ('simkai', 128))
    gdraw.draw_N(paper, -240, 240, ('simhei', 100), 2, 100, 0)
    return paper

def draw_style():
    paper = gnp.geoarray(np.zeros((480,1024), dtype=np.uint8))

    body = [('Style', 'simhei', 72),
            ('blank',50),
            ('line', 1,  'this is line style'),
            ('circle', 2,  'this is circle style'),
            ('rect', 3,  'this is rect style')]

    lut = np.array([[255,255,255],
                    [255,0  ,0  ],
                    [0  ,255,0  ],
                    [0  ,0  ,255],
                    [0  ,0  ,0  ]], dtype=np.uint8)
    gdraw.draw_style(paper,128,-20, body, mar=(20, 30),
        recsize=(120,60,3), font=('simsun', 60), color=4, box=5)
    return paper.lookup(lut)

def draw_grade():
    shandong = gio.read_shp('../data/shape/shandong.shp')
    shandong = shandong.to_crs(3857)
    box = gutil.shp2box(shandong, (3600, 2400), 0.1)
    paper = gnp.frombox(*box, dtype=np.uint8)
    
    areas = shandong.area
    grade_lut = np.array([3]*60 + [2]*30 + [1]*10, dtype=np.uint8)
    vs = (areas-areas.min())/(areas.max()-areas.min())*99
    grade = grade_lut[vs.astype(int)]
    print(grade)
    
    gdraw.draw_polygon(paper, shandong, grade, 0)
    gdraw.draw_polygon(paper, shandong, 4, 2)
    
    gdraw.draw_ruler(paper, 80, 50, -80, -50, 1, 4326, ('times', 32), 4, 2, 5)
    gdraw.draw_lab(paper, shandong, 'name', 4, ('simhei', 32), 'ct')
    gdraw.draw_unit(paper, -180, -100, 0.3, 30, ('times', 48), 4, 'km', 3, anc='r')
    gdraw.draw_text(paper, '山东省', 180, 120, 4, ('simkai', 128))
    gdraw.draw_N(paper, -240, 240, ('simhei', 100), 2, 100, 4)

    body = [('图例', 'simhei', 72),
            ('rect', 1,  '特大城市'),
            ('rect', 2,  '中型城市'),
            ('rect', 3,  '一般城市')]
    # 底图，位置，内容，空隙，矩形尺寸及线宽，字体字号颜色，外边框宽度
    gdraw.draw_style(paper, 150, -90, body, mar=(20, 30),
        recsize=(120,60,2), font=('simsun', 60, 4), color=4, box=0)
    
    lut = np.array([[255,255,255],
                    [255,200,100],
                    [255,255,128],
                    [255,255,200],
                    [0  ,0  ,0  ]], dtype=np.uint8)
                    
    return paper.lookup(lut)

def draw_class():
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
    box = gutil.shp2box(liaoning, (3600, 2400), 0.15)
    paper = gnp.frombox(*box, dtype=np.uint8)

    # ===== match the class tif into paper
    fs = glob('../data/class/*.tif')
    idx = gmt.build_index(fs)
    gmt.match_idx(idx, out=paper, order=0)

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

    gdraw.draw_unit(paper, -120, -60, 0.3, 30, ('times', 48), 0, 'km', 3, anc='r')

    gdraw.draw_text(paper, '山东省土地利用类型', 80, 60, 0, ('simkai', 128))

    gdraw.draw_N(paper, -240, 240, ('msyh', 100), 2, 100, 0)

    gdraw.draw_polygon(paper, liaoning, 0, 2)
    
    gdraw.draw_bound(paper, 5, 5, -5, -5, 0, 2, clear=None)
        
    return paper.lookup(lut)
    
    
if __name__ == '__main__':
    
    rst = draw_simple()
    rst = draw_style()
    rst = draw_grade()
    rst = draw_class()
    
    Image.fromarray(rst).save('../doc/imgs/00.png')
    Image.fromarray(rst).show()
