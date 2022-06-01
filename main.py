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

face_db = []
faces = []


def zaznajObraz(img_path1):
    try:
        slika1 = cv2.imread(img_path1)

        detected_faces = faceCascade.detectMultiScale(slika1, 1.3, 5)
        x, y, w, h = detected_faces[0]  # focus on the 1st face in the image

        slika1 = slika1[y:y + h, x:x + w]  # focus on the detected area
        slika1 = cv2.resize(slika1, (700, 700))
        slika1 = cv2.cvtColor(slika1, cv2.COLOR_BGR2GRAY)
    except:
        print("No face detected.")
        return None

    return slika1


def najdiObraz(target_file):
    img2 = zaznajObraz(target_file)
    if img2 is None:
        return "No_face"

    idx, confidence = model.predict(img2)


    print("Confidence: ", round(confidence, 2))
    print("Path: ", face_db[idx])
    match_path = face_db[idx]
    #match_name = re.sub(r'^.*?\\', '', match_path)

    print("Name: ", match_path)
    return match_path


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
            face_db.append(filename)

        #return str(len(face_db))

        for img_path0 in face_db:
            img0 = zaznajObraz(img_path0)
            if img0 is not None:
                faces.append(img0)

        ids = np.array([i for i in range(0, len(faces))])


        pre_built_model = "pre-built-model.yml"

        model.train(faces, ids)
        model.save(pre_built_model)

        slikaZNajdenimObrazom = najdiObraz("iskana/" + ime + '.png')
        if slikaZNajdenimObrazom is 'No_face':
            return "ERROR_no_face_detected"

        value = {
            "ime": str(slikaZNajdenimObrazom)
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
