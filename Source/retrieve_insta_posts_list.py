from itertools import islice
from math import ceil
from instaloader import Instaloader, Profile
import time
import json

#Retrieves percentage amount of photos for a given a username. Max percentage is such that max number of
#photos to be downloaded is 60 (in main())
def retrieve_posts(username, num):
    PROFILE = username        # profile to download from

    L = Instaloader(download_videos = False, download_video_thumbnails = False, download_comments = True)

    profile = Profile.from_username(L.context, PROFILE)

    posts = profile.get_posts()

    posts_sorted_by_comments = sorted(posts,
                                   key=lambda p: p.comments,
                                   reverse=True)

    post_shortcodes = [x.shortcode for x in posts_sorted_by_comments]

    return post_shortcodes[:num]

#Cleans the numberings from the num_posts.txt (Removes commas and ks)
def clean_num(num_posts_all):
    num_posts_cleaned = []
    for num in num_posts_all:
        if "," in num:
            num_posts_cleaned.append(int(num.replace(",", "")))

        elif "k" in num:
            num  = num.replace("k", "")
            num = int(float(num)*1000)
            num_posts_cleaned.append(num)

        else:
            num_posts_cleaned.append(int(num))

    return num_posts_cleaned

#Main function
def main():
    #Starting Timer
    t0 = time.time()

    with open('../Data/usernames.txt') as f:
        usernames = f.readlines()

    usernames = [x.strip() for x in usernames]

    with open('../Data/num_posts.txt') as f:
        num_posts_all = f.readlines()

    num_posts_all = [x.strip() for x in num_posts_all]
    num_posts_all = clean_num(num_posts_all)


    #Sorting posts by comments and saving the list of posts
    for i in range(0, len(usernames)):
        username = usernames[i]
        if num_posts_all[i] <= 100:
            posts = retrieve_posts(username, num_posts_all[i])
        else:
            posts = retrieve_posts(username, 100)

        with open('../Data/Posts_list/' + username + ".json" , 'w') as f:
            json.dump(posts,f)

        print("Posts for %s added. | " %(username), end = "")
        print("Time elapsed: ", end = "")
        print(time.time()-t0)

    t1 = time.time()
    total_time = t1-t0

    #Ending the timer
    print("Total Time Elapsed", end = ' ')
    print(total_time)


#Calling Main function
if __name__== "__main__":
    main()
