import cv2
import sys
import dlib
import numpy as np
from contextlib import contextmanager
import urllib2
from bmi_model import get_model
import bmi_config as config

#Retrieves Pretrained model to predict Body Mass Index (BMI)
def get_trained_model():
    weights_file = '../Models/BMI_Model/bmi_model_weights.h5'
    model = get_model(ignore_age_weights=True)
    model.load_weights(weights_file)
    return model

#Predicts BMI for a given image
def predict_bmi():
    model = get_trained_model()
    print 'Loading model to detect BMI.'

    last_seen_bmis = []
    detector = dlib.get_frontal_face_detector()

    img = cv2.imread('../Data/Photos/evyan.whitney/2016-07-19_01-35-30_UTC.jpg',0)

    input_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    img_h, img_w, _ = np.shape(input_img)

    detected = detector(input_img, 1)
    faces = np.empty((len(detected), config.RESNET50_DEFAULT_IMG_WIDTH, config.RESNET50_DEFAULT_IMG_WIDTH, 3))

    if len(detected) > 0:
        for i, d in enumerate(detected):
            x1, y1, x2, y2, w, h = d.left(), d.top(), d.right() + 1, d.bottom() + 1, d.width(), d.height()
            xw1 = max(int(x1 - config.MARGIN * w), 0)
            yw1 = max(int(y1 - config.MARGIN * h), 0)
            xw2 = min(int(x2 + config.MARGIN * w), img_w - 1)
            yw2 = min(int(y2 + config.MARGIN * h), img_h - 1)
            cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 0), 2)
            faces[i, :, :, :] = cv2.resize(input_img[yw1:yw2 + 1, xw1:xw2 + 1, :], (config.RESNET50_DEFAULT_IMG_WIDTH, config.RESNET50_DEFAULT_IMG_WIDTH)) / 255.00

        predictions = model.predict(faces)

        print(predictions)

#Main function
def main():
    predict_bmi()

#Calling Main function
if __name__ == '__main__':
    main()
