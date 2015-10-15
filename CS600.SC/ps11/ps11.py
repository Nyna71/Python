# 6.00 Problem Set 11
#
# ps11.py
#
# Graph optimization
# Finding shortest paths through MIT buildings
#

import string
from graph import Digraph, Node, Path

#
# Problem 2: Building up the Campus Map
#
# Each buidling will be represented as a node in a directed graph
# Each path between two buildings will be represente as an edge.
# Graph.py contains a Path class, which is a subtypeof edge, wearing
# two additional attributes for registering the total and outdoor distance
# of the path
#

def load_map(mapFilename):
    """ 
    Parses the map file and constructs a directed graph

    Parameters: 
        mapFilename : name of the map file

    Assumes:
        Each entry in the map file consists of the following four positive 
        integers, separated by a blank space:
            From To TotalDistance DistanceOutdoors
        e.g.
            32 76 54 23
        This entry would become an edge from 32 to 76.

    Returns:
        a directed graph representing the map
    """
    print "Loading map from file..."
    
    dataFile = open(mapFilename, 'r')
    g = Digraph()
    
    for line in dataFile:
        if len(line) == 0 or line[0] == '#':
            continue

        dataLine = string.split(line)
        
        fromBuidling = g.getNode(dataLine[0])
        toBuilding = g.getNode(dataLine[1])
        totalDistance = int(dataLine[2])
        outdoorDistance = int(dataLine[3])
        
        if fromBuidling is None:
            fromBuidling = Node(dataLine[0])
            g.addNode(fromBuidling)
        if toBuilding is None:
            toBuilding = Node(dataLine[1])
            g.addNode(toBuilding)        
        
        p = Path(fromBuidling, toBuilding, totalDistance, outdoorDistance)
        
        g.addEdge(p)
        
    return g
    
#
# Problem 3: Finding the Shortest Path using Brute Force Search
#
# State the optimization problem as a function to minimize
# and the constraints
#
def bruteForceSearch(graph, startNode, endNode, maxTotalDist, maxDistOutdoors, visited = []):    
    """
    Finds the shortest path from start to end using brute-force approach.
    The total distance travelled on the path must not exceed maxTotalDist, and
    the distance spent outdoor on this path must not exceed maxDisOutdoors.

    Parameters: 
        digraph: instance of class Digraph or its subclass
        start, end: start & end building numbers (strings)
        maxTotalDist : maximum total distance on a path (integer)
        maxDistOutdoors: maximum distance spent outdoors on a path (integer)

    Assumes:
        start and end are numbers for existing buildings in graph

    Returns:
        The shortest-path from start to end, represented by 
        a list of building numbers (in strings), [n_1, n_2, ..., n_k], 
        where there exists an edge from n_i to n_(i+1) in digraph, 
        for all 1 <= i < k.

        If there exists no path that satisfies maxTotalDist and
        maxDistOutdoors constraints, then raises a ValueError.
    """ 
    global numCalls
    numCalls += 1
    
    #Check if the distance constraints are respected
    if maxTotalDist < 0 or maxDistOutdoors < 0:
        return None
    
    #Did we reach the end node
    if startNode == endNode:
        return []
    
    bestPath = None
    
    for edge in graph.childrenOf(startNode):
        #If we already visited the desination node, try with next node
        if edge.getDestination() in visited:
            continue

        visited = visited + [edge.getSource()]
        path = bruteForceSearch(graph, edge.getDestination(), endNode, \
            maxTotalDist - edge.getTotalDistance(), maxDistOutdoors - edge.getOutdoorDistance(), visited)
                
        if path != None: #Did we reach the end node ?
            if bestPath == None or len(path) < len(bestPath):
                bestPath = [edge] + path
    
    if bestPath != None:
        return bestPath
    else:
        return None

