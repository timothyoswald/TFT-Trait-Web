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

# for now, score should be based on unit cost
# and traits contributed to the board
# there is an issue where score changes
# as new units are added
def computeScore(G, allTraits, boardTraits, newUnit):
    score = G.nodes[newUnit]["cost"]
    for trait in G.nodes[newUnit]["traits"]:
        if trait in boardTraits:
            boardTraits[trait] += 1
            num = boardTraits[trait]
            if str(num) in allTraits[trait]:
                score += num
        else:
            boardTraits[trait] = 1
    return score

# given a carry find a level 9 comp around it
def findCompositionWithCarry(G, carry, traits):
    currentBoard = {carry}
    totalScore = G.nodes[carry]["cost"]
    traitsSoFar = {trait: 1 for trait in G.nodes[carry]["traits"]}

    while len(currentBoard) < 9:
        bestOption = None
        bestScore = 0
        # look at all current neighbors and choose best one
        # should definitely make this more efficient to not 
        # relook through all neighbors
        for unit in currentBoard:
            for nbor in G.neighbors(unit):
                score = computeScore(G, traits, traitsSoFar, nbor)
                if score > bestScore:
                    bestOption = nbor
                    bestScore = score
        currentBoard.add(bestOption)
        totalScore += bestScore

    return currentBoard, totalScore


units, traits = loadData()
G = makeGraph(units, traits)
print(findCompositionWithCarry(G, "Kindred", traits))
