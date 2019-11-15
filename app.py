from flask import Flask, render_template, url_for, request, redirect
from pymongo import MongoClient

from filter import videoCapture

import cv2
import numpy as np

app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        videoCapture()
        return redirect('/')
    else:
        render_template('index.html')

    return render_template('index.html')





if __name__ == "__main__":
    app.run(debug=True)