import json
import os.path
# from pprint import pprint

with open('all-nps-sites.json') as data_file:    
    data = json.load(data_file)

	num = 1

	for document in data.get('documents'):
		# Creates a new file in the corpous folder named json1.json
		f = open(os.path.join("/Users/juanalvarez/Desktop/CECS 429 HW 2/corpous", "json" + str(num) + ".json"), "w+")

		# Grabs the body element from the json file and then writes to the json(num).json file
		f.write(json.dumps(document))
		num += 1
		f.close()