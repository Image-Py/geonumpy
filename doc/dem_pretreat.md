# geonumpy.pretreat

遥感影像需要很多预处理工作，比如大气校正，去条带等



## 去条带

```python
path = '../data/landsat-gap/LE07_L1TP_123037_20180721_20180816_01_T1_sr_ndvi.tif'
img = gio.read_tif(path)
# 去条带
degapimg = gpt.degap(img.copy(), img==-9999, 10)

# 绘制处理前后的图并展示
ax1 = plt.subplot(121)
ax1.set_title('ori image')
ax1.imshow(img, cmap='gray')

ax2 = plt.subplot(122)
ax2.set_title('degaped image')
ax2.imshow(degapimg, cmap='gray')
plt.show()

```
![](./imgs/16.png)

部分旧传感器返回的数据中带有条带，degap 函数可以有效的处理条带。