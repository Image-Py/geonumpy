# pretreat

遥感影像需要很多预处理工作，比如大气校正，去条带



### degap

---

degap(img, msk, r=0)

**img:** GeoArray对象，要去条带的影像

**msk:** 条带掩膜

**r:** 去条带影响半径，超出这个范围则不进行修复，0 表示整图修复