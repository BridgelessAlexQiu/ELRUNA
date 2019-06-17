import numpy as np
import networkx as nx
import random
import utility as uti
from collections import defaultdict
from docplex.mp.constants import ComparisonType
from docplex.mp.model import Model
import math


# the large constant
beta = 40
d_replace = 20

g1 = nx.read_edgelist("test1.edgelist", nodetype = int)
g2 = nx.read_edgelist("test2.edgelist", nodetype = int)

g1_node_list = list(g1.nodes()) 
g2_node_list = list(g2.nodes()) 

C = nx.to_numpy_matrix(g1, dtype = np.int8)
D = nx.to_numpy_matrix(g2, g1_node_list, dtype = np.int8)

for i in range(len(g2)):
    for j in range(len(g2)):
        if D[i, j] == 0:
            D[i, j] = d_replace

n = len(g1_node_list)
# the initial mapping (quite arbitrary )
mapping = {1 : 2, 0 : 4, 3 : 1, 4 : 3, 2 : 0}

V_1 = g1_node_list
V_2 = g2_node_list

partial_D = np.zeros((n, n), np.int8)
for i in range(n):
    for j in range(n):
        partial_D[i, j] = D[V_2[i], V_2[j]]

# M_1 = \beta \times I_{n_1 \times n_1} \otimes Oi(I_{n_2 \times n_2} ), here n_1 = n_2 = n
M_1 = beta * np.kron(
	np.identity(n, np.int8), 
	uti.Oi(np.identity(n, np.int8))
	)  

# M_2 = \beta \times Oi(I_{n_1 \times n_1}) \otimes I_{n_2 \times n_2}, here n_1 = n_2 = n
M_2 = beta * np.kron(
	uti.Oi(np.identity(n, np.int8)),
	np.identity(n, np.int8)
	)

# M_3 = -2\beta \times I_{n_1n_2 \times n_1n_2}
M_3 =  -2 * beta * np.identity(n**2)

# construct H
H = np.kron(C, partial_D) + M_1 + M_2 + M_3

# empty bias
J = [0] * n**2

result = uti.solve_ising(H, J)

for r in range(len(result)):
    if result[r] == 1.0:
        i = V_1[math.floor(r / n)]
        u = V_2[r % n]
        mapping[int(i)] = int(u)

for v, k in mapping.items():
    print("{} : {}".format(v, k))

print(result)