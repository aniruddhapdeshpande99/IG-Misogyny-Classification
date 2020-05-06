from selenium import webdriver
import time
import sys
import json
import os

#Function that returns about 10K comments for a given post
def return_comments(post_url):
    driver = webdriver.Chrome("../Resources/SeleniumDriver/chromedriver")
    driver.get(post_url)
    time.sleep(3)

    #if user not logined
    try:
        close_button = driver.find_element_by_class_name('xqRnw')
        close_button.click()
    except:
        pass


    try:
        load_more_comment = driver.find_element_by_css_selector('.MGdpg > button:nth-child(1)')
        print("Found {}".format(str(load_more_comment)))
        i = 0
        while load_more_comment.is_displayed() and i < 70:
            load_more_comment.click()
            time.sleep(1.5)
            load_more_comment = driver.find_element_by_css_selector('.MGdpg > button:nth-child(1)')
            print("Found {}".format(str(load_more_comment)))
            i += 1
    except Exception as e:
        print(e)
        pass

    user_names = []
    user_comments = []
    comment = driver.find_elements_by_class_name('gElp9 ')
    for c in comment:
        container = c.find_element_by_class_name('C4VMK')
        name = container.find_element_by_class_name('_6lAjh').text
        content = container.find_element_by_tag_name('span').text
        content = content.replace('\n', ' ').strip().rstrip()
        user_names.append(name)
        user_comments.append(content)

    user_names.pop(0)
    user_comments.pop(0)

    driver.close()

    return user_names, user_comments

#Returns a dict mapping the author of the comment and the comment itself
def make_dict(usernames, comments):
    comment_dict = {}
    for index in range(0, len(usernames)):
        username = usernames[index]
        comment = comments[index]
        comment_dict[username] = comment

    return comment_dict

#Saving comments for each post for a given username
def save_comments(username):
    parent_dir = "../Data/Comments/"
    comment_dir = os.path.join(parent_dir, username)
    os.mkdir(comment_dir)

    shortcodes = []
    with open("../Data/Posts_list/" + username + ".json") as f:
        shortcodes = json.load(f)

    for shortcode in posts:
        comment_usernames, comments = return_comments("https://www.instagram.com/p/" + shortcode + "/")
        comment_dict = make_dict(comment_usernames, comments)

        with open (comment_dir + "/" + shortcode + ".json", "w") as f:
            json.dump(comment_dict, f)


#Main function
def main():

    with open('../Data/usernames.txt') as f:
        usernames = f.readlines()

    usernames = [x.strip() for x in usernames]

    for username in usernames:
        print("Downloading Comments for %s" %(username))
        save_comments(username)
        print("\n\n")
        print("Download for %s finished" %(username))
        print("============================================================================")


#Calling Main function
if __name__== "__main__":
    main()
