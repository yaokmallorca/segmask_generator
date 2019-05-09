from PIL import Image
import os
import json
from base64 import b64encode, b64decode
import math
import cv2
import imutils

def convert_img(width, height, IMG_IN_PATH, IMG_OUT_PATH):

    img_name = IMG_IN_PATH + '.jpg'
    img_out = IMG_OUT_PATH + '.jpg'
    im = Image.open(img_name)
    # h, w = im.shape[:2]
    (w, h)= im.size
    print h, w
    if w == 1920 and h == 1080:
	x_s = width
	y_s = height # h * width / w
    else:
	x_s = width
	y_s = height
    out = im.resize((x_s, y_s), Image.ANTIALIAS)
    out.save(img_out)

def coord_rotation(x, y, x0, y0, beta):
    x1 = (x-x0)*math.cos(beta) - (y-y0)*math.sin(beta) + x0
    y1 = (x-x0)*math.sin(beta) + (y-y0)*math.cos(beta) + y0
    return x1, y1

def convert_json(width, height, JSON_IN_PATH, JSON_OUT_PATH, IMG_IN_PATH, IMG_OUT_PATH, img_name):

	json_path = JSON_IN_PATH + img_name + '.json'
	json_out = JSON_OUT_PATH + img_name + '.json'
	img_in = IMG_IN_PATH + img_name + '.jpg'
	is_rotation = False
	# print json_out
	with open(json_path) as load_f:
		load_dict = json.load(load_f)
		# img_name = path[0:-4] + ".jpg" # "resize_img/" + path[0:-4] + ".jpg" 
		# Change image name
		im = Image.open(img_in)
		(w, h)= im.size
		w_s = float(width) / float(w)
		h_s = float(height) / float(h)
		new_img_name = img_name + '.jpg'
		load_dict['imagePath'] = new_img_name
		im.close()
		# Change image data
		with open(IMG_OUT_PATH + new_img_name, 'rb') as f:
			new_img_name = f.read()
			load_dict['imageData'] = b64encode(new_img_name).decode('utf-8')# new_img_name

		for i in range(0, len(load_dict['shapes'])):
			for iter_pt in range(0, len(load_dict['shapes'][i]['points'])):
				# print load_dict['shapes'][i]['points'][iter_pt]
				x = load_dict['shapes'][i]['points'][iter_pt][0] * w_s # x_s
				y = load_dict['shapes'][i]['points'][iter_pt][1] * h_s # y_s
				load_dict['shapes'][i]['points'][iter_pt][0] = x
				load_dict['shapes'][i]['points'][iter_pt][1] = y

	with open(json_out, 'w') as dump_f:
		print json_out
		json.dump(load_dict, dump_f)



if __name__ == '__main__':
	img_list = os.listdir(DATA_DIR + 'img/')
	# print file_list
	for filename in img_list:
		# filename = "image0355.jpg"
		print filename
		# img_path = DATA_DIR + 'resize_img/' + filename
		# json_path = DATA_DIR + 'JSON/' + filename[0:-4] + ".json"
		convert_img(500, 500, filename)
		convert_json(500, 500, filename)
		print "#################################"
		# input('stop')
