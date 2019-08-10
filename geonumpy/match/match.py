import gdal, osr, pyproj
import geopandas as gpd
from glob import glob
import numpy as np
from numpy.linalg import inv
from .. import util as gutil
from .. import io as gio
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
    
def match_one(raster, des, step=10, out='auto', order=1):
    if out != 'in' or raster.channels() != des.channels():
        if out == 'auto': out = raster.dtype
        shape = (des.shape[:2] + (raster.channels(),))[:raster.ndim]
        des = GeoArray(np.zeros(shape, dtype=out), des.crs, des.mat)
    imgd, prjd, md = des, des.crs, des.mat
    if out != 'in': imgd = np.zeros(imgd.shape, dtype=out)
    img, prjs, ms = raster, raster.crs, raster.mat
    hs, ws = img.shape
    xx = np.linspace(0,ws-1,100).reshape((-1,1))*[1,0]
    yy = np.linspace(0,hs-1,100).reshape((-1,1))*[0,1]
    xy = np.vstack((xx, xx+[0,hs-1], yy, yy+[ws-1,0]))
    xy = mp2pm(xy, ms, prjs, prjd, md)#.astype(np.int)
    
    (left, top), (right, bot) = xy.min(axis=0)-1, xy.max(axis=0)+1
    left, right = np.clip((left, right), -1, imgd.shape[1])
    top, bot = np.clip((top, bot), -1, imgd.shape[0])
    hb, wb = bot-top, right-left
    nh, nw = int(hb//step+1), int(wb//step+1)
    xy = np.mgrid[top:bot:nh*1j, left:right:nw*1j].reshape((2,-1)).T
    xs, ys = mp2pm(xy[:,::-1], md, prjd, prjs, ms).T

    xs.shape = ys.shape = (nh, nw)#block.shape

    intleft, intright = max(0, ceil(left)), min(imgd.shape[1]-1, floor(right))
    inttop, intbot = max(0, ceil(top)), min(imgd.shape[0]-1, floor(bot))
    rc = np.mgrid[inttop:intbot+1, intleft:intright+1].reshape((2,-1))
    frc = rc.astype(np.float32)
    frc[0] = (frc[0]-top)/(bot-top)*(nh-1)
    frc[1] = (frc[1]-left)/(right-left)*(nw-1)
    xs = map_coordinates(xs, frc, cval=-100, order=1)
    ys = map_coordinates(ys, frc, cval=-100, order=1)
    for i in range(img.channels()):
        rcs, dcs = img.channels(i), imgd.channels(i)
        rcs = np.pad(rcs, 1, 'edge')
        vs = map_coordinates(rcs, np.array([ys, xs])+1, order=order)#prefilter=False)
        dcs[tuple(rc)] = np.max((dcs[tuple(rc)], vs), axis=0)   
    return imgd

def match_multi(rasters, des, step=10, out='auto', order=1):
    if out != 'in' or rasters[0].channels() != des.channels():
        if out == 'auto': out = rasters[0].dtype
        shape = (des.shape[:2] + (rasters[0].channels(),))[:rasters[0].ndim]
        des = GeoArray(np.zeros(shape, dtype=out), des.crs, des.mat)
    for raster in rasters: match_one(raster, des, step, 'in', order)
    return des

def build_index(fs):
    boxes, bcrs = [], None
    for i in range(len(fs)):
        shp, crs, m, chans = gio.read_raster_info(fs[i])
        if bcrs is None: bcrs = crs
        box = gutil.box2shp(shp, crs, m, chans).to_crs(bcrs)
        boxes.append([box[0], shp, m, chans, fs[i]])
    columns = ['geometry', 'shape', 'mat', 'channels', 'path']
    return gpd.GeoDataFrame(boxes, columns=columns, crs=bcrs)

def match_idx(idx, des, step=10, out='auto', order=1, chan=None):
    channels = len(idx['channels'][0]) if chan is None else len(chan)
    shape, crs, mat, chans = des.shape[:2], des.crs, des.mat, des.channels()
    if out != 'in' or channels != des.channels(): des = None
    idx = idx.to_crs(gutil.makeprj(crs).to_proj4())
    box = gutil.box2shp(shape, crs, mat, chans)[0]
    for i in idx.index:
        if box.intersects(idx.loc[i]['geometry']):
            print(chan)
            raster = gio.read_raster(idx.loc[i]['path'], chan)
            if des is None:
                shape = (shape[:2] + (channels,))[:2+(channels>1)]
                if out=='auto': out = raster.dtype
                des = GeoArray(np.zeros(shape, dtype=out), crs, mat)
            print('merge ...', idx.loc[i]['path'], end=' ')
            match_one(raster, des, step, 'in', order)
            print('end')
    return des
        
if __name__ == '__main__':
    wkt = 'PROJCS["China_Lambert_Conformal_Conic",GEOGCS["GCS_Beijing_1954",DATUM["Beijing_1954",SPHEROID["Krassowsky_1940",6378245,298.3,AUTHORITY["EPSG","7024"]],AUTHORITY["EPSG","6214"]],PRIMEM["Greenwich",0],UNIT["degree",0.0174532925199433]],PROJECTION["Lambert_Conformal_Conic_2SP"],PARAMETER["standard_parallel_1",30],PARAMETER["standard_parallel_2",62],PARAMETER["latitude_of_origin",0],PARAMETER["central_meridian",105],PARAMETER["false_easting",0],PARAMETER["false_northing",0],UNIT["metre",1,AUTHORITY["EPSG","9001"]]]'
    wktesri = open('全国县界行政区划2010_project.prj').read()
    from pygis.draw import make_paper
    idx = build_index('../data/class')
    
    china = read_shp('./全国县界行政区划2010_project.shp')
    paper = make_paper(china[china['Province']=='河南省'], (1024,768))
    paper = (paper[0], wkt, paper[2])
    match_idx(paper, idx)
