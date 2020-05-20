import os
import json
import pandas as pd
from collections import Counter 
import random

#Global Indexing Dictionaries to mark from Text Label to a numeric value
comment_label_dict = {} 
emotion_label_dict = {}
race_label_dict = {}

#Returns top three frequently occuring sexist comment classes for a given post
def get_top_three_comment_labels(username, shortcode):
    parent_dir = "../Data/ClassifiedComments/"
    comment_dir = os.path.join(parent_dir, username)
    excel_file = os.path.join(comment_dir, shortcode + ".xlsx")

    comments_df = pd.read_excel(excel_file)
    label_freq_dict = {}

    for index, row in comments_df.iterrows():    
        #Some Comments weren't classified (due to an unknown error). These are ignored.
        if isinstance(row['labels'], str):
            labels = row['labels'].split(",")
            for label in labels:
                #Ignoring Non-Sexist Labels
                if label != "__label__Non-Sexist":
                    #Adding the label to the global dict of index dictionary
                    if label not in comment_label_dict.keys():
                        comment_label_dict[label] = ""
                
                    #Counting for each type of Sexist label for a given post 
                    if label not in label_freq_dict.keys():
                        label_freq_dict[label] = 0
                    else:
                        label_freq_dict[label] += 1

    # Finding top 3 frequently Sexist Labels 
    top_freq_labels = Counter(label_freq_dict).most_common(3)

    #Returning the labels without frequency values
    top_labels = []
    for value in top_freq_labels:
        top_labels.append(value[0])

    return top_labels

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
        shortcode = row['shortcode']

        #To avoid errors that come up due to errors in downloading the some comment files
        if os.path.isfile("../Data/ClassifiedComments/" + username + "/" + shortcode + ".xlsx"):
            #Adding values to global dict of race labels
            if race not in race_label_dict.keys():
                race_label_dict[race] = ""
        
            #Adding values to global dict of emotion labels
            if emotion not in emotion_label_dict.keys():
                emotion_label_dict[emotion] = ""
        
            X_val = [age, race, emotion, bmi]
            Y_val = get_top_three_comment_labels(username, shortcode)

            user_correlation_data.append({"x": X_val, "y": Y_val})

    return user_correlation_data

#Adds numeric values to the above global index dicts
def create_index():
    count = 0
    for key in emotion_label_dict.keys():
        emotion_label_dict[key] = count
        count += 1
    
    count = 0
    for key in race_label_dict.keys():
        race_label_dict[key] = count
        count += 1
    
    count = 0
    for key in comment_label_dict.keys():
        comment_label_dict[key] = count
        count += 1
    
    return


#Main function
def main(): 
    correlation_data = []
    with open('../Data/usernames.txt') as f:
        usernames = f.readlines()

    usernames = [x.strip() for x in usernames]

    for username in usernames:
        print("Loading Data files for user %s" %(username))
        correlation_data.extend(get_X_Y(username))
    
    #Creating the final index dictionary for the global dict values
    create_index()

    #Assigning the numerical values to the classes based on the global dict values
    for value in correlation_data:
        value['x'][1] = race_label_dict[value['x'][1]]
        value['x'][2] = emotion_label_dict[value['x'][2]]
        
        for index in range(0,len(value['y'])):
            value['y'][index] = comment_label_dict[value['y'][index]]

    #Shuffling the data
    random.shuffle(correlation_data)
    #Saving all the data
    with open("../Data/CorrelationData/race_label_dict.json", "w") as f:
        json.dump(race_label_dict, f)

    with open("../Data/CorrelationData/emotion_label_dict.json", "w") as f:
        json.dump(emotion_label_dict, f)

    with open("../Data/CorrelationData/comment_label_dict.json", "w") as f:
        json.dump(comment_label_dict, f)
    
    with open("../Data/CorrelationData/data.json", "w") as f:
        json.dump(correlation_data, f)

if __name__=="__main__": 
    main() 