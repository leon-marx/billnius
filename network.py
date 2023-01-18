import numpy as np
import pandas as pd
import networkx as nx
import os
import matplotlib.pyplot as plt
import itertools
import igraph as ig
import cairocffi as cairo


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


# Data Preparation

# Assume a dataframe with columns:
#   index, song_name, artist, filename, lyrics (tokenized)
# song_df = get_data()
# song_df.to_pickle("song_data.pkl")
song_df = pd.read_pickle("song_data.pkl")
print(song_df.head())

# building data
forbidden = [",", ";", ".", ":", "(", ")", "[", "]", "#", "'"]

words = {}
for lyrics in song_df["lyrics"]:
    for word in lyrics:
        words.setdefault(word, 0)
        words[word] += 1
words = dict(sorted(words.items(), key=lambda item: item[1])[::-1])
words = list(words.keys())

song_id = {song: i for i, song in enumerate(song_df["filename"])}
word_id = {word: i for i, word in enumerate(words)}
data = np.zeros((len(song_df["filename"]), len(words)), dtype=np.uint8)

for i, song in enumerate(song_df["filename"]):
    for word in song_df["lyrics"][i]:
        data[song_id[song], word_id[word]] = 1

# from here, data is expected to be a binary matrix of shape(#songs, #total words)

edge_dict = {}
for row in data:
    ind1 = [i for i, x in enumerate(row) if x == 1]
    pairs = list(itertools.combinations(ind1, 2))
    for i, j in pairs:
        edge_dict.setdefault(f"{i},{j}", 0)
        edge_dict[f"{i},{j}"] += 1

edges = []
for k in list(edge_dict.keys()):
    i, j = k.split(",")
    i = int(i)
    j = int(j)
    if edge_dict[k] > 1:
        edges.append((i, j, edge_dict[k]))
G = nx.Graph()
G.add_weighted_edges_from(edges)

print(len(G.nodes()))
print(len(G.edges()))

g = ig.Graph.from_networkx(G)
ig.plot(g, "network.pdf")
