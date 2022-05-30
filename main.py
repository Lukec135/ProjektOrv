#!/usr/bin/python
# -*- coding: utf-8 -*-
import os

from flask import Flask
from flask import request

import io
import base64
from PIL import Image

import requests
import json

#######################################
# numpy~=1.22.4
# opencv-python~=4.5.5.64
# opencv-contrib-python~=4.5.5.64

import re

import numpy as np

import cv2

import glob

face_detector_path = 'haarcascade_frontalface_default.xml'
faceCascade = cv2.CascadeClassifier(face_detector_path)  # POLJUBNI DETEKTOR

model = cv2.face.LBPHFaceRecognizer_create()  # Local Binary Patterns Histograms #LBP   <---- !!!

face_db = []
faces = []


def detect_face(img_path1):
    img1 = cv2.imread(img_path1)

    detected_faces = faceCascade.detectMultiScale(img1, 1.3, 5)
    (x, y, w, h) = detected_faces[0]  # focus on the 1st face in the image

    img1 = img1[y:y + h, x:x + w]  # focus on the detected area
    img1 = cv2.resize(img1, (224, 224))
    img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)

    return img1


def findFace(target_file):
    img2 = detect_face(target_file)

    # print(img.shape)

    (idx, confidence) = model.predict(img2)

    print ('Confidence: ', round(confidence, 2))
    print ('Path: ', face_db[idx])
    match_path = face_db[idx]

    # match_name = re.sub(r'^.*?\\', '', match_path)

    print ('Name: ', match_path)

    # plt.show()

    return match_path


##############################################################################

app = Flask(__name__)


@app.route('/')
def hello_world():
    name = os.environ.get('NAME', 'World')
    return 'Hello {}!'.format(name)


@app.route('/preveri', methods=['POST'])
def preveri():
    if not request.json or not 'ime' in request.json:
        return 400

    ime = request.json['ime']
    slika = request.json['slika']

    try:

        # Assuming base64_str is the string value without 'data:image/jpeg;base64,'

        img3 = Image.open(io.BytesIO(base64.decodebytes(bytes(slika,
                          'utf-8'))))
        img3.save('iskana/' + ime + '.png')

        vse_slike_internal()

        # #############################################################################

        # face_db = []

        for filename in glob.glob('slike/*'):  # assuming png
            face_db.append(filename)

        # return str(len(face_db))

        # faces = []

        for img_path0 in face_db:

            # print(img_path0)

            img0 = detect_face(img_path0)

            # if img0 is not None:

            faces.append(img0)

        # return str(len(faces)) !! ne izpise

        ids = np.array([i for i in range(0, len(faces))])

        pre_built_model = 'pre-built-model.yml'

        model.train(faces, ids)
        model.save(pre_built_model)

        image_found = findFace('iskana/' + ime + '.png')

        # #############################################################################

        value = {'ime': str(image_found)}
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

            img4 = \
                Image.open(io.BytesIO(base64.decodebytes(bytes(slika,
                           'utf-8'))))
            img4.save('slike/' + ime + ' ' + str(c) + '.png')
            c = c + 1

        (_, _, files) = next(os.walk('slike'))
        file_count = len(files)

        # return str(file_count)

        value = {'velikost': str(file_count)}
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

            img4 = \
                Image.open(io.BytesIO(base64.decodebytes(bytes(slika,
                           'utf-8'))))
            img4.save('slike/' + ime + ' ' + str(c) + '.png')
            c = c + 1
    except Exception as e:
        return str(e)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT',
            8080)))
