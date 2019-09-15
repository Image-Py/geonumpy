import geonumpy.io as gio
import numpy as np
import geonumpy as gnp
import geonumpy.match as gmt
from glob import glob
import geonumpy.util as gutil
import geonumpy.draw as gdraw
import matplotlib.pyplot as plt
import geopandas as gpd

def all_source():
    fs = glob('../data/modis/*.hdf')
    ax1 = plt.subplot(131)
    ax1.imshow(gio.read_hdf(fs[0], 0))
    ax2 = plt.subplot(132)
    ax2.imshow(gio.read_hdf(fs[1], 0))
    ax3 = plt.subplot(133)
    ax3.imshow(gio.read_hdf(fs[2], 0))
    plt.show()
    
def match_one_test():
    shandong = gio.read_shp('../data/shape/shandong.shp')
    shandong = shandong.to_crs(3857)
    info = gutil.shp2box(shandong, (2048,1536), 0.05)
    #paper = gnp.frombox(*info, dtype=np.int16)
    path = '../data/modis/MOD09Q1.A2019017.h27v05.006.2019030120430.hdf'
    raster = gio.read_hdf(path)
    print(raster.shape)
    rst = gmt.match_one(raster, info, 0)
    print(rst.shape)
    plt.imshow(rst)
    plt.show()

def match_multi_test():
    shandong = gio.read_shp('../data/shape/shandong.shp')
    shandong = shandong.to_crs(3857)
    info = gutil.shp2box(shandong, (2048,1536), 0.05)
    fs = glob('../data/modis/*.hdf')
    rasters = [gio.read_hdf(i, 0) for i in fs]
    rst = gmt.match_multi(rasters, info, 0)
    plt.imshow(rst)
    plt.show()

def build_idx_test():
    fs = glob('../data/modis/*.hdf')
    idx = gmt.build_index(fs)
    idx.plot()
    plt.show()

def match_idx_test():
    shandong = gio.read_shp('../data/shape/shandong.shp')
    shandong = shandong.to_crs(3857)
    info = gutil.shp2box(shandong, (2048,768*2), 0.05)
    
    fs = glob('../data/modis/*.hdf')
    idx = gmt.build_index(fs)
    
    rst = gmt.match_idx(idx, info, chan=[0])
    plt.imshow(rst)
    plt.show()

def crs_trans_test():
    path = '../data/modis/MOD09Q1.A2019017.h27v05.006.2019030120430.hdf'
    raster = gio.read_hdf(path, 0)
    outshp = gutil.box2shp(*raster.getbox()).to_crs(3857)
    box = gutil.shp2box(outshp, 1000, 0)
    paper = gnp.frombox(*box, dtype=np.int16)
    gmt.match_one(raster, out=paper)

    plt.imshow(paper)
    plt.show()
    
if __name__ == '__main__':
    all_source()
    match_one_test()
    match_multi_test()
    
    build_idx_test()
    
    match_idx_test()
    
    crs_trans_test()
