from scipy.ndimage import distance_transform_edt as edt
import numpy as np

def gap_repair(img, msk, r=0):
	dis, indices = edt(msk, return_indices=True)
	if r!=0: msk = msk & (dis<r)
	if isinstance(img, list): imgs = img
	else: imgs = [img] if img.ndim==2 else img
	rc = [i[msk] for i in indices]
	for im in imgs: im[msk] = im[tuple(rc)]
	return img