import cv2
import sys
import dlib
import numpy as np
from contextlib import contextmanager
import urllib2
from bmi_model import get_model
import bmi_config as config
import pandas as pd
import os
import sys
import json

#Retrieves Pretrained model to predict Body Mass Index (BMI)
def get_trained_model():
    weights_file = '../Models/BMI_Model/bmi_model_weights.h5'
    model = get_model(ignore_age_weights=True)
    model.load_weights(weights_file)
    return model

#Predicts BMI for a given image
def predict_bmi(img_path, model):
    detector = dlib.get_frontal_face_detector()

    img = cv2.imread(img_path,0)

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

        predictions_list = []

        for prediction in predictions:
            predictions_list.append(prediction[0])
        
        final_bmi = round(np.mean(predictions_list), 3)
        
        return final_bmi

    else:
        print("No Face detected, please ensure that the image doesn't include picture without a face or a partially covered Face")
        print("If you would still like to run the classifier, please enter your BMI. Press 'N/n' to exit.")
        bmi_val = raw_input()

        if bmi_val == "n" or bmi_val == "N":
            sys.exit("Exiting")
        
        try:
            bmi_val = float(bmi_val)
            return bmi_val
        except:
            print("Error: Value entered for BMI is not a numerical value. Exiting")
            sys.exit(2)

#Main function
def main():
    input_args = sys.argv
    if len(input_args) != 2:
        print("Usage: python main_part1.py <image_path>")
        sys.exit(2)
    
    if os.path.isfile(input_args[1]):
        print("Loading BMI Model")
        model = get_trained_model()
        image_path = input_args[1]
        temp_json_path = "../Data/temp_input.json"
        X = {image_path: list(np.zeros(6))}
        X[image_path][3] = predict_bmi(image_path, model)
        with open(temp_json_path, "w") as f:
            json.dump(X, f)
        print("BMI Features Saved. Please run main_part2.py to add other Image features and get final classification")
    else:
        print("Error: File Doesn't Exist. Check the Image Path")
        sys.exit(2)

#Calling Main function
if __name__== "__main__":
    main()

