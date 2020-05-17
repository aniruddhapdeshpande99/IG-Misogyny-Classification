import pandas as pd
import json
import os
from deepface import DeepFace
from deepface.extendedmodels import Age, Race, Emotion
import numpy as np

#Loading Deepface demographics models
models = {}
models["emotion"] = Emotion.loadModel()
models["age"] = Age.loadModel()
models["race"] = Race.loadModel()

#Adds Demographic Features - Age, Emotion, Race into dataframe
def add_demographic_features(df):
    for index, row in df.iterrows():
        image_path = row['image_path']
        try:
            demography = DeepFace.analyze(image_path, ['age', 'race', 'emotion'], models=models)
            df.loc[index, "Age"] = int(round(demography["age"]))
            df.loc[index, "Emotion"] = demography["dominant_emotion"]
            df.loc[index, "Ethnicity"] = demography["dominant_race"]
            print("%d. Image %s analyzed" %(index, image_path))
        except:
            print("%d. Face couldn't be detected in Image %s. Ignoring." %(index, image_path))
    
    return df


#The Images wherein face isn't detected (say wherein face is obstructed by a person's hand) need to be assigned
#A default value wrt to the user. The default values are assigned as follows:
#Ethnicity - Most Commonly occuring Ethnicity is assigned as default
#Emotion - Most Common occuring Emotion is assigned as default
#Age - Average Age is assigned as default
def add_default_demographics(df):
    user_races = []
    user_emotions = []
    user_ages = []

    for index, row in df.iterrows():
        if row['Age']:
            user_ages.append(row['Age'])
            user_races.append(row['Ethnicity'])
            user_emotions.append(row['Emotion'])

    avg_age = int(round(np.mean(user_ages))) #Average Age
    most_common_race = max(user_races,key=user_races.count) #Most commonly occuring Ethnicity/Race
    most_common_emotion = max(user_emotions,key=user_emotions.count) #Most commonly occuring Emotion

    for index, row in df.iterrows():
        if row['Age'] == "":
            df.loc[index, "Age"] = avg_age
            df.loc[index, "Ethnicity"] = most_common_race
            df.loc[index, "Emotion"] = most_common_emotion

    return df

#Reads metadata linking Image to Shortcode. Loads the images for the user and saves all the
#images' features related to demographics for a given user
def save_img_feats_demographics(username):
    metadata_dir = "../Data/Metadata/"
    images_features_file = "../Data/ImagesFeatures/" + username + ".xlsx"
    json_file = username + ".json"

    user_json = os.path.join(metadata_dir, json_file)

    user_metadata = []
    with open(user_json, "r") as f:
        user_metadata = json.load(f)
    
    image_features = []
    for post in user_metadata:
        images_path = post['images_path'] 
        if len(images_path) != 0:
            for image in images_path:
                image_features.append([image, post['shortcode'], "", "", "", "", ""])

    image_features_df = pd.DataFrame(image_features, columns = ['image_path', 'shortcode', "Age", "Ethnicity", "Emotion", "BMI", "Clothing"])
    image_feats_with_demographics = add_demographic_features(image_features_df)
    final_demographic_features = add_default_demographics(image_feats_with_demographics)
    
    final_demographic_features.to_excel(images_features_file, index=False)
    return


#Main function
def main():
    with open('../Data/usernames.txt') as f:
        usernames = f.readlines()

    usernames = [x.strip() for x in usernames]

    for username in usernames[:1]:
        save_img_feats_demographics(username)
        print("Demographic Features for %s created. Image Features Excel file created." %(username))
        print("\n\n\n")
        print("============================================================================")


if __name__=="__main__": 
    main() 