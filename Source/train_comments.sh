#!/bin/bash

python3 create_comment_classifier_train_data.py
cd ../Data/TrainingComments
cat train_comments.txt | shuf > train_comments_shuffled.txt
head -n 12460 train_comments_shuffled.txt > comments.train
tail -n 1500 train_comments_shuffled.txt > comments.valid
cd ../../Source
python3 train_comment_classifier.py
