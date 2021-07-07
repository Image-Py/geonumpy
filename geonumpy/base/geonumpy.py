import numpy as np
from numpy.linalg import inv

class GeoArray(np.ndarray):
    def __new__(cls, input_array, crs=4326, mat=None):
        obj = np.asarray(input_array).view(cls)
        obj.crs, obj.mat = crs, mat.reshape((2,3))
        return obj
    
    def __array_finalize__(self, obj):
        if obj is None: return
        self.crs = getattr(obj, 'crs', '')
        self.mat = getattr(obj, 'mat', None)
    
    def __getitem__(self, item):
        sliced = True & isinstance(item, tuple)
        if sliced:
            sliced &= len(item) in (2, 3)
            sliced &= isinstance(item[1], slice)
            sliced &= isinstance(item[0], slice)
        def gs(s): return (s.start or 0, s.step or 1)
        if sliced:
            (s1,d1), (s2,d2) = gs(item[0]), gs(item[1])
            obj = super(GeoArray, self).__getitem__(item)
            if not obj.mat is None:
                m, offset = obj.mat[:,1:], obj.mat[:,:1]
                o = np.dot(m, [[s2],[s1]]) + offset
                t = m * [d2, d1]
                obj.mat = np.hstack((o,t))
            return obj
        if not sliced:
            return super().__getitem__(item).__array__()

    def __array_wrap__(self, out_arr, context=None):
        if out_arr.shape[:2] != self.shape[:2]:
            out_arr = out_arr.__array__()
        return out_arr

    @property
    def imat(self):
        imat = np.vstack((self.mat[:,[1,2,0]], [[0,0,1]]))
        return np.linalg.inv(imat)[:2,[2,0,1]]

    @property
    def imat1(self): return self.imat.ravel()[[1,2,4,5,0,3]]

    def project(self, x, y):
        m, offset = self.mat[:,1:], self.mat[:,:1]
        xy = np.array([x, y]).reshape((2,-1))
        return np.dot(m, xy) + offset

    def invpro(self, e, n):
        m, offset = self.mat[:,1:], self.mat[:,:1]
        en = np.array([e, n]).reshape((2,-1))
        return np.dot(inv(m), en - offset)

    def channels(self, n=None):
        if n is None:
            return 1 if self.ndim==2 else self.shape[2]
        else:
            return self if self.ndim==2 else self[:,:,n]

    def lookup(self, lut):
        return GeoArray(lut[self], self.crs, self.mat)

    def getbox(self): 
        return (self.shape[:2], self.crs, self.mat)


def frombox(shp, crs, mat, chan=1, dtype=np.uint8):
    if chan>1: shp += (chan,)
    return GeoArray(np.zeros(shp, dtype=dtype), crs, mat)

def geoarray(arr, crs=None, mat=np.array([[1,1,0],[1,0,1]])):
    return GeoArray(arr, crs, mat)

        
if __name__ == '__main__':
    prj = np.array([0,1,0, 0,0,1])
    a = GeoArray(np.ones((5,5)), crs=4326, mat=prj)
    print(a.crs)
    print(a.mat)
    b = a+1
    print(a.crs)
    print(a.mat)
    c = a[1::2,1::2]
    print(c.crs)
    print(c.mat)
