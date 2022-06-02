import os
from flask import Flask
from flask import request
import io
import base64
from PIL import Image
import requests
import json
import numpy as np
import cv2
import glob

face_detector_path = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(face_detector_path)

model = cv2.face.LBPHFaceRecognizer_create() #LBP

slike_navadne = []
slike_obrazov = []

def zaznajObraz(pot_slike):
    try:
        slika1 = cv2.imread(pot_slike)

        zaznani_obrazi = faceCascade.detectMultiScale(slika1, 1.3, 5)
        x, y, w, h = zaznani_obrazi[0]  # vrne prvi obraz na sliki

        slika1 = slika1[y:y + h, x:x + w]  # se fokusiramo na zaznano območje
        slika1 = cv2.resize(slika1, (224, 224))
        slika1 = cv2.cvtColor(slika1, cv2.COLOR_BGR2GRAY)
    except:
        print("No face detected.")
        return None

    return slika1


def najdiObraz(glavna_slika):
    img2 = zaznajObraz(glavna_slika)
    if img2 is None:
        return "No_face"

    index, prepricanje = model.predict(img2)
    print("Procent prepričanja: ", round(prepricanje, 2))
    ime_slike = slike_navadne[index]

    print("Ime: ", ime_slike)
    return ime_slike



app = Flask(__name__)



@app.route('/preveri', methods=['POST'])
def preveri():
    if not request.json or not 'ime' in request.json:
        return 400

    ime = request.json['ime']
    slika = request.json['slika']

    try:
        # Assuming base64_str is the string value without 'data:image/jpeg;base64,'
        img3 = Image.open(io.BytesIO(base64.decodebytes(bytes(slika, "utf-8"))))
        img3.save("iskana/" + ime + '.png')


        vse_slike_internal()

        for filename in glob.glob('slike/*'):  #lahko je katerikoli format
            slike_navadne.append(filename)

        #return str(len(face_db))

        for img_path0 in slike_navadne:
            img0 = zaznajObraz(img_path0)
            if img0 is not None:
                slike_obrazov.append(img0)

        np_indexes = np.array([i for i in range(0, len(slike_obrazov))])


        znacilnice = "znacilnice.yml"

        model.train(slike_obrazov, np_indexes)
        model.save(znacilnice)

        slikaZNajdenimObrazom = najdiObraz("iskana/" + ime + '.png')
        if slikaZNajdenimObrazom is 'No_face':
            return "ERROR_no_face_detected"

        value = {
            "ime": str(slikaZNajdenimObrazom)
        }
        return json.dumps(value)
    except Exception as e:
        return str(e)


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

    data = response.json()

    c = int(0)
    for i in data['images']:
        ime = i['ime']
        slika = i['slika']
        try:
            # Assuming base64_str is the string value without 'data:image/jpeg;base64,'
            img4 = Image.open(io.BytesIO(base64.decodebytes(bytes(slika, "utf-8"))))
            img4.save('slike/' + ime + ' ' + str(c) + '.png')
            c = c+1
        except:
            print("neveljavna slika")



if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))