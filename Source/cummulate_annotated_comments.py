import pandas as pd
import json

#Extracts annotated comments for a given post of a user. 
#This function also Removes the 0 class - ie. Non Sexist class. 
def extract_sexist_comments(shortcode, username):
    excel_file = pd.read_excel("../Data/CommentsExcel/" + username + "/" + shortcode + ".xlsx")
    excel_file.rename(columns = {'Unnamed: 0':'index'}, inplace = True)
    excel_file["class"].replace({0: None}, inplace=True) 
    bool_series = pd.notnull(excel_file["class"]) 
    return excel_file[bool_series][['class', 'comment']]

#Returns all the annotated comments for a given user
def userwise_extract_comments(username):
    userwise_annotated_comments = []
    shortcodes = []
    with open("../Data/Posts_list/" + username + ".json") as f:
        shortcodes = json.load(f)
    
    for shortcode in shortcodes:
        userwise_annotated_comments.append(extract_sexist_comments(shortcode, username))
    
    return pd.concat(userwise_annotated_comments)

#Main function
def main():
    
    final_dataframes = []
    with open('../Data/usernames.txt') as f:
        usernames = f.readlines()

    usernames = [x.strip() for x in usernames]
    
    for username in usernames:
        final_dataframes.append(userwise_extract_comments(username))
    
    final_annotated_comments = pd.concat(final_dataframes)
    print(final_annotated_comments)

#Calling Main function
if __name__== "__main__":
    main()