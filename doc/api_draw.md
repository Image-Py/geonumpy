# geonumpy.draw

此模块用于绘图，这里说明本模块凡是需要提供坐标，长度的内容，都遵循以下规则：

* 正整数表示从左边算或从上方算，具体看作用的方向

* 负整数表示从右边算或从底部算，具体看作用的方向

* 小数表示对应维度的比例，例如x给0.5，表示宽度的一半

  

### draw_polygon

---

draw_polygon(raster, shape, color, width)

**raster:** 被绘制的 geoarray 对象

**shape:** 用于绘图的GeoDataFrame对象，必须是polygon类型

**color: ** 绘制用的颜色

* 如果是整数，浮点，表示用这个值绘制

* 如果是pandas.series对象或ndarray对象，则表示依次用这些颜色绘制每个对象

* 如果是字符类型，则会到shape中查找对应列的值一次绘制每个对象

* 如果是tuple类型，则认为是rgb色

**width:** 线条宽度，如果给0，则表示进行多边形填充



### draw_text

---

draw_text(raster, txt, x, y, color, ft, anc='lt', align='left')

**raster:** 被绘制的geoarray对象

**txt:** 要绘制的文字，支持多行

**x, y:** 绘制的坐标，比例尺的基准点是左下角或右小角，取决于anc

**w, h:** 绘制比例尺的宽度，高度（通常w会给小数，比如0.3，表示占用十分之三宽度）

**color:** 绘图使用的颜色

**ft:** 字体，字号的二元组

**anc:** lt, rt, lb, rb, ct，表示左上角，右上角，左下角，右下角，中心

**align:** left, right, center，多行文字时，左右对齐，或中心对齐



### draw_lab

---

draw_lab(raster, shp, name, color, ft, anc)

**raster:** 被绘制的geoarray对象

**shp:** 用于绘图的GeoDataFrame对象

**name:** 列名称，需要时str类型的列，用于绘制标签

**color:** 绘图使用的颜色

**ft:** 字体，字号的二元组

**anc:** lt, rt, lb, rb, ct，表示左上角，右上角，左下角，右下角，中心



### draw_unit

---

draw_unit(raster, x, y, w, h, ft, color, unit, lw, anc='l')

**raster:** 被绘制的geoarray对象

**x, y:** 绘制的坐标，比例尺的基准点是左下角或右小角，取决于anc

**w, h:** 绘制比例尺的宽度，高度（通常w会给小数，比如0.3，表示占用十分之三宽度）

**ft:** 字体，字号的二元组

**color:** 绘图使用的颜色

**lw:** 线条宽度

**anc:** left 或 right，表示左对齐或右对齐



### draw_N

---

draw_N(raster, x, y, ft, lw, h, color)

**raster:** 被绘制的geoarray对象

**x, y:** 绘制的坐标，基准点是箭头顶端

**ft:** 字体，字号的二元组

**lw:** 线条宽度

**h:** 指北针中心竖线高度

**color:** 绘图使用的颜色



### draw_bound

---

draw_bound(raster, left, top, right, bot, color, lw, clear=None):

**raster:** 被绘制的geoarray对象

**left, top, right, bot:** 上下左右的边界坐标，右侧，底部通常用左侧与上边的相反数

**color:** 绘图使用的颜色

**lw:** 线条宽度

**clear:** 线框以外的清除色，None表示不清除



### draw_ruler

---

draw_ruler(raster, left, top, right, bot, step, crs, ft, color, lw, dh)

**raster:** 被绘制的geoarray对象

**left, top, right, bot:** 上下左右的边界坐标，右侧，底部通常用左侧与上边的相反数

**step:** 刻度间隔

**crs:** 刻度坐标系，很可能使用投影坐标绘图，但使用经纬度绘制刻度

**ft:** 字体，字号的二元组

**color:** 绘图使用的颜色

**lw:** 线条宽度

**dh:** 刻度高度



### draw_style

---

draw_style(raster, x, y, body, mar, recsize, ft, color, box)

**raster:** 被绘制的geoarray对象

**x, y:** 绘制的坐标，基准点是左下角

**body:**  三元组，具体用法如下：

* (str, font, height) 表示用font字体，height高度，绘制str
* ('rect', c,  str) 用颜色c，绘制一个矩形，后面跟着文字str
* ('line', c,  str) 用颜色c，绘制一条线段，后面跟着文字str
* ('circle', c,  str) 用颜色c，绘制一个圆，后面跟着文字str
* ('blank', h) 一个高度为h的空行

**mar:** 二元组，图例之间的行列间距

**recsize:** 三元组，矩形的尺寸，以及边框线条宽度

**ft:** 字体，字号的二元组

**color:** 绘图使用的颜色，将被用于文字，矩形边框，以及外框

**box:** 最外侧边框宽度，0表示无边框

```python
body = [('Style', 'simhei', 72),
         ('line', 1,  'line'),
         ('circle', 2,  'circle'),
         ('rect', 3,  'rect')]

draw_style(paper,30,-30, body, mar=(20, 30), recsize=(120,60,3), 
           font=('simsun', 60), color=4, box=5)
```

