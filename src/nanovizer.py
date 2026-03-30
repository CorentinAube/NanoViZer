import json
from flask import Flask, jsonify, request
from flask_cors import CORS
import main

DEBUG = True

app = Flask(__name__)
app.config.from_object(__name__)

CORS(app, resources={r'/*': {"origins":"*"}})


@app.route("/parse-file", methods=["POST", "GET"])
def run_nanovizer():
    """
    This function retrieves information from the front end, then launches the back end,
    NanoViZer, using either user-provided parameters or default values.
    It returns a JSON file to the back end, which then generates graphical
    representations of the data.
    """
    parameters = {"file_name":"", "genome_name":None,"genome_size":None, \
                  "passthrough":0, "min_3_end":0, \
                  "max_3_end":1000000000000, "min_read_length":0, \
                  "max_5_start":0, "genome_file_name":None, "min_5_start":1000000000000}

    input_front = request.get_data()
    input_front = json.loads(input_front.decode('utf-8'))

    for key in input_front:
        if key in parameters:
            if input_front[key] != "":
                parameters[key] = input_front[key]

    data = main.main(parameters["file_name"], parameters["genome_name"], \
                          parameters["genome_size"], int(parameters["passthrough"]), \
                          int(parameters["min_3_end"]), int(parameters["max_3_end"]),\
                          int(parameters["min_read_length"]),parameters["max_5_start"], parameters["genome_file_name"], \
                          int(parameters["min_5_start"]))
    return jsonify(data)

if __name__ == '__main__':
    app.run(host="0.0.0.0")
