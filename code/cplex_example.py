import numpy as np
import networkx as nx
from docplex.mp.constants import ComparisonType
from docplex.mp.model import Model


def solve_ising(B, bias):
    """
    Ising model: \sum_{i,j} B_ij s_i s_j + \sum_i C_i c_i 
    """
    mdl = Model()
    n = B.shape[0]
    x = {i: mdl.binary_var(name='x_{0}'.format(i)) for i in range(n)}
    
    # objective function
    # couplers_func =  mdl.sum(2 * B[i,j] * (2 * x[i] - 1) * (2 * x[j] - 1) for i in range(n - 1) for j in range(i, n)) s_i\in {-1,+1}

    couplers_func =  mdl.sum(2 * B[i,j] * x[i] * x[j] for i in range(n - 1) for j in range(i, n)) # s_i \in{0,1}
    bias_func = mdl.sum(float(bias[i]) * x[i] for i in range(n))
    ising_func = couplers_func + bias_func

    mdl.minimize(ising_func)
    solution = mdl.solve()
    cplex_solution = solution.get_all_values()

    # print('CPLEX solution: ', [int(1-2*i) for i in cplex_solution])  s_i \in {-1,+1}
    print('CPLEX solution: ', cplex_solution)
    return cplex_solution


if __name__ == '__main__':
    n=4 # Number of nodes in graph
    G=nx.Graph()
    G.add_nodes_from(np.arange(0,n,1))
    elist=[(0,1,1.0),(0,2,1.0),(0,3,1.0),(1,2,1.0),(2,3,1.0)]
    # tuple is (i,j,weight) where (i,j) is the edge
    G.add_weighted_edges_from(elist)
        L = - nx.laplacian_matrix(G).A 
        solve_ising(L, [0] * G.number_of_nodes()) 
