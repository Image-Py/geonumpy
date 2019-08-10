from skimage.io import imread, imsave
import matplotlib.pyplot as plt
from glob import glob
import numpy as np

'''
# 省图添加标记
msk = imread('msk/省蝗虫发生等级.png')
imgs = glob('result/province/*.png')
for i in imgs:
    print(i)
    img = imread(i)
    weight = msk[:,:,3]/255
    np.multiply(img.T, 1-weight.T, out=img.T, casting='unsafe')
    np.add(img.T, msk[:,:,:3].T*weight.T, out=img.T, casting='unsafe')
    imsave(i.replace('province', 'province-msk'), img)
'''
'''
# 省利用类型添加标记
msk = imread('msk/省_土地利用.png')
imgs = glob('result/proclass/*.png')
for i in imgs:
    print(i)
    img = imread(i)
    weight = msk[:,:,3]/255
    np.multiply(img.T, 1-weight.T, out=img.T, casting='unsafe')
    np.add(img.T, msk[:,:,:3].T*weight.T, out=img.T, casting='unsafe')
    imsave(i.replace('proclass', 'proclass-msk'), img)
'''
'''
# 县添加标记
msk = imread('msk/县蝗虫发生等级.png')
imgs = glob('result/county/*.png')
for i in imgs:
    print(i)
    img = imread(i)
    weight = msk[:,:,3]/255
    np.multiply(img.T, 1-weight.T, out=img.T, casting='unsafe')
    np.add(img.T, msk[:,:,:3].T*weight.T, out=img.T, casting='unsafe')
    imsave(i.replace('county', 'county-msk'), img)
'''
msk = imread('msk/县土地利用-1.png')
imgs = glob('result/xinjiang/*.png')
for i in imgs:
    print(i)
    img = imread(i)
    weight = msk[:,:,3]/255
    np.multiply(img.T, 1-weight.T, out=img.T, casting='unsafe')
    np.add(img.T, msk[:,:,:3].T*weight.T, out=img.T, casting='unsafe')
    imsave(i.replace('xinjiang', 'xinjiang-msk'), img)
