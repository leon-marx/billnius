import numpy as np
import pandas as pd

import os
import re

import nltk
from nltk.corpus import gutenberg, wordnet, stopwords
from nltk.tokenize import sent_tokenize , word_tokenize
from nltk.stem import WordNetLemmatizer
from string import punctuation

nltk.download('omw-1.4')
nltk.download('stopwords')
nltk.download('punkt')

# function to lemmatize

lemmatizer = WordNetLemmatizer()

# function to convert nltk tag to wordnet tag
def nltk_to_wordnet(nltk_tag):
    if nltk_tag.startswith('J'):
        return wordnet.ADJ
    elif nltk_tag.startswith('V'):
        return wordnet.VERB
    elif nltk_tag.startswith('N'):
        return wordnet.NOUN
    elif nltk_tag.startswith('R'):
        return wordnet.ADV
    else:
        return None

# list with stopwords and punctuation to remove
stoplist = set(stopwords.words('english') + list(punctuation))

def clean_lyrics(lyrics):
    # change everything to lower case
    lyrics = lyrics.lower()
    # remove numbers
    lyrics_nonum = re.sub(r'\d+', '', lyrics)

    #tokenize the lyrics and find the POS tag for each token
    nltk_tagged = nltk.pos_tag(nltk.word_tokenize(lyrics_nonum))

    #tuple of (token, wordnet_tag)
    wordnet_tagged = map(lambda x: (x[0], nltk_to_wordnet(x[1])), nltk_tagged)
    lemmatized_lyrics = []
    for word, tag in wordnet_tagged:
        if tag is None:
            #if there is no available tag, append the token as is
            lemmatized_lyrics.append(word)
        else:
            #else use the tag to lemmatize the token
            lemmatized_lyrics.append(lemmatizer.lemmatize(word, tag))

    unique_tokens = unique_tokens = list(set(lemmatized_lyrics))

    # remove stopwords
    unique_nostop = [word for word in unique_tokens if word not in stoplist]
    return unique_nostop

# decade = int(input("Which year to start?"))

for year in range(1955, 2024, 1):
    path_songs = f"./songs/songs_{year}"
    songlist = [song for song in os.listdir(path_songs) if os.path.isfile(os.path.join(path_songs, song))]
    # print(songlist)
    print(f"Lemmatizing year {year}...")
    df_songs = pd.DataFrame(columns = ['title','artist'])
    song_lyrics = []

    for song in songlist:
        # getting title and artist from the file name
        title_artist = pd.DataFrame(song[:-4].split(' by ',1))
        title_artist = title_artist.transpose()
        title_artist.columns = ['title','artist']

        # clean lyrics
        source = open(os.path.join(path_songs, song), 'r', encoding='cp1252')
        lyrics = source.read()
        clean_tokens = clean_lyrics(lyrics)
        lyrics_string = ' '.join(clean_tokens)
        song_lyrics.append(lyrics_string)

        # add to the dataframe
        df_songs = pd.concat([df_songs, title_artist])

    df_songs['lyrics'] = song_lyrics
    df_songs['filename'] = songlist

    # print(df_songs.head())
    df_songs.to_csv(f"./songs_cleaned_version_2/songs_{year}.csv", sep=";", index=False)
    print("")