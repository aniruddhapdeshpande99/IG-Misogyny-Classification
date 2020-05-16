import pandas as pd
import nltk
import string
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
from emo_unicode import EMOTICONS
import emoji
import re

#Uncomment if you don't have it downloaded
# nltk.download('wordnet')
# nltk.download('stopwords')
# nltk.download('averaged_perceptron_tagger')

#Removes punctuation from a given string
def remove_punctuation(text):
    PUNCT_TO_REMOVE = string.punctuation
    PUNCT_TO_REMOVE = PUNCT_TO_REMOVE.replace("@","") #To keep hashtags so that it can be removed by remove_url_usertags()
    PUNCT_TO_REMOVE = PUNCT_TO_REMOVE.replace("_","") #To keep emojis
    PUNCT_TO_REMOVE = PUNCT_TO_REMOVE.replace(":","") #To keep emojis
    return text.translate(str.maketrans('', '', PUNCT_TO_REMOVE))

#Removes stopwords from a string
def remove_stopwords(text):
    STOPWORDS = set(stopwords.words('english'))
    return " ".join([word for word in str(text).split() if word not in STOPWORDS])

#Stems a given string
def stem_words(text):
    stemmer = PorterStemmer()
    return " ".join([stemmer.stem(word) for word in text.split()])

#Lemmatizes a given string
def lemmatize_words(text):
    lemmatizer = WordNetLemmatizer()
    wordnet_map = {"N":wordnet.NOUN, "V":wordnet.VERB, "J":wordnet.ADJ, "R":wordnet.ADV}
    pos_tagged_text = nltk.pos_tag(text.split())
    return " ".join([lemmatizer.lemmatize(word, wordnet_map.get(pos[0], wordnet.NOUN)) for word, pos in pos_tagged_text])

#Converts Emoticons to words from a given string
def convert_emoticons(text):
    for emot in EMOTICONS:
        text = re.sub(u'('+emot+')', "_".join(EMOTICONS[emot].replace(",","").split()), text)
    return text

#Converts Emojis to words from a given string
def convert_emojis(text):
    return emoji.demojize(text)

#Removes URLs and Usertags from a given string
def remove_url_usertags(text):
    return re.sub(r"(?:\@|https?\://)\S+", "", text)
     
#Loads Abbreviations 
def load_abbreviations():
    abbr_index = []
    with open("../Data/abbreviations.txt") as f:
        abbr_index = f.readlines()
    abbr_index = [x.strip() for x in abbr_index] 

    chat_words_map_dict = {}
    chat_words_list = []
    for line in abbr_index:
        if line != "":
            cw = line.split("=")[0]
            cw_expanded = line.split("=")[1]
            chat_words_list.append(cw)
            chat_words_map_dict[cw] = cw_expanded
    chat_words_list = set(chat_words_list)
    return chat_words_list, chat_words_map_dict

#Replaces Abbreviations with their full forms
def remove_abbreviations(text, chat_words_list, chat_words_map_dict):
    new_text = []
    for w in text.split():
        if w.upper() in chat_words_list:
            new_text.append(chat_words_map_dict[w.upper()])
        else:
            new_text.append(w)
    return " ".join(new_text)

#Removes the comments from the dataframe which are empty after preprocessing
def remove_empty_string_columns(df):
    df["post"].replace({"": None}, inplace=True) 
    bool_series = pd.notnull(df["post"]) 
    return df[bool_series][['post', 'labels']]
    
#Preprocesses the entire dataset (has to be in the form of Dataframe [['post', 'class']])
def preprocess(df):
    #Converting abbreviations
    abbreviations, abbr_dict = load_abbreviations()
    df ['post'] = df['post'].apply(lambda text: remove_abbreviations(text, abbreviations, abbr_dict))
    #Converting Emoticons and Emojis to words
    df['post'] = df['post'].apply(lambda text: convert_emoticons(text))
    df['post'] = df['post'].apply(lambda text: convert_emojis(text))
    #Lowercase text
    df['post'] = df['post'].str.lower()
    #Remove punctuation
    df['post'] = df['post'].apply(lambda text: remove_punctuation(text))
    #Remove stop words
    df["post"] = df["post"].apply(lambda text: remove_stopwords(text))
    #Stemming data [Uncomment if you want to Stem and Comment Lemmatize line]
    # df["post"] = df["post"].apply(lambda text: stem_words(text))
    #Lemmatize data [Either lemmatize or Stem, dont do both]
    df["post"] = df["post"].apply(lambda text: lemmatize_words(text))
    #Remove URLs, Username tags, Hashtags
    df['post'] = df['post'].apply(lambda text: remove_url_usertags(text))
    return df 