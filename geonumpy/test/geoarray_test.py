from geonumpy import GeoArray
import numpy as np

if __name__ == '__main__':
    prj = np.array([[0,1,0],[0,0,1]])
    a = GeoArray(np.ones((5,5)), crs=4326, mat=prj)
    print(a.crs)
    print(a.mat)
    b = a+1
    print(a.crs)
    print(a.mat)
    c = a[1::2,1::2]
    print(c.crs)
    print(c.mat)

    info = c.get_info()
    print(info)

    d = GeoArray.from_info(*info, dtype=np.uint8)
    print(d.get_info())
