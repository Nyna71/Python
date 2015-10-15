# 6.00 Problem Set 11
#
# graph.py
#
# A set of data structures to represent graphs
#

class Node(object):
   def __init__(self, name):
       self.name = str(name)
   def getName(self):
       return self.name
   def __str__(self):
       return self.name
   def __repr__(self):
      return self.name
   def __eq__(self, other):
      return self.name == other.name
   def __ne__(self, other):
      return not self.__eq__(other)

class Edge(object):
   def __init__(self, src, dest):
       self.src = src
       self.dest = dest
   def getSource(self):
       return self.src
   def getDestination(self):
       return self.dest
   def __str__(self):
       return str(self.src) + '->' + str(self.dest)
       
class Path(Edge):
    def __init__(self, src, dest, totalDistance, outdoorDistance):
        self.src = src
        self.dest = dest
        self.totalDistance = totalDistance
        self.outdoorDistance = outdoorDistance
        
    def getTotalDistance(self):
        return self.totalDistance
        
    def getOutdoorDistance(self):
        return self.outdoorDistance
        
    def __str__(self):
        return str(self.src) + '->' + str(self.dest) + " (" + str(self.totalDistance) + \
                ", " + str(self.outdoorDistance) + ")"

class Digraph(object):
   """
   A directed graph
   """
   def __init__(self):
       self.nodes = set([])
       self.edges = {}
   def addNode(self, node):
       if node in self.nodes:
           raise ValueError('Duplicate node')
       else:
           self.nodes.add(node)
           self.edges[node] = []

   def getNode(self, name):
       for node in self.nodes:
           if node.getName() == name:
               return node
       return None
       
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

