# -*- coding: utf-8 -*-
"""
Created on Fri May 21 18:20:47 2021

@author: ricca
"""

import matplotlib.pyplot as plt
import networkx as nx
import pylab
G = nx.Graph()

agents = ['A1','A2','A3','A4','A5','A6','A7','A8','A9','A10']

G.add_nodes_from(agents)

ba = nx.barabasi_albert_graph(10, 2, seed=42)


print ("G.edges = ", sorted(ba.edges()))
sorted_stuff = sorted(ba.degree, key=lambda x: x[1], reverse=True)

first_element_sorted_stuff = []

for i in sorted_stuff:
    first_element_sorted_stuff.append(i[0])
    
print(first_element_sorted_stuff)

node_view = ba.nodes

for i in range(len(first_element_sorted_stuff)):
    ba.nodes[first_element_sorted_stuff[i]]['Agent_ID'] = agents[i]
    
labels = nx.get_node_attributes(ba, 'Agent_ID')
nx.draw(ba,labels=labels,node_size=1000)
pylab.show()
