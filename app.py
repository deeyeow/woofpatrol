from flask import Flask, render_template, url_for, request, redirect
from filter import apply_mask

import cv2
import numpy as np
import base64
import random

from db import Client

app = Flask(__name__)

client = Client()

@app.route('/')
def index():
    # if request.method == 'POST':
    #     videoCapture()
    #     return redirect('/')
    # else:
    #     render_template('index.html')

    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['image']

    # Save file
    #filename = 'static/' + file.filename
    #file.save(filename)

    # Read image
    image = cv2.imdecode(np.frombuffer(file.read(), np.uint8), cv2.IMREAD_COLOR)
    # print(image.shape)
    
    # load mask
    mask = cv2.imread('assets/snapchat_dog.png')
    
    # initialize front face classifier
    cascade = cv2.CascadeClassifier("assets/haarcascade_frontalface_default.xml")
   
    # Get image shape
    image_h, image_w, _ = image.shape

    # Convert to black-and-white, and add contrast
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blackwhite = cv2.equalizeHist(gray)

    # Detect faces
    rects = cascade.detectMultiScale(
        blackwhite, scaleFactor=1.3, minNeighbors=4, minSize=(30, 30),
        flags=cv2.CASCADE_SCALE_IMAGE)

    # Add all bounding boxes to the image
    for x, y, w, h in rects:
        # crop a frame slightly larger than the face
        y0, y1 = int(y - 0.20*h), int(y + 0.80*h)
        x0, x1 = x, x + w

        # give up if the cropped frame would be out-of-bounds
        if x0 < 0 or y0 < 0 or x1 > image_w or y1 > image_h:
            continue

        # apply mask
        image[y0: y1, x0: x1] = apply_mask(image[y0: y1, x0: x1], mask)

    # Save
    #cv2.imwrite(filename, image)
        
    # In memory
    image_content = cv2.imencode('.jpg', image)[1].tostring()
    encoded_image = base64.encodebytes(image_content)
    to_send = 'data:image/jpg;base64, ' + str(encoded_image, 'utf-8')

    if len(rects) == 0:
        face_detected = False
    else:
        if client.getSize() == 0:
            counter = 0
        else:
            counter = client.getHighestCount() + 1
        face_detected = True
        client.insertImage(counter, encoded_image)
        counter += 1


    return render_template('index.html', image_to_show=to_send, face_detected=face_detected, init_upload=True)

@app.route('/mostwanted', methods=['POST'])
def show_most_wanted():
    size = client.getSize()
    if (size == 0):
        has_data = False
        to_send = None
    
    else:
        has_data = True
        rand = random.randint(0, size - 1)
        image_str = client.retrieveImage(rand)

        encoded_image = base64.encodebytes(image_str)
        to_send = 'data:image/jpg;base64, ' + str(encoded_image, 'utf-8')

    return render_template('index.html', image_to_show=to_send, has_data=has_data, init_mostwanted=True)

if __name__ == '__main__':
    app.run(debug=True)