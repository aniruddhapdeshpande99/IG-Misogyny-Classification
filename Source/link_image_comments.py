import json
import os

#Filename for a post are not the same as the shortcode, therefore they need to be linked
#This function returns the shortcode from the Image Metadata JSON
def link_shortcodes_jsonfile(json_files, username):
    shortcode_dict = {}
    img_metadata_dir = os.path.join("../Data/Photos/", username)

    for file in json_files:
        file_path = os.path.join(img_metadata_dir, file)
        img_metadata = {}
        with open(file_path) as f:
            img_metadata = json.load(f)
        shortcode_dict[file] = img_metadata['node']['shortcode']

    return shortcode_dict

#Filename for the Image Metadata JSON file is a substring within each image for that post
#This function returns paths for images for a given post using the Metadata JSON file names
def link_imgs_jsonfile(json_files, jpg_files, username):
    imgs_dict = {}
    img_dir = os.path.join("../Data/Photos/", username)

    for file in json_files:
        img_arr = []
        file_name = file.replace(".json", "")
        for img in jpg_files:
            if file_name in img:
                img_arr.append(os.path.join(img_dir, img))

        imgs_dict[file] = img_arr

    return imgs_dict

#This function links the shortcode to its respective list of image paths for a given user
def retrieve_metadata(username):

    shortcodes_file = os.path.join("../Data/Posts_list", username + ".json")
    shortcodes = []
    with open(shortcodes_file) as f:
        shortcodes = json.load(f)

    images_dir = os.path.join("../Data/Photos/", username)
    json_files = [pos_json for pos_json in os.listdir(images_dir) if pos_json.endswith('.json')]
    jpg_files = [pos_jpg for pos_jpg in os.listdir(images_dir) if pos_jpg.endswith('.jpg')]

    shortcode_dict = link_shortcodes_jsonfile(json_files, username)
    imgs_dict = link_imgs_jsonfile(json_files, jpg_files, username)

    user_metadata = []
    for key in shortcode_dict:
        user_metadata.append({'shortcode' : shortcode_dict[key], 'images_path' : imgs_dict[key]})

    return user_metadata

#Saves metadata for a user
def save_user_metadata(username):
    user_metadata = retrieve_metadata(username)
    metadata_parent_dir = "../Data/Metadata"
    user_metadata_file = os.path.join(metadata_parent_dir, username + ".json")
    with open(user_metadata_file, "w") as f:
        json.dump(user_metadata, f)

#Main function
def main():
    with open('../Data/usernames.txt') as f:
        usernames = f.readlines()

    usernames = [x.strip() for x in usernames]

    for username in usernames:
        print("Saving Metadata for %s" %(username))
        save_user_metadata(username)

#Calling Main function
if __name__== "__main__":
    main()
