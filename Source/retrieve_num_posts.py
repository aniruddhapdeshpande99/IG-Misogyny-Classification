# importing libraries
from bs4 import BeautifulSoup
import requests

# instagram URL
URL = "https://www.instagram.com/{}/"

# parse function
def parse_data(s):

    # creating a dictionary
    data = {}

    # splittting the content
    # then taking the first part
    s = s.split("-")[0]

    # again splitting the content
    s = s.split(" ")

    # assigning the values
    data['Followers'] = s[0]
    data['Following'] = s[2]
    data['Posts'] = s[4]

    # returning the dictionary
    return data

# scrape function
def scrape_data(username):

    # getting the request from url
    r = requests.get(URL.format(username))

    # converting the text
    s = BeautifulSoup(r.text, "html.parser")

    # finding meta info
    meta = s.find("meta", property ="og:description")

    # calling parse method
    return parse_data(meta.attrs['content'])

# main function
if __name__=="__main__":

    with open('../Data/usernames.txt') as f:
        usernames = f.readlines()

    #Retrieving list of usernames
    usernames = [x.strip() for x in usernames]
    num_posts = []

    for username in usernames:
        user_data = scrape_data(username)
        num_posts.append(user_data['Posts'])

    for post in num_posts:
        with open('../Data/num_posts.txt', 'a') as the_file:
            the_file.write(post+"\n")
