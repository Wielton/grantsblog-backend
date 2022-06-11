from flask import Flask, request, jsonify
from helpers.db_helpers import *
import sys

app = Flask(__name__)

@app.get('/api/animalsdb')
def animals_get():
    # TODO: db SELECT
    animal_list = run_query("SELECT * FROM animal")
    resp = []
    for animal in animal_list:
        an_obj = {}
        an_obj['animalId'] = animal[0]
        an_obj['animalName'] = animal[1]
        an_obj['imageURL'] = animal[2]
        resp.append(an_obj)
    return jsonify(resp), 200

@app.post('/api/animalsdb')
def animals_post():
    data = request.json
    animal_name = data.get('animalName')
    image_url = data.get('imageURL')
    if not animal_name:
        return jsonify("Missing required argument 'animalName'"), 422
    if not image_url:
        return jsonify("Missing required argument 'imageURL'"), 422
    # TODO: Error checking the actual values for the arguments
    run_query("INSERT INTO animal (name, image_url) VALUES (?,?)", [animal_name, image_url])
    return jsonify("Animal added"), 201




if (len(sys.argv) > 1):
    mode = sys.argv[1]
else:
    print("No mode argument: testing | production")
    exit()    
    
if mode == "testing":
    from flask_cors import CORS
    CORS(app)    # Only want CORS on testing servers
    app.run(debug=True)
elif mode == "production":
    import bjoern
    bjoern.run(app, "0.0.0.0", 5005) # Other apps might be using 5000 or 5001 at the moment, so to be safe I'll go 5005
    print('Running in development mode!')
else:
    print("Invalid mode.  Must be testing or production")