#This file Preprocesses the "Multi-label Categorization of Accounts of Sexism using a Neural Framework" Dataset
#And converts it to fasttext training data format. This dataset can be accessed by approaching the 
#Authors of this paper - https://arxiv.org/abs/1910.04602
#Save the data.tsv file in IG-Misogyny-Classification/Data/TrainingComments

import pandas as pd
from text_preprocessor import *
import json
import random

#Loads the Dataframe
def read_df():
    filename = "../Data/TrainingComments/data.tsv"   
    return pd.read_csv(filename, sep='\t', header=0)

def save_fasttext_format(df):
    f = open('../Data/TrainingComments/train_comments.txt', 'a')
    for index in range(0,df.shape[0]):
        labels = df[['labels']].values[index][0].split(",")
        comment = df[['post']].values[index][0]
        text = ""
        label_arr = []
        for label in labels:
            new_label = label.strip()
            new_label = new_label.replace(" ", "_")
            new_label = "__label__" + new_label
            label_arr.append(new_label)
        
        for label in label_arr:
            text = text + label + " "
        
        text = text + comment + "\n"
        f.write(text)
    f.close()
    return

#This function extracts non-sexist comments from annotated Evyan Whitney file
def extract_nonsexist_comments(shortcode, username):
    excel_file = pd.read_excel("../Data/CommentsExcel/" + username + "/" + shortcode + ".xlsx")
    excel_file.rename(columns = {'Unnamed: 0':'index'}, inplace = True) 
    return excel_file.loc[excel_file['class'] == 0][['class', 'comment']]

#Returns all the annotated comments for a given user [We need Evyan Whitney Comments here]
def load_annotated_comments(username):
    userwise_annotated_comments = []
    shortcodes = []
    with open("../Data/Posts_list/" + username + ".json") as f:
        shortcodes = json.load(f)
    
    for shortcode in shortcodes:
        userwise_annotated_comments.append(extract_nonsexist_comments(shortcode, username))
    
    return pd.concat(userwise_annotated_comments)

#This function concatenates 1000 random non-sexist comments from Evyan Whitney's annotated data to training data
#This is done because the original dataset doesn't have Non-Sexist Data
def save_nonsexist():
    non_sexist_dataframes = []

    usernames = ['evyan.whitney']
    
    for username in usernames:
        non_sexist_dataframes.append(load_annotated_comments(username))
    
    non_sexist_comments = pd.concat(non_sexist_dataframes)
    #Choosing 1000 random comments
    random_non_sexist = random.choices(non_sexist_comments.values, k=1000)

    data = []
    for comment in random_non_sexist:
        data.append([comment[1], "Non-Sexist"])
    
    df = pd.DataFrame(data, columns = ['post', 'labels'])
    df = preprocess(df)
    df = remove_empty_string_columns(df)
    save_fasttext_format(df)

#Main function
def main():
    data = read_df()
    data = preprocess(data)
    data = remove_empty_string_columns(data)
    #Saving the training data
    save_fasttext_format(data)
    save_nonsexist()

if __name__=="__main__": 
    main() 