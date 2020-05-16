import pandas as pd
import fasttext
from text_preprocessor import *
import json
import random

model = fasttext.train_supervised(input='comments.train', autotuneValidationFile='comments.valid', autotuneDuration=600)
model.save_model("../Models/model_comments_classifier.bin")
model.test("../Data/TrainingComments/comments.valid")