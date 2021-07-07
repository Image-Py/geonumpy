from shapely.affinity import affine_transform
from shapely.geometry import GeometryCollection
from PIL import Image, ImageDraw, ImageFont
from shapely.geometry import Polygon, LineString
import numpy as np, pandas as pd, pyproj
from numba import jit

def draw_polygon(raster, shape, color, width):
    shape = shape.to_crs(raster.crs)
    img = Image.fromarray(raster)
    draw = ImageDraw.Draw(img)
    geoms = shape['geometry'].affine_transform(raster.imat1)
    if isinstance(color, np.ndarray): colors = color.tolist()
    elif isinstance(color, pd.Series): colors = color.to_list()
    elif isinstance(color, str): colors = shape[color].to_list()
    else: colors = [color] * len(geoms)
    for g, c in zip(geoms, colors):
        gs = g #affine_transform(g, m)
        if isinstance(gs, Polygon): gs = [gs]
        if isinstance(gs, LineString): gs = [gs]
        for g in gs:
            pts = np.array(g.exterior.xy).T.astype(np.int).reshape((-1,2))
            pts = [tuple(i) for i in pts]
            if width==0: draw.polygon(pts, c)
            if width!=0: draw.line(pts, c, width, joint='curve')
    raster[:] = np.array(img)

def draw_line(raster, shape, color, width):
    shape = shape.to_crs(raster.crs)
    m = raster.mat
    m = [1/m[0,1], 0, 0, -1/m[0,1], -m[0,0]/m[0,1], m[1,0]/m[0,1]]
    img = Image.fromarray(raster)
    draw = ImageDraw.Draw(img)
    geoms = shape['geometry']
    if isinstance(color, pd.Series): colors = color.to_list()
    elif isinstance(color, str): colors = shape[color].to_list()
    else: colors = [color] * len(geoms)
    for g, c in zip(geoms, colors):
        gs = affine_transform(g, m)
        if isinstance(gs, LineString): gs = [gs]
        for g in gs:
            pts = np.array(g.xy).T.astype(np.int).reshape((-1,2))
            pts = [tuple(i) for i in pts]
            draw.line(pts, c, width, joint='curve')
    raster[:] = np.array(img)

def draw_mask(img, msk):
    weight = msk[:,:,3]/255
    np.multiply(img.T, 1-weight.T, out=img.T, casting='unsafe')
    np.add(img.T, msk[:,:,:3].T*weight.T, out=img.T, casting='unsafe')

@jit
def draw_mask(img, msk):
    h, w = img.shape[:2]
    for r in range(h):
        for c in range(w):
            wg = msk[r,c,3]/255.0
            img[r,c] = img[r,c]*(1-wg) + msk[r,c,:3]*wg
    return img

