# Instagram Misogyny Classification and Correlation

This aim of this project is to try and correlate Misogynistic comments for an Instagram Post to that of the features of a person within the photo. Further details about the project can be understood using the Final Report in the Documentation Folder.

### Getting Started

* The Folder - "Data/Photos" only has photos for one IG user. Please download the rest of the photos needed to create Image Features using this [link](https://iiitaphyd-my.sharepoint.com/:f:/g/personal/aniruddha_d_research_iiit_ac_in/EhDJlZVYuFZIgZzFx4uTafkBBWq6MhxOMzTK16jGZCkhzw?e=fkxZZR). This step can be avoided if you just want to use the main classifier as the training image feature dataset is already present in the repository.

* Download and place the Clothing Classifier (clothing_model.h5) in "Models" directory using this [link](https://iiitaphyd-my.sharepoint.com/:f:/g/personal/aniruddha_d_research_iiit_ac_in/EmSM32mFuF9LjNl4_aqmdrYBstRfiPT8Qe3IjF-JRPNkqA?e=R2jfNo)

* If you wish to classify your own personal dataset of comments, use the pretrained comment classifier model (model_comments_classifier.bin) using the [link](https://iiitaphyd-my.sharepoint.com/:f:/g/personal/aniruddha_d_research_iiit_ac_in/EmSM32mFuF9LjNl4_aqmdrYBstRfiPT8Qe3IjF-JRPNkqA?e=R2jfNo)

### Prerequisites

* The Code requires you to have Python3.5 (or any other future Python3 versions) and Python2.7 in your system.

* The following libraries also include dependancies required to create your own dataset and later the image and comment features on your own custom dataset. You may choose to skip using some of these if you just want to run just the classifier.

* Install the required Python3.5 libraries by running ```pip3 install -r requirements3.5.txt```

* Install the required Python2.7 libraries by running ```pip install -r requirements2.7.txt```

### Running the Sexist Comment Classifier

* Running the classifier for a given image yields top 3 Sexist comment types an Image may be prone to.
* Follow the below steps to run the classifier.

```
source <python2_project_env>/bin/activate
python main_part1.py <image_path>
deactivate
source <python3_project_env>/bin/activate
python3 main_part2.py <image_path>
```

### Creating Image Feature Dataset on your own list of custom users

* Create a list of your custom users and add their Instagram usernames line by line to 'Data/usernames.txt'. Note - You will have to activate your respective Python3.5 and Python2.7 environments while running the following.

* Run ```python3 retrieve_num_posts.py```

* Manually clean through the 'Data/num_posts.txt' file in case a wrong number of posts value is added to the file. Each line corresponds to each user in the 'Data/usernames.txt' file.

* Run ```python3 retrieve_insta_posts_list.py```

* Run ```python3 retrieve_photos.py``` and ```python3 retrieve_comments.py```. These will be dependant on your internet connection. You can choose to run these parallely in separate terminal instances as well.

* Run ```python3 link_images_comments.py``` to create the new metadata content.

* Run ```python3 create_demographic_features.py```

* Run ```python add_bmi_img_feature.py```

* Run ```python3 add_clothing_img_features.py```

* If you manually wish to annotate comment classes, run ```python3 convert_to_excel.py```. Use the corresponding excel files to carry out your own annotation. Note the annotation schema must be same as that of the one used in [Multi-label Categorization of Accounts of Sexism](https://www.aclweb.org/anthology/D19-1174/)

* Run ```shell Source/train_comments.sh``` to train your comment classifier model.

* Alternatively, Comment classes for each of the comment for a post can be predicted using the pretrained model. To do this run ```python3 classify_all_comments.py```

* You are now ready to create your final Image Features and Sexist Comment Weight Vector for future correlation and classification tasks. To do so run ```python3 save_correlation_data.py```.

* To train the regression models run the following ```jupyter notebook```. Select 'Source/IG-Sexism-Classifier.ipynb' and run all the cells. Now you can see the distribution statistics and the correlation matrices between each Image feature type and Sexist comment types for your own dataset. This code also trains the regression models needed for classification of new images.

* You can now follow the steps in 'Running the Sexist Comment Classifier' to classify images based on a model trained on your own custom dataset.

### Authors

* **Aniruddha Deshpande** [Github Profile](https://github.com/aniruddhapdeshpande99)
* **Aditya Agarwal** [Github Profile](https://github.com/aditya3498)

See also the list of [contributors](https://github.com/aniruddhapdeshpande99/WikiData-To-WikiPages/graphs/contributors) who participated in this project.

### Acknowledgments

* We would like to thank Prof. Nimmi Rangaswamy for guiding us for this project.
