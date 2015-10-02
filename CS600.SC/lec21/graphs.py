# -*- coding: utf-8 -*-
"""
Created on Mon Sep 21 16:16:56 2015

@author: Jonathan
"""
import random

class Node(object):
    def __init__(self, name):
        self.name = name
    def getName(self):
        return self.name
    def __str__(self):
        return self.name
    def __eq__(self, other):
        return self.getName() == other.getName()

class Edge(object):
    def __init__(self, src, dest, weight = 0):
        self.src = src
        self.dest = dest
        self.weight = weight
    def getSource(self):
        return self.src
    def getDestination(self):
        return self.dest
    def getWeight(self):
        return self.weight
    def __str__(self):
        return str(self.src) + '->' + str(self.dest)

class Digraph(object):
    def __init__(self):
        self.nodes = set()
        self.edges = {}
        
    def addNode(self, node):
        nodePresent = False
        for n in self.nodes:
            if n == node:
                nodePresent = True
        
        if not nodePresent:
            self.nodes.add(node)
            self.edges[node] = []
            
    def addEdge(self, edge):
        src = edge.getSource()
        dest = edge.getDestination()
        if not(src in self.nodes and dest in self.nodes):
            raise ValueError('Node not in graph')
        self.edges[src].append(edge)
        
    def childrenOf(self, node):
        return self.edges[node]
        
    def hasNode(self, node):
        return node in self.nodes
        
    def __str__(self):
        res = ''
        for node in self.nodes:
            for edge in self.edges[node]:
                res += str(edge) + '\n'
                #res = res + str(k) + '->' + str(d) + '\n'
        return res[:-1]

class Graph(Digraph):
    def addEdge(self, edge):
        Digraph.addEdge(self, edge)
        rev = Edge(edge.getDestination(), edge.getSource())
        Digraph.addEdge(self, rev)

def getNodes(path):
    """ Return a list of all nodes in the path
        Path: a list of edges   
    """
    if len(path) == 0:
        return []
    
    nodes = []
    nodes.append(path[0].getSource())
    for edge in path:
        nodes.append(edge.getDestination())
        
    return nodes

def shortestPath(graph, startNode, endNode, visited = []):   
    global numCalls
    numCalls += 1
    
    if startNode == endNode:
        return []
    
    bestPath = None
    
    for edge in graph.childrenOf(startNode):
        #If we already visited the desination node, try with next node
        if edge.getDestination() in visited:
            continue

        visited = visited + [edge.getSource()]
        path = shortestPath(graph, edge.getDestination(), endNode, visited)
                
        if path != None: #Did we reach the end node ?
            if bestPath == None or len(path) < len(bestPath):
                bestPath = [edge] + path
    
    if bestPath != None:
        return bestPath
    else:
        return None
    
def test1(kind):
    nodes = []
    for name in range(10):
        nodes.append(Node("Node" + str(name)))
    g = kind()
    for n in nodes:
        g.addNode(n)
    g.addEdge(Edge(nodes[0],nodes[1]))
    g.addEdge(Edge(nodes[1],nodes[2]))
    g.addEdge(Edge(nodes[2],nodes[3]))
    g.addEdge(Edge(nodes[3],nodes[4]))
    g.addEdge(Edge(nodes[3],nodes[5]))
    g.addEdge(Edge(nodes[0],nodes[2]))
    g.addEdge(Edge(nodes[1],nodes[1]))
    g.addEdge(Edge(nodes[1],nodes[0]))
    g.addEdge(Edge(nodes[4],nodes[0]))
    print 'The graph:'
    print g
    
def test2(kind, toPrint = False):
    nodes = []
    for name in range(10):
        nodes.append(Node("Node" + str(name)))
    g = kind()
    for n in nodes:
        g.addNode(n)

    g.addEdge(Edge(nodes[0],nodes[1]))
    g.addEdge(Edge(nodes[1],nodes[2]))
    g.addEdge(Edge(nodes[2],nodes[3]))
    g.addEdge(Edge(nodes[3],nodes[4]))
    g.addEdge(Edge(nodes[3],nodes[5]))
    g.addEdge(Edge(nodes[0],nodes[2]))
    g.addEdge(Edge(nodes[1],nodes[1]))
    g.addEdge(Edge(nodes[1],nodes[0]))
    g.addEdge(Edge(nodes[4],nodes[0]))

    print 'The graph:'
    print g
    print 'The shortest path:'
    shortest = shortestPath(g, nodes[0], nodes[5])
    for edge in shortest:
        print edge
        
def bigTest1(kind, numNodes = 25, numEdges = 100):
    nodes = []
    for name in range(numNodes):
        nodes.append(Node("Node" + str(name)))
    g = kind()
    for n in nodes:
        g.addNode(n)
    for e in range(numEdges):
        src = nodes[random.choice(range(0, len(nodes)))]
        dest = nodes[random.choice(range(0, len(nodes)))]
        g.addEdge(Edge(src, dest))

    global numCalls   
    numCalls = 0
    
    print g
    
    print 'The shortest path:'
    shortest = shortestPath(g, nodes[0], nodes[5])
    for edge in shortest:
        print edge
        
    print numCalls