import pandas as pd
import json
import os

#Reads all the shortcode.json files for a given username and saves it in excel format.
#These excel files can now be used for the purpose of misogyny class annotation
def create_excel(username):
    comments = []

    JSON_parent_dir = os.path.join("../Data/CommentsJSON", username)
    Excel_parent_dir = os.path.join("../Data/CommentsExcel", username)
    shortcodes_file = os.path.join("../Data/Posts_list", username + ".json")

    os.mkdir(Excel_parent_dir)

    shortcodes = []
    with open(shortcodes_file) as f:
        shortcodes = json.load(f)

    for shortcode in shortcodes:

        json_file = os.path.join(JSON_parent_dir, shortcode + ".json")
        excel_file = os.path.join(Excel_parent_dir, shortcode + ".xlsx")

        with open(json_file) as f:
            comments = json.load(f)

        dataframe_format_comments = []

        for username in comments.keys():
            dataframe_format_comments.append({"username" : username, "comment": comments[username], "class": ""})

        df = pd.DataFrame(dataframe_format_comments)
        df.to_excel(excel_file)

    return

#Main function
def main():
    with open('../Data/usernames.txt') as f:
        usernames = f.readlines()

    usernames = [x.strip() for x in usernames]

    for username in usernames:
        print("Saving Comments for %s in excel format" %(username))
        create_excel(username)

#Calling Main function
if __name__== "__main__":
    main()
