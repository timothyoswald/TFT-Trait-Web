import networkx as nx
import itertools
import json

def loadData():
    with open ("units_set16.json", "r") as f:
        units = json.load(f)
    with open ("traits_set16.json", "r") as g:
        traits = json.load(g)
    return units, traits

def makeGraph():
    G = nx.Graph()

