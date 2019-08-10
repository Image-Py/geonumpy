from pygis.io import *
from pygis.util import *
from pygis.draw import *

import numpy as np
from time import time
from glob import glob
from skimage.io import imsave, imread
from scipy.ndimage import binary_dilation
from PIL import Image, ImageDraw, ImageFont
from skimage.segmentation import find_boundaries

cmap = np.zeros((255,3), dtype=np.uint8)
ydlx = np.array([[0, 0, 0],
                 [249,243,192],
                 [20,119,73],
                 [169,208,95],
                 [56,168,0],
                 [126,206,244],
                 [0,86,154],
                 [112,168,0],
                 [147,47,20],
                 [202,202,202],
                 [0,255,197]], dtype=np.uint8)
k = 0.7
cmap[1:11] = ydlx[1:]*k+255*(1-k)
cmap[100] = 255

cmappure = cmap.copy()
#cmappure = cmap[:11] = ydlx

def decorate(rgb, name, k, scale=3.8):
    f = lambda x : int(x * scale)
    font = ImageFont.truetype('simkai.ttf', f(80))
    img = Image.fromarray(rgb)
    d = ImageDraw.Draw(img)
    d.text((f(60),f(60)), name, font=font, fill=(0, 0, 0))
    # 边框
    d.rectangle([0,0,img.width-1,img.height-1], outline=(0,0,0), width=f(2))

    # 比例尺
    step = int(round(img.width*k/1000/30))
    if step>100:
        n = 10**len(str(step))/10
        step = int(np.round(step/n)*n)
    cell = int(step * 1000 / k)
    for s, e, c in zip((10,9,7,4), (9,7,4,0), (1,0,1,0)):
        d.rectangle([img.width-f(180)-s*cell, img.height-f(60), img.width-f(180)-e*cell, img.height-f(40)],
                    fill=[(0,0,0),None][c], outline=(0,0,0), width=f(2))
    font = ImageFont.truetype('msyh.ttc', f(44))
    for s in (10,9,7,4,0):
        d.text((img.width-f(180)-s*cell-f(10), img.height-f(120)),
               str(step*(10-s))+['',' km'][s==0], font=font, fill=(0,0,0))

    #img.show()
    return np.array(img)

def get_type(area, back):
    bounds = get_bounds(area, 9921/6378)
    outline = shp2raster(area, (9921, 6378), 0.15, 0, 0, np.uint8, bounds)
    ground = back[0]#rasters2des([back], outline)[0]
    ground[outline[0]==0] = 100
    return (cmap[ground], outline[1], outline[2])

def get_province(area, roi):
    bounds = get_bounds(area, 9921/6378)
    outline = shp2raster(area, (9921,6378), 0.15, 255, 1, np.uint8, bounds)
    roi.sort_values(by=['area'], axis=0, ascending=False, inplace=True)
    badarea = shp2raster(roi, (9921,6378), 0.15, 0, 0, np.uint32, bounds)
    # print(roi.shape, badarea[0].max())
    cidx = list(roi['color'].unique())
    cmap[20:20+len(cidx)] = cidx
    cidx = roi['color'].apply(lambda x:cidx.index(x)+20)
    hcq = np.hstack(((0,), cidx))[badarea[0]]
    ground = np.ones_like(outline[0]) * 100
    print(ground.shape, 'outshape')
    msk = hcq>0
    ground[msk] = hcq[msk]
    ground[binary_dilation(outline[0], np.ones((5,5)))] = 0
    return (cmap[ground], outline[1], outline[2])

def get_county(area, roi, ground):
    bounds = get_bounds(area, 3508/2480)
    outline = shp2raster(area, (3508, 2480), 0.15, 255, 1, np.uint8, bounds)
    roi = roi.sort_values(by=['area'], axis=0, ascending=False)
    roi.prj = area.prj
    badarea = shp2raster(roi, (3508, 2480), 0.15, 0, 0, np.uint32, bounds)

    cidx = list(roi['color'].unique())
    cmap[20:20+len(cidx)] = cidx
    cidx = roi['color'].apply(lambda x:cidx.index(x)+20)
    hcq = np.hstack(((0,), cidx))[badarea[0]]

    #ground = rasters2des([ground], outline)[0]
    msk = hcq>0
    ground[msk] = hcq[msk]
    ground[binary_dilation(outline[0], np.ones((5,5)))] = 0
    return Raster(cmap[ground], outline[1], outline[2])

