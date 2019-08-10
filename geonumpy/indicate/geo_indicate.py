import numpy as np

def count_ndvi(raster1, raster2):
    b1 = np.clip(raster1[0], 1, 1e8)
    b2 = np.clip(raster2[0], 1, 1e8)
    ndvi = (((b2-b1)/(b2+b1)+1)/2*255+0.5).astype(np.uint8)
    return (ndvi, raster1[1], raster1[2])