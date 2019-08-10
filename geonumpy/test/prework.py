from pygis.io import *
from pygis.util import *
import numpy as np
from time import time
from skimage.io import imsave
from scipy.ndimage import binary_dilation
from PIL import Image, ImageDraw, ImageFont
from shapely.geometry import Polygon
import os.path as osp
from glob import glob

def raster_bound_index(root):
    fs = glob(root+'/*.tif')
    boxes, csr = [], {}
    for i in fs:
        print('build', i, '...')
        rs = gdal.Open(i)
        csr = rs.GetProjection()
        m = rs.GetGeoTransform()
        m = np.array(m).reshape((2,3))
        shp = (rs.RasterYSize, rs.RasterXSize)
        boxes.append([raster_box(shp, csr, m), i])
    gdf = gpd.GeoDataFrame(boxes, columns=['geometry', 'path'])
    gdf.crs = makeprj(csr).ExportToProj4()
    return gdf

def group_merge(shape, name, size, raspath, outpath):
    idx = read_shp(raspath+'/idx.shp')
    idx = idx.to_crs(shape.crs)
    
    print(idx['geometry'])
    print(areas[name].unique().shape)
    s = 0
    for province in areas[name].unique():
        print(province)
        s += 1
        print(s)
        prv = areas[areas[name]==province]
        bounds = shp_box(prv, size[0]/size[1])
        des = shp2raster(prv, size, 0.1, 255, 1, np.uint8)
        box = raster_box(des[0].shape, des[1], des[2])
        des[0][:] = 0
        print('end')
        for i in idx.index:
            if box.intersects(idx.loc[i]['geometry']):
                raster = read_tif(raspath+'/'+idx.loc[i]['path'])[0]
                print('merge')
                raster2des(raster, des, 10)
                print('end')
        write_tif(des, outpath + '/%s.tif'%province)

if __name__ == '__main__':
    rs = raster_bound_index('../data/class')
    idx = read_shp('../data/class/idx.shp')
    areas = read_shp('../data/shape/xinjiang.shp')
    '''
    print(rs.crs)
    areas = read_shp('../data/shape/buchong.shp')
    
    areas = read_shp('../data/shape/xinjiang.shp')
    
    des = shp2raster(areas, (1024,768), 0.1, 255, 0)
    print(des[1])
    group_merge(areas, 'longname', (3508, 2480), '../data/class', '../data/out')
    # (9921, 6378) 省图
    '''
