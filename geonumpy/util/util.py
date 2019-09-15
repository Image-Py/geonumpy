from shapely.geometry import GeometryCollection
from shapely.geometry import Polygon
import geopandas as gpd
import pyproj, numpy as np

def makecrs(prj): return pyproj.CRS(prj)

def shp2box(shape, scale, margin=0.05):
    if isinstance(shape, gpd.GeoDataFrame):
        shape = shape['geometry']
    shapes = shape.values
    kmargin = margin/(1-2*margin)
    geoms = list(shape.values)
    bounds = GeometryCollection(geoms).bounds
    l,t,r,b = bounds
    w,h = r-l, b-t
    if isinstance(scale, tuple):
        ox, oy = (l+r)/2, (t+b)/2
        W, H = np.array(scale) * (1-margin*2)
        scale = max(w/W, h/H)
        if w/h > W/H: h = w/W*H
        else: w = h/H*W
        l, t, r, b = (ox-w/2, oy-h/2, ox+w/2, oy+h/2)
    offsetx, offsety = l-w*kmargin, b+h*kmargin
    shp = np.array((h,w))*(1+(kmargin*2))/scale
    shp = (tuple(shp.round().astype(np.int)))
    m = np.array([offsetx, scale, 0, offsety, 0, -scale]).reshape((2,3))
    return (shp, shape.crs, m)

def box2shp(shape, crs, m):
    hs, ws = shape[:2]
    xx = np.linspace(0,ws,100).reshape((-1,1))*[1,0]
    yy = np.linspace(0,hs,100).reshape((-1,1))*[0,1]
    xy = np.vstack((xx, yy+[ws+1,0], xx[::-1]+[0,hs+1],yy[::-1]))
    xy = np.dot(m[:,1:], xy.T) + m[:,:1]
    return gpd.GeoSeries([Polygon(xy.T)], crs=pyproj.CRS(crs).to_proj4())

def shp_bounds(shape):
    bds = shape.bounds
    return [bds['minx'].min(), bds['miny'].min(), 
            bds['maxx'].max(), bds['maxy'].max()]

def box_boundx(shape, crs, m):
    return shp_bounds(box2shp(shape, crs, m))

if __name__ == '__main__':
    shp = read_shp('../../tasks/country_china_wheat_2018/region.shp')
    from time import time
    start = time()
    raster = shp2raster(shp, 250, 0, style='lab')
    print(time()-start)
    plt.imshow(raster.imgs[0])
    plt.show()