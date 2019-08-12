import geonumpy as gnp
import numpy as np

if __name__ == '__main__':
    mat = np.array([[0,1,0],[0,0,1]])
    garr = gnp.geoarray(np.ones((5,5)), crs=4326, mat=mat)
    print(garr.crs)
    print(garr.mat)
    
    garr2 = garr+1
    print(garr2.crs)
    print(garr2.mat)
    
    garr3 = garr[1::2,1::2]
    print(garr3.crs)
    print(garr3.mat)

    box = garr.getbox()
    print(box)

    garr4 = gnp.frombox(*box, dtype=np.uint8)
    print(garr4.getbox())

    garr_mc = gnp.geoarray(np.ones((5,5,3)), crs=4326, mat=mat)
    print(garr_mc.crs)
    print(garr_mc.mat)
    
