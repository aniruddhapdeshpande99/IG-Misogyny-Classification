import fasttext
import json
import pandas as pd
import os
from text_preprocessor import *

#Creates Dataframe using list of comments
def create_comments_df(comments):
    data = []
    for comment in comments:
        data.append([comment, ""])
    
    df = pd.DataFrame(data, columns = ['post', 'labels'])
    return df

#Classifies each comment on a post and stores it an excel file with title "shortcode.xlsx"
def classify_post_comments(username, shortcode, model):
    comments_dict = {}
    json_path = "../Data/CommentsJSON/" + username + "/" + shortcode + ".json"
    excel_path = "../Data/ClassifiedComments/" + username + "/" + shortcode + ".xlsx"

    #To check if file exists or not. 
    #(To tackle issues that the comments scraper may have gone through which led to file not downloading)
    if os.path.isfile(json_path):
        #loading the comments
        with open(json_path, "r") as f:
            comments_dict = json.load(f)
    
        #Converting comments to Dataframe and preprocessing it
        comments = list(list(comments_dict.values()))
        comments_df = create_comments_df(comments)
        preprocessed_comments_df = remove_empty_string_columns(preprocess(comments_df))

        #Predicting labels for each comment
        for index, row in preprocessed_comments_df.iterrows():
            comment = row['post']
            predictions = model.predict(comment, k=5, threshold=0.1) #Top 5 labels retrieved with a prediction threshold of 0.1
        
            #No Prediction
            if len(predictions[0]) == 0:
                preprocessed_comments_df.drop([index])
        
            else:
                #If Non-sexist comment, don't consider other labels
                if predictions[0][0] == "__label__Non-Sexist":
                    row['labels'] = predictions[0][0]
        
                else:
                    row['labels'] = ','.join(predictions[0])
    
        #Storing the dataframe with classified comments into the excel file
        preprocessed_comments_df.to_excel(excel_path)

        print("Classified Comments for post with shortcode %s stored" %(shortcode))
    
    else:
        print("Comments JSON file for post with shortcode %s doesn't exist. Ignoring." %(shortcode))

    return
    
#Creates the directory for a user in the ClassifiedComments Directory and calls above function to store 
#Classified comments for each post for that user
def userwise_classify(username, model):
    parent_dir = "../Data/ClassifiedComments/"
    comment_dir = os.path.join(parent_dir, username)
    os.mkdir(comment_dir)

    shortcodes = []
    with open("../Data/Posts_list/" + username + ".json") as f:
        shortcodes = json.load(f)
    
    for shortcode in shortcodes:
        classify_post_comments(username, shortcode, model)
    return

#Main function - Loads all usernames and the comment classifier model and calls the above
#funtion for all users
def main():

    classifier_model = fasttext.load_model("../Models/model_comments_classifier.bin")

    with open('../Data/usernames.txt') as f:
        usernames = f.readlines()

    usernames = [x.strip() for x in usernames]

    for username in usernames:
        print("Classifying Comments for %s" %(username))
        userwise_classify(username, classifier_model)
        print("\n\n")
        print("Comments for all posts of %s classified successfully" %(username))
        print("============================================================================")

if __name__=="__main__":
    main()
