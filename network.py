import numpy as np
import pandas as pd
import networkx as nx
import os
import matplotlib.pyplot as plt
import itertools
import igraph as ig
import cairocffi as cairo


def get_data(year):
    df = pd.read_csv(f"./songs_cleaned/songs_{year}.csv", sep=";")
    return df


def build_network(data, min_count=50, min_connection=10, save_neo4j_config=False):
    """
    Given a suitable dataframe, constructs a network with the following properties:

    edges:
        - size: how often do two words appear in the same song?
    nodes:
        - size: in how many songs does the word appear?
        - color: degree of the node
    """
    G = nx.Graph()

    # read all unique words
    print("Reading words...")
    words = []
    for lyrics in data["lyrics"]:
        for word in lyrics.split(" "):
            words.append(word)

    # get unique words with counts, sort by most popular and remove words with counts < min_count
    print("Word preprocessing...")
    words, w_counts = np.unique(words, return_counts=True)
    words = [x for _, x in sorted(zip(w_counts, words))][::-1]
    w_counts = sorted(w_counts)[::-1]
    w_cutoff = w_counts.index(min_count-1)
    words = words[:w_cutoff]
    w_counts = w_counts[:w_cutoff]

    # read song-word links
    word_to_index = {word: i for i, word in enumerate(words)}
    index_to_word = {i: word for i, word in enumerate(words)}
    song_word_connector = np.zeros((len(data), len(words)))
    for i, lyrics in enumerate(data["lyrics"]):
        for word in lyrics.split(" "):
            try:
                song_word_connector[i, word_to_index[word]] = 1
            except KeyError:
                pass

    # read all edges between remaining words
    print("Reading edges...")
    edge_dict = {}
    for row in song_word_connector:
        ind1 = [i for i, x in enumerate(row) if x == 1]
        pairs = list(itertools.combinations(ind1, 2))
        for i, j in pairs:
            edge_dict.setdefault(f"{i},{j}", 0)
            edge_dict[f"{i},{j}"] += 1

    # adding unique edges with thei respective count to the edges list if the count is bigger/equal min_connection
    print("Edge preprocessing...")
    edges = []
    for k in list(edge_dict.keys()):
        i, j = k.split(",")
        i = int(i)
        j = int(j)
        if edge_dict[k] >= min_connection:
            edges.append((index_to_word[i], index_to_word[j], {"weight": edge_dict[k]}))

    # add nodes and edges to graph
    print("Adding nodes to the network...")
    G.add_nodes_from([
        (word, {"color": "red", "size": w_counts[i]}) for i, word in enumerate(words)
    ])
    print("Adding edges to the network...")
    G.add_edges_from(edges)

    if save_neo4j_config:
        with open("neo4j_config.csv", "w") as f:
            f.write("start,stop,weight\n")
            for edge in edges:
                f.write(f"{edge[0]},{edge[1]},{edge[2]['weight']}\n")

    return G


def plot(graph):
    pass


if __name__ == "__main__":
    year = 2022

    data = get_data(year)

    G = build_network(data, save_neo4j_config=True)

    print(G.number_of_nodes())
    print(G.number_of_edges())
