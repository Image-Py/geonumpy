from geonumpy.base import GeoArray
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
    box = gutil.shp2box(shandong, (3600, 2400), 0.1, 1)
    paper = GeoArray.from_box(*box, dtype=np.uint8)
    paper[:] = 255
    gdraw.draw_polygon(paper, shandong, 0, 2)
    gdraw.draw_ruler(paper, 80, 50, -80, -50, 1, 4326, ('times', 32), 0, 2, 5)
    gdraw.draw_lab(paper, shandong, 'name', 0, ('simhei', 32), 'ct')
    gdraw.draw_unit(paper, -180, -100, 0.3, 30, ('times', 48), 0, 'km', 3, anc='r')
    gdraw.draw_text(paper, '山东省', (180, 120), 0, ('simkai', 128))
    gdraw.draw_N(paper, -240, 240, ('simhei', 100), 2, 100, 0)
    return paper

def draw_grade():
    shandong = gio.read_shp('../data/shape/shandong.shp')
    shandong = shandong.to_crs(3857)
    box = gutil.shp2box(shandong, (3600, 2400), 0.1, 1)
    paper = GeoArray.from_box(*box, dtype=np.uint8)
    
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
    gdraw.draw_text(paper, '山东省', (180, 120), 4, ('simkai', 128))
    gdraw.draw_N(paper, -240, 240, ('simhei', 100), 2, 100, 4)

    body = [('图例', 'simhei', 72),
            ('rect', 1,  '特大城市'),
            ('rect', 2,  '中型城市'),
            ('rect', 3,  '一般城市')]
    # 底图，位置，内容，空隙，矩形尺寸及线宽，字体字号颜色，外边框宽度
    gdraw.draw_style(paper, 150, -90, body, mar=(20, 30),
        recsize=(120,60,2), font=('simsun', 60, 4), box=0)
    
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
    box = gutil.shp2box(liaoning, (3600, 2400), 0.15, 1)
    paper = GeoArray.from_box(*box, dtype=np.uint8)

    # ===== match the class tif into paper
    fs = glob('../data/class/*.tif')
    idx = gmt.build_index(fs)
    gmt.match_idx(idx, paper, out='in', order=0)

    msk = paper * 0
    gdraw.draw_polygon(msk, liaoning, 255, 0)
    paper[msk==0] = 11

    body = [('图例', 'simhei', 72),
            ('rect', 1,  'water'),
            ('rect', 2,  'water'),
            ('rect', 3,  'water'),
            ('rect', 4,  'water'),
            ('rect', 5,  'water'),
            ('rect', 6,  'water'),
            ('rect', 7,  'water'),
            ('rect', 8,  'water'),
            ('rect', 9,  'water'),
            ('rect', 10, 'water')]
    # 底图，位置，内容，空隙，矩形尺寸及线宽，字体字号颜色，外边框宽度
    gdraw.draw_style(paper, 60, -60, body, mar=(20, 30),
        recsize=(120,60,0), font=('times', 60, 0), box=0)

    gdraw.draw_unit(paper, -120, -60, 0.3, 30, ('times', 48), 0, 'km', 3, anc='r')

    gdraw.draw_text(paper, '山东土地利用类型', (80, 60), 0, ('simkai', 128))

    gdraw.draw_N(paper, -240, 240, ('simhei', 100), 2, 100, 0)

    gdraw.draw_polygon(paper, liaoning, 0, 2)
    
    gdraw.draw_bound(paper, 5, 5, -5, -5, 0, 2, clear=None)
        
    return paper.lookup(lut)
    
    
if __name__ == '__main__':
    #rst = draw_simple()
    rst = draw_grade()
    #rst = draw_class()
    
    #gdraw.draw_ruler(paper, 30, 30, -30, -30, 1, 4326, ('times', 32), 0, 2, 5)

    
    Image.fromarray(rst).show()