def get_global(area, roi):
    global cmap
    bounds = get_bounds(area, 9921/6378)
    outline = shp2raster(area, (9921,6378), 0.05, 0, 0, np.uint32, bounds)
    ss = area['Province']
    idx = area['Province'].unique()
    idx = pd.Series(np.arange(len(idx))+1, idx)
    lut = np.hstack(((0,), idx.loc[areas['Province']].values))
    imgp = (lut.astype(np.uint8))[outline[0]]
    msk1 = find_boundaries(outline[0])
    msk2 = find_boundaries(imgp)
    roi.sort_values(by=['area'], axis=0, ascending=False, inplace=True)
    badarea = shp2raster(roi, (9921,6378), 0.05, 0, 0, np.uint32, bounds)

    cidx = list(roi['color'].unique())
    cmap[20:20+len(cidx)] = cidx
    cidx = roi['color'].apply(lambda x:cidx.index(x)+20)
    hcq = np.hstack(((0,), cidx))[badarea[0]]
    
    ground = np.ones_like(outline[0]) * 100
    msk = hcq>0
    
    ground[binary_dilation(msk1, np.ones((3,3)))] = 30
    cmap[30] = (200,200,200)
    ground[binary_dilation(msk2, np.ones((5,5)))] = 0
    ground[msk] = hcq[msk]
    return (cmap[ground], outline[1], outline[2])

def draw(ground, shp, color, width, dtype=np.uint8):

    outline = shp2raster(area, (3508, 2480), 0.15, 255, 1, np.uint8, bounds)
    roi = roi.sort_values(by=['area'], axis=0, ascending=False)
    roi.prj = area.prj
    badarea = shp2raster(roi, (3508, 2480), 0.15, 0, 0, np.uint32, bounds)

    cidx = list(roi['color'].unique())
    cmap[20:20+len(cidx)] = cidx
    cidx = roi['color'].apply(lambda x:cidx.index(x)+20)
    hcq = np.hstack(((0,), cidx))[badarea[0]]

    #ground = rasters2des([ground], outline)[0]
    msk = hcq>0
    ground[msk] = hcq[msk]
    ground[binary_dilation(outline[0], np.ones((5,5)))] = 0
    return Raster(cmap[ground], outline[1], outline[2])

if __name__ == '__main__':
    '''
    print('读取数据')
    areas = read_shp('shape/area.shp')
    rois = read_shp('shape/roi.shp')
    rois['color'] = rois['color'].apply(lambda x:eval(x))
    #rois = shape2prj(rois, areas.prj)
    print('准备就绪')
    '''
    '''
    # 全国
    rgb = get_global(areas, rois)
    rst = decorate(rgb[0], '中国蝗区分布', rgb[2].ravel()[1])
    imsave('result/province/%s.png'%'中国', rst)
    '''
    
    '''
    # 省蝗区图
    for prv in rois['Province'].unique():
        print(prv)
        prov = areas[areas['Province']==prv]
        prov.prj = areas.prj
        roiprov = rois[rois['Province']==prv]
        roiprov.prj = rois.prj
        roiprov = shape2prj(roiprov, areas.prj)
        rgb = get_province(prov, roiprov)
        rst = decorate(rgb[0], prv, rgb[2].ravel()[1])
        imsave('result/province/%s.png'%prv, rst)
        print('end')
    '''
    
    '''
    # 用地类型
    for prv in rois['Province'].unique():
        print(prv)
        imgclass = read_tif('provincecls/%s.tif'%prv)[0]
        prov = areas[areas['Province']==prv]
        prov.prj = areas.prj
        rgb = get_type(prov, imgclass)
        rst = decorate(rgb[0], '%s土地利用/覆盖遥感监测图'%prv, rgb[2].ravel()[1], 3.8)
        imsave('result/proclass/%s.png'%prv, rst)
        print('end')
    '''
    '''
    s = 0 #生成县图
    for longname in rois['longname'].unique():
        s += 1
        imgclass = read_tif('countycls/%s.tif'%longname)[0]
        print(s, longname)
        prv, city, name = longname.split('_')
        print('正在处理：%s'%longname, '...')
        roi = rois[rois['longname']==longname]
        roi.prj = rois.prj
        area = areas[areas['longname']==longname]
        area.prj = areas.prj
        rgb = get_county(area, roi, imgclass[0])
        rst = decorate(rgb.imgs, name, rgb.m.ravel()[1], 1.5)
        imsave('result/county/%s.png'%longname, rst)
    '''
    '''
    shape = read_shp('../data/shape/buchong.shp')
    for longname in shape['longname'].unique():
        shp = shape[shape['longname']==longname]
        raster = read_tif('../data/out/tif/%s.tif'%longname)[0]
        rgb = (cmap[raster[0]], raster[1], raster[2])
        shp_draw_raster(rgb, shp, (0,0,0), 7)
        rst = decorate(rgb[0], longname.split('_')[-1], rgb[2].ravel()[1], 1.5)
        imsave('../data/out/rgb/%s.png'%longname, rst)
    '''
    
    msk = imread('../data/mask.png')
    for i in glob('../data/out/rgb/*.png'):
        img = imread(i)
        draw_mask(img, msk)
        imsave(i.replace('rgb', 'msk'), img)
    
