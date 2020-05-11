import pandas as pd
import json
import numpy as np

#Extracts annotated comments for a given post of a user. 
#This function also Removes the 0 class - ie. Non Sexist class. 
def extract_nonsexist_comments(shortcode, username):
    excel_file = pd.read_excel("../Data/CommentsExcel/" + username + "/" + shortcode + ".xlsx")
    excel_file.rename(columns = {'Unnamed: 0':'index'}, inplace = True) 
    return excel_file.loc[excel_file['class'] == 0][['class', 'comment']]

#Returns all the annotated comments for a given user
def userwise_extract_comments(username):
    userwise_annotated_comments = []
    shortcodes = []
    with open("../Data/Posts_list/" + username + ".json") as f:
        shortcodes = json.load(f)
    
    for shortcode in shortcodes:
        userwise_annotated_comments.append(extract_nonsexist_comments(shortcode, username))
    
    return pd.concat(userwise_annotated_comments)

#Main function - Since Comments for Evyan Whitney were annotated, non sexist comments from that profile
#Are used to add to the "Multi-label Categorization of Accounts of Sexism using a Neural Framework" Dataset
#This is done because the above dataset only has sexist comments and hence will also classify a non sexist comment into a sexist category.
#These comments will then be useful for fasttext to also classify non hateful comments.
def main():
    
    non_sexist_dataframes = []

    usernames = ['evyan.whitney']
    
    for username in usernames:
        non_sexist_dataframes.append(userwise_extract_comments(username))
    
    non_sexist_comments = pd.concat(non_sexist_dataframes)
    print(non_sexist_comments.shape)

#Calling Main function
if __name__== "__main__":
    main()