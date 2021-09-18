import geopandas as pd
from .. import io as gio
from .. import util as gutil
from .. import geoarray

import numpy as np
from shapely.geometry import Polygon, GeometryCollection
from imageio import imread, imsave

max_lon = 85.0511287798
max_dis = 20037508.343

def build_grid_idx(level=0):
    n = 2**level
    rcs = np.mgrid[0:n,0:n].reshape(2,-1)
    rgs = np.mgrid[-max_dis:max_dis:(n+1)*1j,
                   max_dis:-max_dis:(n+1)*1j]
    p1, p2 = rgs[:,:-1,:-1], rgs[:,:-1,1:]
    p3, p4 = rgs[:,1:,1:], rgs[:,1:,:-1]
    pts = np.array([p1, p2, p3, p4])
    plgs = pts.reshape(4,2,-1).transpose(2,0,1)
    plgs = [Polygon(i) for i in plgs]
    data = {'geometry':plgs, 'x':rcs[0], 'y':rcs[1]}
    zs = np.ones(len(plgs), dtype=np.uint8)
    data['z'] = zs * level
    return pd.GeoDataFrame(data, crs=3857)

def build_geo_tif(img, crs, box):
    h, w = img.shape[:2]
    mat = [[box[0], (box[2]-box[0])/(w-1), 0],
           [box[3], 0, -(box[3]-box[1])/(h-1)]]
    return geoarray(img, crs=crs, mat=np.array(mat))

def build_online_tiles(level=3, box=None):
    if not box is None:
        shp = gutil.box2shp(*box).to_crs(3857)[0]
    if level is None and not box is None:
        a,b,c,d = shp.bounds
        l = ((c-a)**2 + (d-b)**2)**0.5
        s = (box[0][0]**2 + box[0][1]**2)**0.5
        rg = max_dis*2 / 256 / 2 ** np.arange(13)
        k = max(l/s, rg[-1]+1e-3)
        level = np.argmax(rg <= k)
    ts = build_grid_idx(level)
    if not box is None: ts = ts[ts.intersects(shp)]
    return ts

urls = {'arcgis blue':'https://map.geoq.cn/ArcGIS/rest/services/ChinaOnlineCommunity/MapServer/tile/{z}/{y}/{x}',
        'arcgis gray':'https://map.geoq.cn/ArcGIS/rest/services/ChinaOnlineStreetGray/MapServer/tile/{z}/{y}/{x}',
        'arcgis dark':'https://map.geoq.cn/ArcGIS/rest/services/ChinaOnlineStreetPurplishBlue/MapServer/tile/{z}/{y}/{x}',
        'gaode':'https://webst01.is.autonavi.com/appmaptile?style=6&x={x}&y={y}&z={z}',
        'google':'http://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}'}

def download_online_tiles(tiles, path, src='gaode'):
    for i,g,x,y,z in tiles[['geometry','x','y','z']].to_records():
        img = imread(urls[src].format(x=x, y=y, z=z))
        img = build_geo_tif(img, 3857, g.bounds)
        gio.write_tif(img, '%s/%ld_%d_%d.tif'%(path,z,y,x))

if __name__ == '__main__':
    import geonumpy.draw as gdraw
    import geonumpy.match as gmt
    import geonumpy.io as gio

    from glob import glob

    box = gio.read_tif_box('./3.背景TIF.tif')
    buf = gnp.frombox(*box[:3], 3)

    tiles = build_online_tiles(level=7, box=box[:3])
    download_online_tiles(tiles, './tiles', 'gaode')

    idx = gmt.build_index(glob('./tiles/*.tif'))
    rst = gmt.match_idx(idx, box[:3])
    gio.write_tif(rst, 'b.tif')

