import geonumpy.io as gio
import matplotlib.pyplot as plt


if __name__ == '__main__':
    gdf = gio.read_shp('../data/shape/shandong.shp')
    print(gdf)
    gdf.plot()
    plt.show()
    
    print('read modis hdf data:')
    modis = gio.read_hdf('../data/modis/MOD09Q1.A2019017.h28v05.006.2019030120612.hdf', 0)
    print(modis.shape, '\n', modis.crs, '\n', modis.mat)
    plt.imshow(modis, cmap='gray')
    plt.show()

    print('\nread landsat tif data:')
    landsat = gio.read_tif('../data/landsat/LC08_L1TP_122033_20190506_20190506_01_RT_B5.TIF')
    print(modis.shape, '\n', modis.crs, '\n', modis.mat)
    plt.imshow(landsat, cmap='gray')
    plt.show()

    print('\nsave modis as tif')
    gio.write_tif(modis, '../data/modis/MOD09Q1.A2019017.h25v05.006.2019030120448.tif')

    box = gio.read_tif_box('../data/landsat/LC08_L1TP_122033_20190506_20190506_01_RT_B5.TIF')
    print(box)
