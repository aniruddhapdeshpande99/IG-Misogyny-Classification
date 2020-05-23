import pandas as pd
import json
import os
from deepface import DeepFace
from deepface.extendedmodels import Age, Race, Emotion
import numpy as np
from keras.models import load_model
from keras.preprocessing import image
from keras.optimizers import SGD
from tensorflow.keras.applications.resnet50 import preprocess_input, decode_predictions
import heapq
import sys
import pickle
import operator

#Loading the global index dictionaries for Demographic, Clothing and Sexist Comment Categories
race_index = {}
with open("../Data/CorrelationData/race_label_dict.json") as f:
    race_index = json.load(f)

inv_race_index = {v: k for k, v in race_index.items()} 
    
emotion_index = {}
with open("../Data/CorrelationData/emotion_label_dict.json") as f:
    emotion_index = json.load(f)

inv_emotion_index = {v: k for k, v in emotion_index.items()}

comment_index = {}
with open("../Data/CorrelationData/comment_label_dict.json") as f:
    comment_index = json.load(f)

inv_comment_index = {v: k for k, v in comment_index.items()}

clothing_index = {}
with open("../Data/CorrelationData/clothing_label_dict.json") as f:
    clothing_index = json.load(f)

inv_clothing_index = {v: k for k, v in clothing_index.items()}

#Retrieves Pretrained model to predict clothing classes
def get_trained_model():
    # load the model we saved
    model = load_model('../Models/clothing_model.h5')
    opt = SGD(lr=0.0001, momentum=0.9, nesterov=True)
    model.compile(optimizer=opt,
                    loss={'img': 'categorical_crossentropy',
                          'bbox': 'mean_squared_error'},
                    metrics={'img': ['accuracy', 'top_k_categorical_accuracy'], # default: top-5
                             'bbox': ['mse']})
    
    return model

#Adds Demographic Features - Age, Emotion, Race for the input image
def add_demographic_features(image_path, models):
    try:
        demography = DeepFace.analyze(image_path, ['age', 'race', 'emotion'], models=models)
        age = int(round(demography["age"]))
        emotion = emotion_index[demography["dominant_emotion"]]
        race = race_index[demography["dominant_race"]]
        print("Demographic Features Added.")
        return age, race, emotion
    except:
        print("No Face detected, please ensure that the image doesn't include picture without a face or a partially covered Face")
        print("Press Y/y to add these features manually or press any other key to exit")
        choice = input()
        if choice == "Y" or choice == "y":
            age = input("Enter your age:")
            try:
                age = int(age)
            except:
                print("Error: Age value entered is not a numeric value. Exiting.")
                sys.exit(2)
            
            print("Following are the supported race classes. Please enter the appropriate number which best matches the person in the image")
            print("0: black, 1: latino hispanic, 2: middle eastern, 3: asian, 4: white, 5: indian")
            race = input("Enter the race class: ")
            try:
                race = int(race)
                if not (race >= 0 and race <= 5):
                    sys.exit(2)
            except:
                print("Error: Please enter a numerical value between 0 and 5 as per the index. Exiting")
                sys.exit(2)
            
            print("Following are the supported emotion classes. Please enter the appropriate number which best matches the person in the image")
            print("0: neutral, 1: sad, 2: happy, 3: surprise, 4: angry, 5: fear, 6: disgust")
            emotion = input("Enter the emotion class: ")
            try:
                emotion = int(emotion)
                if not (emotion >= 0 and emotion <= 6):
                    sys.exit(2)
            except:
                print("Error: Please enter a numerical value between 0 and 6 as per the index. Exiting")
                sys.exit(2)
            
            return age, race, emotion
        
        else:
            print("Exiting")
            sys.exit()

#Predict the clothing category based on the pretrained model. Top 2 predictions are returned.
def predict_clothing(img_path, model):
    #dimensions of our images
    img_width, img_height = 200, 200

    #predicting images
    img = image.load_img(img_path, target_size=(img_width, img_height))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)

    #Retrieve the predicted value
    y = model.predict(x)
    clothing_labels = heapq.nlargest(2, range(len(y[0][0])), y[0][0].__getitem__)
    print("Clothing Features Addded.")
    return clothing_labels[0], clothing_labels[1]

