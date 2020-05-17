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
        return ""

#Adds default BMI to all images where the above function couldn't detect a face. Default BMI = Avg (All BMIs)
def add_default_bmi(df):
    bmi_values = []
    for index, row in df.iterrows():
        if row['BMI']:
            bmi_values.append(row['BMI'])
    
    avg_bmi = round(np.mean(bmi_values), 3)

    for index, row in df.iterrows():
        if row['BMI'] == "":
            df.loc[index, "BMI"] = avg_bmi
    
    return df

#Adds BMI values to the Image Features excel file for a given user
def add_bmi(username, model):
    image_features_df = pd.read_excel("../Data/ImagesFeatures/" + username + ".xlsx")
    for index, row in image_features_df.iterrows():
        image_path = row['image_path']
        print("Calculating BMI for %s" %(image_path))
        image_features_df.loc[index, "BMI"] = predict_bmi(image_path, model)
    
    final_bmi_included_df = add_default_bmi(image_features_df)
    
    return final_bmi_included_df 

#Main function
def main():

    model = get_trained_model()
    print('Loading model to detect BMI.')

    with open('../Data/usernames.txt') as f:
        usernames = f.readlines()

    usernames = [x.strip() for x in usernames]

    for username in usernames[:1]:
        img_features_with_bmi = add_bmi(username,model)
        img_features_with_bmi.to_excel("../Data/ImagesFeatures/" + username + "_bmi.xlsx", index = False)
        os.remove("../Data/ImagesFeatures/" + username + ".xlsx")
        os.rename("../Data/ImagesFeatures/" + username + "_bmi.xlsx", "../Data/ImagesFeatures/" + username + ".xlsx")
        print("BMI values for %s added. Excel file for Image features modified." %(username))
        print("\n\n\n")
        print("============================================================================")

#Calling Main function
if __name__ == '__main__':
    main()
