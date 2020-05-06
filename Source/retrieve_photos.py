from itertools import islice
from math import ceil
from instaloader import Instaloader, Profile, Post
import time
import json

#Download posts for a given username by retrieving its list of shortcodes
def download_photos(username):
    L = Instaloader(download_videos = False, download_video_thumbnails = False, download_comments = False, compress_json = False, dirname_pattern = "../Data/Photos/{target}")

    posts = []
    with open("../Data/Posts_list/" + username + ".json") as f:
        posts = json.load(f)

    for post in posts:
        post = Post.from_shortcode(L.context, post)
        L.download_post(post, username)

#Main function
def main():

    with open('../Data/usernames.txt') as f:
        usernames = f.readlines()

    usernames = [x.strip() for x in usernames]

    for username in usernames:
        print("Downloading Photos for %s" %(username))
        download_photos(username)
        print("\n\n")
        print("Download for %s finished" %(username))
        print("============================================================================")

#Calling Main function
if __name__== "__main__":
    main()