#Loads all the correlation regression networks and predicts top labels    
def top_comment_predictions(image_features):
    print("Loading Image feature - Comment Label Correlation Models")
    rand_forest = pickle.load(open("../Models/Final_Classifier_Models/rand_forest.sav", 'rb'))
    dec_tree = pickle.load(open("../Models/Final_Classifier_Models/dec_tree.sav", 'rb'))
    knn = pickle.load(open("../Models/Final_Classifier_Models/knn.sav", 'rb'))
    lin_reg = pickle.load(open("../Models/Final_Classifier_Models/lin_reg.sav", 'rb'))
    mlp = pickle.load(open("../Models/Final_Classifier_Models/mlp.sav", 'rb'))
    grad_boost = pickle.load(open("../Models/Final_Classifier_Models/grad_boost.sav", 'rb'))

    rand_forest_prediction = list(rand_forest.predict([image_features])[0])
    rand_forest_prediction = list(zip(*heapq.nlargest(3, enumerate(rand_forest_prediction), key=operator.itemgetter(1))))[0]

    dec_tree_prediction = list(dec_tree.predict([image_features])[0])
    dec_tree_prediction = list(zip(*heapq.nlargest(3, enumerate(dec_tree_prediction), key=operator.itemgetter(1))))[0]

    knn_prediction = list(knn.predict([image_features])[0])
    knn_prediction = list(zip(*heapq.nlargest(3, enumerate(knn_prediction), key=operator.itemgetter(1))))[0]

    lin_reg_prediction = list(lin_reg.predict([image_features])[0])
    lin_reg_prediction = list(zip(*heapq.nlargest(3, enumerate(lin_reg_prediction), key=operator.itemgetter(1))))[0]

    mlp_prediction = list(mlp.predict([image_features])[0])
    mlp_prediction = list(zip(*heapq.nlargest(3, enumerate(mlp_prediction), key=operator.itemgetter(1))))[0]

    grad_boost_prediction = list(grad_boost.predict([image_features])[0])
    grad_boost_prediction = list(zip(*heapq.nlargest(3, enumerate(grad_boost_prediction), key=operator.itemgetter(1))))[0]

    preds = [rand_forest_prediction, dec_tree_prediction, knn_prediction, lin_reg_prediction, mlp_prediction, grad_boost_prediction]

    top_three_pred = {}

    for pred in preds:
        for label in pred:
            if label not in top_three_pred.keys():
                top_three_pred[label] = 1
            else:
                top_three_pred[label] += 1
    
    final_top_labels = heapq.nlargest(3, top_three_pred, key = top_three_pred.get)
    print("\n\n\n==================================================================")
    print("Top 3 Sexist Comment Categories that the image may be prone to are:\n")
    for label in final_top_labels:
        print(inv_comment_index[label].replace("__label__", ""))
    return 

#Main function
def main():
    input_args = sys.argv
    if len(input_args) != 2:
        print("Usage: python3 main_part2.py <image_path>")
        sys.exit(2)
    
    if os.path.isfile(input_args[1]):
        image_path = input_args[1]
        image_features_path = "../Data/temp_input.json"
        image_features = {}
        try:
            with open(image_features_path, "r") as f:
                image_features = json.load(f)
        except:
            print("Error: Please Run main_part1.py before running main_part2.py")
            sys.exit(2)
           
        orig_img_path = list(image_features.keys())[0]
        if orig_img_path != image_path:
            print("Error: Image Paths added to main_part1.py and main_part2.py don't match. Please add matching paths.")
            sys.exit(2)
        else:
            #Loading Deepface demographics models
            print("Loading Demographic Feature Extraction Model")
            models = {}
            models["emotion"] = Emotion.loadModel()
            models["age"] = Age.loadModel()
            models["race"] = Race.loadModel()
            
            image_features[image_path][0], image_features[image_path][1], image_features[image_path][2] = add_demographic_features(image_path, models)

            print("Loading Clothing Features Extraction Model")
            clothing_model = get_trained_model()

            image_features[image_path][4], image_features[image_path][5] = predict_clothing(image_path, clothing_model)
            with open(image_features_path, "w") as f:
                json.dump(image_features, f)
            top_comment_predictions(image_features[image_path])
            os.remove(image_features_path)
    else:
        print("Error: File Doesn't Exist. Check the Image Path")
        sys.exit(2)

#Calling Main function
if __name__== "__main__":
    main()