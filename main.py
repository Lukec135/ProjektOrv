import os

from flask import Flask
from flask import request

import io
import base64
from PIL import Image

import requests
import json



app = Flask(__name__)


@app.route("/")
def hello_world():
    name = os.environ.get("NAME", "World")
    return "Hello {}!".format(name)



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


def vse_slike_internal():
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
    except Exception as e:
        return str(e)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
