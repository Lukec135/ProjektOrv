import base64
import io
import json
import os
from tkinter import Image

import requests as requests
from flask import Flask
from flask import request, jsonify

# import io
# import base64
# from PIL import Image


app = Flask(__name__)


@app.route("/")
def hello_world():
    name = os.environ.get("NAME", "Mernik in Adam")
    return "Hello {}!".format(name)


@app.route('/dodaj', methods=['POST'])
def dodaj_sliko():
    if not request.json or not 'ime' in request.json:
        return 400

    ime = request.json['ime']
    slika = request.json['slika']

    # with open("imageToSave.png", "wb") as fh:
    #    fh.write(base64.decodebytes(img_data))

    # img = Image.open(io.BytesIO(base64.decodebytes(bytes(base64_str, "utf-8"))))
    # img.save("slike\\" + ime + '.png')

    return ("DELA ime: " + ime + " slika: " + slika).jsonify

@app.route('/vse_slike', methods=['POST'])
def vse_slike():

    url = 'https://silent-eye-350012.oa.r.appspot.com/images/listAPI'
    response = requests.post(url)

    try:
        data = response.json()

        c = int(0)
        for i in data['images']:
            ime = i['ime']
            slika = i['slika']

            # Assuming base64_str is the string value without 'data:image/jpeg;base64,'
            img4 = Image.open(io.BytesIO(base64.decodebytes(bytes(slika, "utf-8"))))
            img4.save('slike/' + ime + ' ' + str(c) + '.png')
            c = c+1

        _, _, files = next(os.walk("slike"))
        file_count = len(files)
        #return str(file_count)
        value = {
            "velikost": str(file_count)
        }
        return json.dumps(value)
    except Exception as e:
        return str(e)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
