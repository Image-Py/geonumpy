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

def match_class(df):
    shandong = df.to_crs(3857)
    box = gutil.shp2box(shandong, (3600, 2400), 0.15, 1)
    paper = gnp.frombox(*box, dtype=np.uint8)
    idx = gmt.build_index(glob('../data/class/*.tif'))
    gmt.match_idx(idx, paper, out='in', order=0)
    gio.write_tif(paper, '../data/result/shandong_class.tif')

def city_label(df):
    shandong = df.to_crs(3857)
    box = gutil.shp2box(shandong, (3600, 2400), 0.15, 1)
    paper = gnp.frombox(*box, dtype=np.uint8)
    gdraw.draw_polygon(paper, shandong, np.arange(len(shandong))+1, 0)
    gio.write_tif(paper, '../data/result/shandong_label.tif')

def show_class_label(cls, lab):
    ax1, ax2 = plt.subplot(121), plt.subplot(122)
    ax1.imshow(cls)
    ax2.imshow(lab)
    ax1.set_title('shandong class')
    ax2.set_title('shandong label')
    plt.show()

def statistic(cls, lab, df):
    forest = ndimg.sum(cls==2, lab, np.arange(lab.max())+1)
    total = np.bincount(lab.ravel())[1:]
    df['area'] = total
    df['forest'] = forest
    df['ratio'] = forest/total
    return df

def draw_ratio(cls, lab, df):
    shandong = df.to_crs(3857)
    paper = cls.copy()
    paper[lab==0] = 12
    
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
                    [20 ,119,73 ],
                    [255,255,255]], dtype=np.uint8)

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
    
    lut[1:-2] = lut[1:-2] * 0.6 + 255 * 0.4

    shandong['lab'] = shandong['ratio'].apply(lambda x:'%.2f%%'%(x*100))
    gdraw.draw_polygon(paper, shandong, 0, 2)
    gdraw.draw_polygon(paper, shandong[shandong['ratio']>0.1], 11, 8)
    gdraw.draw_lab(paper, shandong, 'lab', 0, ('simhei', 48), 'ct')
    # 底图，位置，内容，空隙，矩形尺寸及线宽，字体字号颜色，外边框宽度
    gdraw.draw_style(paper, 60, -60, body, mar=(20, 30),
        recsize=(120,60,0), font=('simsun', 60, 0), color=0, box=0)
    
    gdraw.draw_unit(paper, -120, -60, 0.3, 30, ('times', 48), 0, 'km', 3, anc='r')
    gdraw.draw_text(paper, '山东省森林覆盖率统计', 80, 60, 0, ('simkai', 128))
    gdraw.draw_N(paper, -240, 240, ('simhei', 100), 2, 100, 0)
    gdraw.draw_bound(paper, 5, 5, -5, -5, 0, 2, clear=None)
    return paper.lookup(lut)

if __name__ == '__main__':
    shandong = gio.read_shp('../data/shape/shandong.shp')
    # match_class(shandong)
    # city_label(shandong)
    
    cls = gio.read_tif('../data/result/shandong_class.tif')
    lab = gio.read_tif('../data/result/shandong_label.tif')

    tab = statistic(cls, lab, shandong)
    print(tab[['name', 'area', 'forest', 'ratio']])

    rst = draw_ratio(cls, lab, shandong)

    Image.fromarray(rst).show()
    Image.fromarray(rst).save('../data/result/shandong_forest.png')
