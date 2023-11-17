from flask import Flask, jsonify
from flask_cors import CORS
from flask import request, abort, Response
import os
import nanovizer
import barcode_to_sequence
import no_genome_name
import threading
import json



DEBUG = True

app = Flask(__name__)
app.config.from_object(__name__)

CORS(app, resources={r'/*': {"origins":"*"}})



@app.route("/parse-file", methods=["POST", "GET"])
def run_nanovizer():
	global parameters
	global result_folder
	parameters = {"file_name":"", "genome_name":None, "genome_size":None, "min_position_3":0, "min_position_5":0, "max_position_5":1000000, "min_read_length":0}
	input_front = request.get_data()
	input_front = json.loads(input_front.decode('utf-8'))

	for key in input_front:
		if key in parameters:
			if input_front[key] != "":
				parameters[key] = input_front[key]
	DATA = nanovizer.main(parameters["file_name"], parameters["genome_name"], parameters["genome_size"],\
						  int(parameters["min_position_3"]), int(parameters["min_position_5"]), int(parameters["max_position_5"]),\
						  int(parameters["min_read_length"]))

 

	return jsonify(DATA)


def launch_url():
	shell = "bash html.sh"
	os.system(shell)

if __name__ == '__main__':
	#Thread2 = threading.Thread(target=launch_url)
	#Thread2.start()
	app.run(host="0.0.0.0")
