from osgeo import gdal, osr
import pyproj
import geopandas as gpd
from glob import glob
import numpy as np
from numpy.linalg import inv
import geonumpy as gnp
import geonumpy.util as gutil
import geonumpy.io as gio
from math import ceil, floor
from scipy.ndimage import map_coordinates

def mp2pm(boxs, m1, prj1, prj2, m2, t1 = lambda x:x, t2 = lambda x:x):
    p1 = osr.SpatialReference()
    p1.ImportFromProj4(pyproj.CRS(prj1).to_proj4())
    p2 = osr.SpatialReference()
    p2.ImportFromProj4(pyproj.CRS(prj2).to_proj4())
    box = t1(np.dot(m1[:,1:], np.array(boxs).T) + m1[:,:1])
    ct = osr.CoordinateTransformation(p1, p2)
    box = t2(np.array(ct.TransformPoints(box.T)).T)
    return np.dot(inv(m2[:,1:]), box[:2]-m2[:,:1]).T
    '''
    prj1 = pyproj.CRS(wkt1)
    prj2 = pyproj.CRS(wkt2)
    ct = pyproj.Transformer.from_crs(prj1, prj2)
    print(ct.transform(116, 39))
    '''
    
def match_one(raster, out, chan='all', step=10, order=1):
    if chan=='all': chan = list(range(raster.channels()))
    if isinstance(chan, int): chan = [chan]
    if isinstance(out, tuple):
        out = gnp.frombox(*out, len(chan), raster.dtype)
    imgd, prjd, md = out, out.crs, out.mat
    img, prjs, ms = raster, raster.crs, raster.mat
    hs, ws = img.shape[:2]
    xx = np.linspace(0,ws,100).reshape((-1,1))*[1,0]
    yy = np.linspace(0,hs,100).reshape((-1,1))*[0,1]
    xy = np.vstack((xx, xx+[0,hs], yy, yy+[ws,0]))
    xy = mp2pm(xy, ms, prjs, prjd, md)#.astype(np.int)
    
    (left, top), (right, bot) = xy.min(axis=0), xy.max(axis=0)
    left, right = np.clip((left, right), 0, imgd.shape[1])
    top, bot = np.clip((top, bot), 0, imgd.shape[0])
    hb, wb = bot-top, right-left # 像素数目
    nh, nw = int(hb//step+1), int(wb//step+1)
    xy = np.mgrid[top:bot:nh*1j, left:right:nw*1j].reshape((2,-1)).T

    xs, ys = mp2pm(xy[:,::-1], md, prjd, prjs, ms).T

    xs.shape = ys.shape = (nh, nw)#block.shape

    intleft, intright = floor(left), ceil(right)
    inttop, intbot = floor(top), ceil(bot)
    rc = np.mgrid[inttop:intbot, intleft:intright].reshape((2,-1))
    frc = rc.astype(np.float32) + 0.5
    frc[0] = (frc[0]-top)/(bot-top)*(nh-1)
    frc[1] = (frc[1]-left)/(right-left)*(nw-1)
    xs = map_coordinates(xs, frc, order=1)
    ys = map_coordinates(ys, frc, order=1)
    for i in chan:
        #range(img.channels()):
        rcs, dcs = img.channels(i), imgd.channels(i)
        vs = map_coordinates(rcs, np.array([ys, xs])-0.5, order=order)#prefilter=False)
        vs[np.isnan(vs)] = 0
        dcs[tuple(rc)] = np.maximum(dcs[tuple(rc)], vs)   
    return imgd

def match_multi(rasters, out, chan='all', step=10, order=1):
    if chan=='all': chan = list(range(rasters[0].channels()))
    if isinstance(chan, int): chan = [chan]
    if isinstance(out, tuple):
        out = gnp.frombox(*out, len(chan), rasters[0].dtype)
    for raster in rasters: match_one(raster, out, chan, step, order)
    return out

def build_index(fs):
    boxes, bcrs = [], None
    for i in fs:
        isfile = isinstance(i, str)
        if isfile: shp, crs, m, chans = gio.read_raster_box(i)
        else: (shp, crs, m), chans = i.getbox(), i.channels()
        if bcrs is None: bcrs = crs
        box = gutil.box2shp(shp, crs, m).to_crs(bcrs)
        boxes.append([box[0], shp, m, chans, ['memory', i][isfile]])
    columns = ['geometry', 'shape', 'mat', 'channels', 'path']
    return gpd.GeoDataFrame(boxes, columns=columns, crs=bcrs)

def match_idx(idx, out, chan='all', step=10, order=1):
    if chan=='all': chan = list(range(len(idx['channels'][0])))
    if isinstance(chan, int): chan = [chan]
    if isinstance(out, tuple): shape, crs, mat = out
    else: shape, crs, mat = out.shape, out.crs, out.mat
    idx = idx.to_crs(gutil.makecrs(crs).to_proj4())
    box = gutil.box2shp(shape, crs, mat)[0]
    for i in idx.index:
        if box.intersects(idx.loc[i]['geometry']):
            print(chan)
            raster = gio.read_raster(idx.loc[i]['path'], chan)
            if isinstance(out, tuple):
                out = gnp.frombox(*out, len(chan), raster.dtype)
            print('merge ...', idx.loc[i]['path'], end=' ')
            match_one(raster, out, chan, step, order)
            print('end')
    return out
    
if __name__ == '__main__':
    wkt = 'PROJCS["China_Lambert_Conformal_Conic",GEOGCS["GCS_Beijing_1954",DATUM["Beijing_1954",SPHEROID["Krassowsky_1940",6378245,298.3,AUTHORITY["EPSG","7024"]],AUTHORITY["EPSG","6214"]],PRIMEM["Greenwich",0],UNIT["degree",0.0174532925199433]],PROJECTION["Lambert_Conformal_Conic_2SP"],PARAMETER["standard_parallel_1",30],PARAMETER["standard_parallel_2",62],PARAMETER["latitude_of_origin",0],PARAMETER["central_meridian",105],PARAMETER["false_easting",0],PARAMETER["false_northing",0],UNIT["metre",1,AUTHORITY["EPSG","9001"]]]'
    wktesri = open('全国县界行政区划2010_project.prj').read()
    from pygis.draw import make_paper
    idx = build_index('../data/class')
    
    china = read_shp('./全国县界行政区划2010_project.shp')
    paper = make_paper(china[china['Province']=='河南省'], (1024,768))
    paper = (paper[0], wkt, paper[2])
    match_idx(paper, idx)
