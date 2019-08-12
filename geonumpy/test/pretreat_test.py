import geonumpy.io as gio
import geonumpy.pretreat as gpt
import matplotlib.pyplot as plt

def degap():
    img = gio.read_tif('../data/landsat-gap/LE07_L1TP_123037_20180721_20180816_01_T1_sr_ndvi.tif')
    degapimg = gpt.degap(img.copy(), img==-9999, 10)

    ax1 = plt.subplot(121)
    ax1.set_title('ori image')
    ax1.imshow(img, cmap='gray')
    
    ax2 = plt.subplot(122)
    ax2.set_title('degaped image')
    ax2.imshow(degapimg, cmap='gray')
    plt.show()

if __name__ == '__main__':
    degap()
