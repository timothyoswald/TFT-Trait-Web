import networkx as nx
import itertools
import json
import random
import helpers

# tibbers is counted as a unit but can only be played
# with annie so need to manually enforce later
# baron counts as 2 void need to update
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

# fix later
def computeScore(G, board):
    score = 0
    for unit in board:
        score += G.nodes[unit]["cost"]
    return score

# perform BFS but only note top 20 teams at any time
def beamSearch(G, traits, beamWidth = 20, teamSize = 9):
    # initially comps randomly
    startUnits = random.sample(list(G.nodes), k = 20)
    currentBeams = []
    for unit in startUnits:
        score = computeScore(G, [unit])
        currentBeams.append((score, [unit]))

    # consider all possible new teams
    for _ in range(teamSize - 1):
        possibleNewComps = []

        # add all neighbors of current top 20
        for score, comp in currentBeams:
            newCandidates = set()
            for x in comp:
                nbors = G.neighbors(x)
                newCandidates.update(nbors)
        
            # test all possible new teams
            for unit in newCandidates:
                if unit not in comp:
                    trialComp = sorted(comp + [unit]) # sort so we can compare later
                    trialScore = computeScore(G, trialComp)
                    possibleNewComps.append((trialScore, trialComp))
            
        # keep top 20
        possibleNewComps.sort(key = lambda x: x[0], reverse = True)
        topNewComps = []
        seenComps = set()
        # need to make sure we don't have same comp twice
        # but in different order
        for newScore, newComp in possibleNewComps:
            ID = tuple(newComp) # tuple so it can be hashed
            if ID not in seenComps:
                seenComps.add(ID)
                topNewComps.append((newScore, newComp))
            if len(topNewComps) >= beamWidth:
                break
        
        currentBeams = topNewComps
    
    return currentBeams[0]

    


units, traits = helpers.loadData()
G = makeGraph(units, traits)
score, comp = beamSearch(G, traits)
helpers.pretty_print_comp(comp, G, traits)
