import numpy as np
import pandas as pd
import networkx as nx
import os
import matplotlib.pyplot as plt
import itertools
import igraph as ig
import cairocffi as cairo


def get_data(year):
    pass


def build_network(data):
    """
    Given a suitable dataframe, constructs a network with the following properties:

    edges:
        - size: how often do two words appear in the same song?
    nodes:
        - size: in how many songs does the word appear?
        - color: degree of the node
    """
    pass


if __name__ == "__main__":
    year = 2022

    data = get_data(year)

    G = build_network(data)
