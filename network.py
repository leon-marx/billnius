import numpy as np
import pandas as pd
import networkx as nx
import os
import matplotlib.pyplot as plt


def get_data():
    song_dict = {}
    word_dict = {0: "I"}
    marker_dict = {}

    # df = pd.DataFrame(columns=["song_name", "artist", "filename", "lyrics"])
    data_dict = {}

    for i, song in enumerate(os.listdir("./songs")):
        song_name = song.split(" ")[:song.split(" ").index("by")]
        song_name = " ".join(song_name)
        artist = song.split(" ")[song.split(" ").index("by")+1:]
        artist = " ".join(artist)[:-4]
        with open(f"./songs/{song}", "r") as f:
            lyrics = np.unique(f.read().replace("\n", " ").split())
        data_dict[i] = [song_name, artist, song, lyrics]
    df = pd.DataFrame.from_dict(data_dict, columns=["song_name", "artist", "filename", "lyrics"], orient="index")

    # for i, song in enumerate(os.listdir("./songs")):
    #     song_dict[i] = song
    #     with open(f"./songs/{song}", "r") as f:
    #         words = np.unique(f.read().replace("\n", " ").split())
    #         for w in words:
    #             if w not in list(word_dict.values()):
    #                 word_dict[list(word_dict.keys())[-1]+1] = w
    #             marker_dict[f"{i},{list(word_dict.keys())[list(word_dict.values()).index(w)]}"] = 1

    # data = np.zeros((len(song_dict), len(word_dict)), dtype=np.uint8)

    # for k in list(marker_dict.keys()):
    #     song_id, word_id = k.split(",")
    #     song_id = int(song_id)
    #     word_id = int(word_id)
    #     data[song_id, word_id] = 1
    # return data, (song_dict, word_dict, marker_dict)
    return df



# building network
# Assume a dataframe with columns:
#   index, song_name, artist, filename, lyrics (tokenized)
song_df = get_data()
song_df.to_pickle("song_data.pkl")
print(song_df.head())

