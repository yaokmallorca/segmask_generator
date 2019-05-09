import os
from subprocess import call

BASE_DIR = 'resize_label/'

for root, dirs, files in os.walk(BASE_DIR):
    for name in files:
	if name.endswith('json'):
	    # command = '[labelme_json_to_dataset, {}]'.format(name)
	    # print command
	    name = BASE_DIR + name
	    call(['labelme_json_to_dataset', name])
	    print "########################################################"
