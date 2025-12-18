import networkx as nx
import itertools
import json

def loadData():
    with open ("units_set16.json", "r") as f:
        units = json.load(f)
    with open ("traits_nohero_set16.json", "r") as h:
        traits = json.load(h)
    # with open ("traits_set16.json", "r") as g:
    #     traits = json.load(g)
    return units, traits

# tibbers is counted as a unit but can only be played
# with annie so need to manually enforce later
def makeGraph(units, traits):
    G = nx.Graph()
    # add nodes to graph labeled by unit name
    for unit in units:
        G.add_node(unit["name"], **unit)
    # go through all possible pairs and add edge in they have same trait
    for unitA, unitB in itertools.combinations(list(G.nodes), 2):
        traitsA = set(G.nodes[unitA]["traits"])
        traitsB = set(G.nodes[unitB]["traits"])
        sharedTraits = traitsA & traitsB
        if sharedTraits:
            # add more weight data later?
            G.add_edge(unitA, unitB, weight = len(sharedTraits), shared = list(sharedTraits))
    return G

# given a carry find a level 9 comp around it
def findCompositionWithCarry(G, carry, traits):
    currentBoard = {carry}

    while len(currentBoard) < 9:
        potentialUnits = set()
        pass

units, traits = loadData()
makeGraph(units, traits)