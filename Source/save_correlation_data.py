import os
import json
import pandas as pd
from collections import Counter 
import random

#Global Indexing Dictionaries to mark from Text Label to a numeric value
comment_label_dict = {} 
emotion_label_dict = {}
race_label_dict = {}
clothing_label_dict = {}

with open("../Data/CorrelationData/clothing_label_dict.json", "r") as f:
    clothing_label_dict = json.load(f)

with open("../Data/CorrelationData/comment_label_dict.json", "r") as f:
    comment_label_dict = json.load(f)

with open("../Data/CorrelationData/race_label_dict.json", "r") as f:
    race_label_dict = json.load(f)

with open("../Data/CorrelationData/emotion_label_dict.json", "r") as f:
    emotion_label_dict = json.load(f)

#Returns a weighted vector scaled to 1. Each value in the vector is a weighted value based on the 
#frequency of comments for a sexist label. The order is based on comment label dict
def return_comment_vector(username, shortcode):
    parent_dir = "../Data/ClassifiedComments/"
    comment_dir = os.path.join(parent_dir, username)
    excel_file = os.path.join(comment_dir, shortcode + ".xlsx")

    comments_df = pd.read_excel(excel_file)
    label_freq_dict = {}

    for label in comment_label_dict.keys():
        label_freq_dict[label] = 0

    for index, row in comments_df.iterrows():    
        #Some Comments weren't classified (due to an unknown error). These are ignored.
        if isinstance(row['labels'], str):
            labels = row['labels'].split(",")
            for label in labels:
                #Ignoring Non-Sexist Labels
                if label != "__label__Non-Sexist":
                    label_freq_dict[label] += 1

    label_vector = []
    
    total_sexist_freq = 0 
    for label in label_freq_dict.keys():
        total_sexist_freq += label_freq_dict[label]
        label_vector.append(float(label_freq_dict[label]))
    
    if total_sexist_freq != 0:
        label_vector[:] = [x / total_sexist_freq for x in label_vector]

    return label_vector

#Returns a list of dictionaries containing X values (Image Features) and Y values (Top 3 frequently occuring sexist comment labels)
def get_X_Y(username):
    img_feats_dir = "../Data/ImagesFeatures"
    user_excel = os.path.join(img_feats_dir, username + ".xlsx")    
    
    image_features_user = pd.read_excel(user_excel)
    
    user_correlation_data = []
    #Reading image features for a given image 
    #(Note: Its  is not for given shortcode, as each shortcode may have multiple images)
    for index, row in image_features_user.iterrows():
        age = row['Age']
        race = row['Ethnicity']
        bmi = row['BMI']
        emotion = row['Emotion']
        clothing = row['Clothing']
        shortcode = row['shortcode']

        #To avoid errors that come up due to errors in downloading the some comment files
        if os.path.isfile("../Data/ClassifiedComments/" + username + "/" + shortcode + ".xlsx"):
            X_val = [age, race, emotion, bmi, clothing]
            Y_val = return_comment_vector(username, shortcode)

            user_correlation_data.append({"x": X_val, "y": Y_val})

    return user_correlation_data

#Main function
def main(): 
    correlation_data = []
    with open('../Data/usernames.txt') as f:
        usernames = f.readlines()

    usernames = [x.strip() for x in usernames]

    for username in usernames:
        print("Loading Data files for user %s" %(username))
        correlation_data.extend(get_X_Y(username))

    #Assigning the numerical values to the classes based on the global dict values 
    # [need not be done for comments as it is a full sized vector with weights]
    for value in correlation_data:
        value['x'][1] = race_label_dict[value['x'][1]]
        value['x'][2] = emotion_label_dict[value['x'][2]]
        clothings = value['x'][4].split(",")

        for i in range(0,len(clothings)):
            clothings[i] = clothing_label_dict[clothings[i]]

        value['x'][4] = clothings
                
    #Shuffling the data
    random.shuffle(correlation_data)
    
    with open("../Data/CorrelationData/data.json", "w") as f:
        json.dump(correlation_data, f)

if __name__=="__main__": 
    main() 