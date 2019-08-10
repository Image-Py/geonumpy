import numpy as np

x_pi = np.pi * 3000.0 / 180.0
pi = 3.1415926535897932384626  # π
a = 6378245.0  # 长半轴
ee = 0.00669342162296594323  # 扁率

def wgs84togcj02(lnglat):
    lng, lat = lnglat.T[:2]
    if out_of_china(lng.mean(), lat.mean()):  # 判断是否在国内
        return lnglat
    dlat = transformlat(lng - 105.0, lat - 35.0)
    dlng = transformlng(lng - 105.0, lat - 35.0)
    radlat = lat / 180.0 * pi
    magic = np.sin(radlat)
    magic = 1 - ee * magic * magic
    sqrtmagic = np.sqrt(magic)
    dlat = (dlat * 180.0) / ((a * (1 - ee)) / (magic * sqrtmagic) * pi)
    dlng = (dlng * 180.0) / (a / sqrtmagic * np.cos(radlat) * pi)
    mglat = lat + dlat
    mglng = lng + dlng
    return np.array([mglng, mglat]).T


def gcj02towgs84(lnglat):
    lng, lat = lnglat.T[:2]
    if out_of_china(lng.mean(), lat.mean()): return lnglat
    dlat = transformlat(lng - 105.0, lat - 35.0)
    dlng = transformlng(lng - 105.0, lat - 35.0)
    radlat = lat / 180.0 * pi
    magic = np.sin(radlat)
    magic = 1 - ee * magic * magic
    sqrtmagic = np.sqrt(magic)
    dlat = (dlat * 180.0) / ((a * (1 - ee)) / (magic * sqrtmagic) * pi)
    dlng = (dlng * 180.0) / (a / sqrtmagic * np.cos(radlat) * pi)
    mglat = lat + dlat
    mglng = lng + dlng
    return np.array([lng * 2 - mglng, lat * 2 - mglat]).T


def transformlat(lng, lat):
    ret = -100.0 + 2.0 * lng + 3.0 * lat + 0.2 * lat * lat + \
        0.1 * lng * lat + 0.2 * np.sqrt(np.abs(lng))
    ret += (20.0 * np.sin(6.0 * lng * pi) + 20.0 *
            np.sin(2.0 * lng * pi)) * 2.0 / 3.0
    ret += (20.0 * np.sin(lat * pi) + 40.0 *
            np.sin(lat / 3.0 * pi)) * 2.0 / 3.0
    ret += (160.0 * np.sin(lat / 12.0 * pi) + 320 *
            np.sin(lat * pi / 30.0)) * 2.0 / 3.0
    return ret


def transformlng(lng, lat):
    ret = 300.0 + lng + 2.0 * lat + 0.1 * lng * lng + \
        0.1 * lng * lat + 0.1 * np.sqrt(np.abs(lng))
    ret += (20.0 * np.sin(6.0 * lng * pi) + 20.0 *
            np.sin(2.0 * lng * pi)) * 2.0 / 3.0
    ret += (20.0 * np.sin(lng * pi) + 40.0 *
            np.sin(lng / 3.0 * pi)) * 2.0 / 3.0
    ret += (150.0 * np.sin(lng / 12.0 * pi) + 300.0 *
            np.sin(lng / 30.0 * pi)) * 2.0 / 3.0
    return ret

def out_of_china(lng, lat):
    msk = (lng > 72.004) & (lng < 137.8347)
    msk &= (lat > 0.8293) & (lat < 55.8271)
    return not msk

def lat2y(lat):
    rad = np.clip(lat, -85.0511287798, 85.0511287798) * np.pi / 180
    return np.log(np.tan(np.pi / 4 + rad / 2)) / np.pi * 180

def y2lat(y):
    return (np.arctan(np.exp(y / 180 * np.pi)) - np.pi / 4) * 2 / np.pi * 180

def gaode_adjust(xy):
    return np.array([xy[:,0], lat2y(xy[:,1])]).T

def gaode_adjust_(xy):
    return np.array([xy[:,0], y2lat(xy[:,1])]).T

def wgs2gaode(xy):
    return gaode_adjust(wgs84togcj02(xy))

def gaode2wgs(xy):
    return gcj02towgs84(gaode_adjust_(xy))

if __name__ == '__main__':
    lng, lat = 120, 35
    lnglat = np.array([[120, 35],[120,35]])
    rst = wgs84togcj02(lnglat)
