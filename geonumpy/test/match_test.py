import geonumpy.io as gio
import numpy as np
from geonumpy import GeoArray
import geonumpy.match as gmt
from glob import glob
import geonumpy.util as gutil
import geonumpy.draw as gdraw
import matplotlib.pyplot as plt
import geopandas as gpd

if __name__ == '__main__':
    sichuan = gio.read_shp('../data/shape/shandong.shp')
    sichuan = sichuan.to_crs(3857)
    
    fs = glob('../data/modis/all/*.hdf')
    idx = gmt.build_index(fs)
    info = gutil.shp2box(sichuan, (2048,768*2), 0.05, 1)
    paper = GeoArray.from_box(*info, dtype=np.int16)
    print(idx.columns)
    gmt.match_idx(idx, paper, out='in', chan=[0])
    #gdraw.draw_polygon(paper, sichuan, 1, 2)

    plt.imshow(paper)
    plt.show()

    box = gutil.box2shp(*paper.get_box())
    box = box.to_crs(3758)
    info = gutil.shp2box(box, (1024,768), 0, 1)
    npaper = GeoArray.from_box(*info, dtype=np.int16)
    gmt.match_one(paper, npaper, out='in')

    plt.imshow(npaper)
    plt.show()
    
    '''
    fs = glob('../data/modis/*.hdf')
    rasters = [gio.read_raster(i, 1) for i in fs]
    info = gutil.shp2info(sichuan, (1024,768), 0.05, 1)
    paper = GeoArray.from_info(*info, dtype=np.int16)
    gmt.match_multi(rasters, paper, out='in')
    gdraw.draw_polygon(paper, sichuan, 1, 2)

    plt.imshow(paper)
    plt.show()
    '''
