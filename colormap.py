import numpy as np
from PIL import Image
from skimage import io, data, color
import os

# Get the specified bit value
def bitget(byteval, idx):
    return ((byteval & (1 << idx)) != 0)

# Create label-color map, label --- [R G B]
#  0 --- [  0   0   0],  1 --- [128   0   0],  2 --- [  0 128   0]
#  3 --- [128 128   0],  4 --- [  0   0 128],  5 --- [128   0 128]
#  6 --- [  0 128 128],  7 --- [128 128 128],  8 --- [ 64   0   0]
#  9 --- [192   0   0], 10 --- [ 64 128   0], 11 --- [192 128   0]
# 12 --- [ 64   0 128], 13 --- [192   0 128], 14 --- [ 64 128 128]
# 15 --- [192 128 128], 16 --- [  0  64   0], 17 --- [128  64   0]
# 18 --- [  0 192   0], 19 --- [128 192   0], 20 --- [  0  64 128]
def labelcolormap(N=256):
    color_map = np.zeros((N, 3))
    for n in xrange(N):
	id_num = n
    	r, g, b = 0, 0, 0
	for pos in xrange(8):
	    r = np.bitwise_or(r, (bitget(id_num, 0) << (7-pos)))
	    g = np.bitwise_or(g, (bitget(id_num, 1) << (7-pos)))
	    b = np.bitwise_or(b, (bitget(id_num, 2) << (7-pos)))
	    id_num = (id_num >> 3)
	color_map[n, 0] = r
	color_map[n, 1] = g
	color_map[n, 2] = b
    return color_map/255

def reverse_color(img):
    img[img < 255] = 128
    img[img == 255] = 0
    img[img == 128] = 255
    return img

def convert_per_img(name):
    color_map=labelcolormap(5)
    print color_map
    img = Image.open('labels/' + name).convert("L")
    img = np.array(img)
    img = reverse_color(img)
    dst = color.label2rgb(img, colors=color_map[1:], bg_label=0, bg_color=(0, 0, 0))
    print np.shape(dst)
    io.imsave('labels_rgb/' + name, dst)

import colorlabel
import PIL.Image
import numpy as np
from skimage import io,data,color

COLORS = ([0.502,   0,   0], [  0, 0.502,   0], [0.502, 0.502,   0], [  0,   0, 0.502])# ('red', 'green', 'yellow', 'purple')
# colors:  [label: [1, 0, 0], lock: [0.   , 0.502, 0.   ], paper tape: [1, 1, 0], purple: [0.502, 0.   , 0.502]]
"""
COLORS = [[128,   0,   0], 
	  [  0, 128,   0],
	  [128, 128,   0],
	  [  0,   0, 128]]
"""

if __name__=="__main__":
    for root, dirs, names in os.walk('labels/'):
	for name in names:
	    if name.endswith('png'):
		print name
		img = PIL.Image.open('labels/'+name)
		label = np.array(img)
		dst = colorlabel.label2rgb(label, bg_label = 0, bg_color =(0,0,0), colors=COLORS) # , colors=COLORS
		io.imsave('labels_rgb/'+name, dst)
		print "#######################################"
		