def draw_unit(raster, x, y, w, h, ft, color, unit, lw, anc='left'):
    y = y-h
    img = Image.fromarray(raster)
    d = ImageDraw.Draw(img)
    def f(x, dir=0):
        v = raster.shape[1-dir]
        if abs(x)>1: x = int(x)
        else: x = int(v * x)
        return x if x>=0 else v+x
    step = int(round(f(w,0)*raster.mat[0,1]/10000))
    if step>100:
        n = 10**len(str(step))/10
        step = int(np.round(step/n)*n)
    cell = int(step * 1000 / raster.mat[0,1])
    offsetx = 0 if anc=='left' else -cell *10
    for s, e, c in zip((0,1,3,6), (1,3,6,10), (1,0,1,0)):
        d.rectangle([f(x)+s*cell+offsetx, f(y,1), 
                     f(x)+e*cell+offsetx, f(y,1)+f(h)],
                     fill=[color, None][c], outline=color, width=lw)
    font = ImageFont.truetype(*ft)
    for s in (0,1,3,6,10):
        w, h = d.textsize(str(step*(s))+['',' km'][s==10], font)
        d.text((f(x)+s*cell-w//2+offsetx, f(y,1)-ft[1]*1.2),
               str(step*(s))+['',' km'][s==10], font=font, fill=color, align='center')
    raster[:] = np.array(img)

def draw_N(raster, x, y, ft, lw, h, color):
    img = Image.fromarray(raster)
    d = ImageDraw.Draw(img)
    def f(x, dir=0):
        v = raster.shape[1-dir]
        if abs(x)>1: x = int(x)
        else: x = int(v * x)
        return x if x>=0 else v+x
    x, y = f(x), f(y, 1)
    d.polygon([x, y, x, y+h, x-h/2, y+h*5//3], color)
    d.line([x, y, x-h/2, y+h*5//3, x, y+h, x+h/2, y+h*5//3, x, y], color, lw)
    font = ImageFont.truetype(*ft)
    w,h = d.textsize('N', font)
    x, y = x-w//2, y-h*1.2
    d.text((x, y), 'N', font=font, fill=color)
    raster[:] = np.array(img)

def draw_text(raster, txt, xs, ys, color, ft, anc='lt', align='left'):
    img = Image.fromarray(raster)
    d = ImageDraw.Draw(img)
    if isinstance(txt, str): txt = [txt]
    if not hasattr(xs, '__len__'): xs = [xs]
    if not hasattr(ys, '__len__'): ys = [ys]
    def f(x, dir=0):
        v = raster.shape[1-dir]
        if abs(x)>1: x = int(x)
        else: x = int(v * x)
        return x if x>=0 else v+x
    font = ImageFont.truetype(*ft)
    for t, x,y in zip(txt, xs, ys):
        x, y = f(x), f(y,1)
        w,h = d.textsize(t, font)
        if anc=='ct': x, y = x-w//2, y-h*3/5
        if anc=='lb': y = y-h
        if anc=='lt': x, y = x, y
        if anc=='rb': x, y = x-w, y-h
        if anc=='rt': x = x-w
        d.text((x, y), t, font=font, fill=color, align=align, spacing=ft[1]*0.3)
    raster[:] = np.array(img)

def draw_lab(raster, shp, name, color, font, anc):
    gs = shp['geometry'].centroid
    m = raster.mat
    m = [1/m[0,1], 0, 0, -1/m[0,1], -m[0,0]/m[0,1], m[1,0]/m[0,1]]
    pos = [(int(p.x), int(p.y)) for p in [affine_transform(i, m) for i in gs]]
    return draw_text(raster, shp[name], *list(zip(*pos)), color, font, anc)

def draw_style(raster, x, y, body, mar, recsize, font, color, box):
    body = body[::-1]
    img = Image.fromarray(raster)
    d = ImageDraw.Draw(img)
    tcolor = color
    def f(x, dir=0):
        v = raster.shape[1-dir]
        if abs(x)>1: x = int(x)
        else: x = int(v * x)
        return x if x>=0 else v+x
    cury, maxx, (w, h, lw) = f(y,1)-mar[1], 0, recsize
    font = ImageFont.truetype(*font[:2])
    for i in range(len(body)):
        item = body[i]
        if item[0]=='line':
            _, c, t = item
            d.line([f(x)+mar[0], cury-f(h,1)//2, f(x)+mar[0]+f(w), 
                cury-f(h,1)//2], fill=c, width=lw)
            tw, th = d.textsize(t, font)
            maxx = max(maxx, f(x)+mar[0]*3+f(w)+tw)
            d.text([f(x)+mar[0]*2+f(w), cury-f(h,1)//2-th*3/5], t, 
                font=font, fill=tcolor)
            cury -= mar[1]+f(h,1)
        elif item[0]=='rect':
            _, c, t = item
            d.rectangle([f(x)+mar[0], cury, f(x)+mar[0]+f(w), cury-f(h,1)], 
                fill=c, outline=[None, tcolor][lw>0], width=lw)
            tw, th = d.textsize(t, font)
            maxx = max(maxx, f(x)+mar[0]*3+f(w)+tw)
            d.text([f(x)+mar[0]*2+f(w), cury-f(h,1)//2-th*3/5], t, 
                font=font, fill=tcolor)
            cury -= mar[1]+f(h,1)
        elif item[0]=='circle':
            _, c, t = item
            d.ellipse([f(x)+mar[0]+f(w)//2-f(h,1)//5, cury-f(h,1)//2-f(h,1)//5,
                       f(x)+mar[0]+f(w)//2+f(h,1)//5, cury-f(h,1)//2+f(h,1)//5],
                       fill=c, outline=[None, tcolor][lw>0], width=lw)
            tw, th = d.textsize(t, font)
            maxx = max(maxx, f(x)+mar[0]*3+f(w)+tw)
            d.text([f(x)+mar[0]*2+f(w), cury-f(h,1)//2-th*3/5], t, 
                font=font, fill=tcolor)
            cury -= mar[1]+f(h,1)
        elif item[0]=='blank':
            cury -= item[1]
        else:
            print(item)
            t, tf, ts = item
            tf = ImageFont.truetype(tf, ts)
            tw, th = d.textsize(t, tf)
            d.text([f(x)+mar[0]*2, cury-f(h,1)//2-th*3/5], 
                t, font=tf, fill=tcolor)
            cury -= mar[1]+f(h,1)
    if box>0:
        d.rectangle([f(x), f(y,1), maxx, cury], outline=tcolor, width=box)
    raster[:] = np.array(img)

def draw_ruler(raster, left, top, right, bot, step, crs, font, color, w, dh): 
    img = Image.fromarray(raster)
    d = ImageDraw.Draw(img)
    def f(x, dir=0):
        v = raster.shape[1-dir]
        if abs(x)>1: x = int(x)
        else: x = int(v * x)
        return x if x>=0 else v+x
    left, top, right, bot = f(left), f(top,1), f(right), f(bot,1)
    d.rectangle([left, top, right, bot], outline=color, width=w)
    pts = np.array([(left,top),(right,top),(right,bot),(left,bot)])
    prj1, prj2 = pyproj.CRS(raster.crs), pyproj.CRS(crs)
    ct = pyproj.Transformer.from_crs(prj1, prj2, always_xy=True)
    pts = np.dot(raster.mat[:,1:], pts.T) + raster.mat[:,:1]
    xs, ys = ct.transform(*pts)

    a, b = int(xs[0]//step), int(xs[1]//step)
    tab = [i*step for i in range(a+1, b+1)]
    nps = ct.transform(tab, np.linspace(ys[0], ys[1], len(tab)), direction='INVERSE')
    nps = np.dot(np.linalg.inv(raster.mat[:,1:]), nps - raster.mat[:,:1])
    font = ImageFont.truetype(*font)
    for x,e in zip(nps[0],tab):
        d.line([int(x), top, int(x), top-dh], color, w)
        tw, th = d.textsize('%d°E'%e, font)
        d.text((int(x-tw//2), top-dh-th*1.2), '%d°E'%e, font=font, fill=color)

    a, b = int(xs[3]//step), int(xs[2]//step)
    tab = [i*step for i in range(a+1, b+1)]
    nps = ct.transform(tab, np.linspace(ys[3], ys[2], len(tab)), direction='INVERSE')
    nps = np.dot(np.linalg.inv(raster.mat[:,1:]), nps - raster.mat[:,:1])
    for x,e in zip(nps[0],tab):
        d.line([int(x), bot, int(x), bot+dh], color, w)
        tw, th = d.textsize('%d°E'%e, font)
        d.text((int(x-tw//2), bot+dh+th*0.0), '%d°E'%e, font=font, fill=color)

    a, b = int(ys[3]//step), int(ys[0]//step)
    tab = [i*step for i in range(a+1, b+1)]
    nps = ct.transform(np.linspace(xs[3], xs[0], len(tab)), tab, direction='INVERSE')
    nps = np.dot(np.linalg.inv(raster.mat[:,1:]), nps - raster.mat[:,:1])
    for y,n in zip(nps[1],tab):
        d.line([left, int(y), left-dh, int(y)], color, w)
        tw, th = d.textsize('%d°N'%n, font)
        d.text((left-dh-tw-th*0.2, int(y-th*3/5)), '%d°N'%n, font=font, fill=color)

    a, b = int(ys[2]//step), int(ys[1]//step)
    tab = [i*step for i in range(a+1, b+1)]
    nps = ct.transform(np.linspace(xs[2], xs[1], len(tab)), tab, direction='INVERSE')
    nps = np.dot(np.linalg.inv(raster.mat[:,1:]), nps - raster.mat[:,:1])
    for y,n in zip(nps[1],tab):
        d.line([right, int(y), right+dh, int(y)], color, w)
        tw, th = d.textsize('%d°N'%n, font)
        d.text((right+dh+th*0.2, int(y-th*3/5)), '%d°N'%n, font=font, fill=color)
    raster[:] = np.array(img)

def draw_bound(raster, left, top, right, bot, c, lw, clear=None):
    def f(x, dir=0):
        v = raster.shape[1-dir]
        if abs(x)>1: x = int(x)
        else: x = int(v * x)
        return x if x>=0 else v+x
    left, top, right, bot = f(left), f(top,1), f(right), f(bot,1)
    if not clear is None:
        raster[:top] = clear
        raster[bot:] = clear
        raster[:,:left] = clear
        raster[:,right:] = clear
    img = Image.fromarray(raster)
    d = ImageDraw.Draw(img)
    d.rectangle([left, top, right, bot], outline=c, width=lw)
    raster[:] = np.array(img)