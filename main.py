import os

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


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