#
# Problem 4: Finding the Shorest Path using Optimized Search Method
#
def directedDFS(digraph, start, end, maxTotalDist, maxDistOutdoors):
    """
    Finds the shortest path from start to end using directed depth-first.
    search approach. The total distance travelled on the path must not
    exceed maxTotalDist, and the distance spent outdoor on this path must
	not exceed maxDisOutdoors.

    Parameters: 
        digraph: instance of class Digraph or its subclass
        start, end: start & end building numbers (strings)
        maxTotalDist : maximum total distance on a path (integer)
        maxDistOutdoors: maximum distance spent outdoors on a path (integer)

    Assumes:
        start and end are numbers for existing buildings in graph

    Returns:
        The shortest-path from start to end, represented by 
        a list of building numbers (in strings), [n_1, n_2, ..., n_k], 
        where there exists an edge from n_i to n_(i+1) in digraph, 
        for all 1 <= i < k.

        If there exists no path that satisfies maxTotalDist and
        maxDistOutdoors constraints, then raises a ValueError.
    """
    #TODO
    pass

def toString(paths):
    """ Returns a string with all the paths inside the given list
        Parameters:
            path: a list of path
    """
    if paths is None:
        return "No possible path respecting the constraints"
    else:
        stringPath = "["
        for p in paths:
            stringPath += str(p) + ", "
            
    stringPath = stringPath[:-2] + "]"
    
    return stringPath

# Uncomment below when ready to test
if __name__ == '__main__':
    # Test cases
    digraph = load_map("mit_map.txt")

    LARGE_DIST = 1000000

#==============================================================================
#    # Test case 1
#    numCalls = 0
#    start = digraph.getNode("32")
#    end = digraph.getNode("56")
#    print "---------------"
#    print "Test case 1:"
#    print "Find the shortest-path from Building 32 to 56"
#    expectedPath1 = ['32', '56']
#
#    brutePath1 = bruteForceSearch(digraph, start, end, LARGE_DIST, LARGE_DIST)
#
#    print "Expected: ", expectedPath1
#    print "Found:", toString(brutePath1)
#    print "NumCalls:", numCalls

#==============================================================================
    # Test case 2
    numCalls = 0
    start = digraph.getNode("32")
    end = digraph.getNode("56")
    print "---------------"
    print "Test case 2:"
    print "Find the shortest-path from Building 32 to 56 without going outdoors"
    expectedPath2 = ['32', '36', '26', '16', '56']
    brutePath2 = bruteForceSearch(digraph, start, end, LARGE_DIST, 0)

    print "Expected: ", expectedPath2
    print "Found:", toString(brutePath2) 
    print "NumCalls:", numCalls

#==============================================================================
     # Test case 3
    numCalls = 0
    start = digraph.getNode("2")
    end = digraph.getNode("9")
    print "---------------"
    print "Test case 3:"
    print "Find the shortest-path from Building 2 to 9"
    expectedPath3 = ['2', '3', '7', '9']
    brutePath3 = bruteForceSearch(digraph, start, end, LARGE_DIST, LARGE_DIST)
    print "Expected: ", expectedPath3
    print "Brute-force: ", toString(brutePath3)
    
#==============================================================================

    # Test case 4
    numCalls = 0
    start = digraph.getNode("2")
    end = digraph.getNode("9")
    print "---------------"
    print "Test case 4:"
    print "Find the shortest-path from Building 2 to 9 without going outdoors"
    expectedPath4 = ['2', '4', '10', '13', '9']
    brutePath4 = bruteForceSearch(digraph, start, end, LARGE_DIST, 0)
    print "Expected: ", expectedPath4
    print "Brute-force: ", toString(brutePath4)


#==============================================================================
    # Test case 5
    numCalls = 0
    start = digraph.getNode("1")
    end = digraph.getNode("32")
    print "---------------"
    print "Test case 5:"
    print "Find the shortest-path from Building 1 to 32"
    expectedPath5 = ['1', '4', '12', '32']
    brutePath5 = bruteForceSearch(digraph, start, end, LARGE_DIST, LARGE_DIST)
    print "Expected: ", expectedPath5
    print "Brute-force: ", toString(brutePath5)

##
##    # Test case 6
    numCalls = 0
    start = digraph.getNode("1")
    end = digraph.getNode("32")
    print "---------------"
    print "Test case 6:"
    print "Find the shortest-path from Building 1 to 32 without going outdoors"
    expectedPath6 = ['1', '3', '10', '4', '12', '24', '34', '36', '32']
    brutePath6 = bruteForceSearch(digraph, start, end, LARGE_DIST, 0)
    print "Expected: ", expectedPath6
    print "Brute-force: ", toString(brutePath6)



