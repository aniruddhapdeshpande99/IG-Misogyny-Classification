from keras.models import load_model
from keras.preprocessing import image
from keras.optimizers import SGD
from tensorflow.keras.applications.resnet50 import preprocess_input, decode_predictions
import numpy as np
import heapq
import json
import os
import pandas as pd

print("Loading Index dictionary for Clothing")
clothing_index = {}
with open("../Data/CorrelationData/clothing_label_dict.json", "r") as f:
    clothing_index = json.load(f)
inv_clothing_index = {v: k for k, v in clothing_index.items()}


#Retrieves Pretrained model to predict clothing classes
def get_trained_model():
    # load the model we saved
    model = load_model('../Models/clothing_model.h5')
    opt = SGD(lr=0.0001, momentum=0.9, nesterov=True)
    model.compile(optimizer=opt,
                    loss={'img': 'categorical_crossentropy',
                          'bbox': 'mean_squared_error'},
                    metrics={'img': ['accuracy', 'top_k_categorical_accuracy'], # default: top-5
                             'bbox': ['mse']})
    
    return model


#Predict the clothing category based on the pretrained model. Top 2 predictions are returned.
def predict_clothing(img_path, model):
    #dimensions of our images
    img_width, img_height = 200, 200

    #predicting images
    img = image.load_img(img_path, target_size=(img_width, img_height))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)

    #Retrieve the predicted value
    y = model.predict(x)
    return heapq.nlargest(2, range(len(y[0][0])), y[0][0].__getitem__)

#Adding clothing features to a user's image features
def add_clothing(username, model):
    image_features_df = pd.read_excel("../Data/ImagesFeatures/" + username + ".xlsx")
    for index, row in image_features_df.iterrows():
        image_path = row['image_path']
        print("Calculating Clothing for %s" %(image_path))
        clothing_labels = predict_clothing(image_path, model)

        for i in range(0, len(clothing_labels)):
            clothing_labels[i] = inv_clothing_index[clothing_labels[i]]

        image_features_df.loc[index, "Clothing"] = ",".join(clothing_labels)
        
    return image_features_df


#Main function
def main():
    model = get_trained_model()
    print('Loading model to predict clothing feature.')

    with open('../Data/usernames.txt') as f:
        usernames = f.readlines()

    usernames = [x.strip() for x in usernames]

    for username in usernames:
        img_features_with_clothing = add_clothing(username,model)
        img_features_with_clothing.to_excel("../Data/ImagesFeatures/" + username + "_clothing.xlsx", index = False)
        os.remove("../Data/ImagesFeatures/" + username + ".xlsx")
        os.rename("../Data/ImagesFeatures/" + username + "_clothing.xlsx", "../Data/ImagesFeatures/" + username + ".xlsx")
        print("Clothing values for %s added. Excel file for Image features modified." %(username))
        print("\n\n\n")
        print("============================================================================")

#Calling Main
if __name__ == "__main__":
    main()


