#include <iostream>
#include <fstream>
#include <map>
#include <list>
#include <algorithm> 
#include <vector>
#include <tuple>
#include <array>

using namespace std;

int main(int argc, char* argv[])
{
	char* g1_network_file_name; // name of the first network
	char* g2_network_file_name; // name of the second network
	int max_iter; // The diameter of the graph

	// If the number of additional argumnets does not equal to 2
	if(argc != 4)
	{
		cerr << "Please make sure you pass exactly two input files and one max_iter\n";
		return -1;
	}
	
	// Assign the network files and the number of iterations
	g1_network_file_name = argv[1];
	g2_network_file_name = argv[2];
	max_iter = atoi(argv[3]);

	// ########################################################################################
	// #                                   Construct G1 Begin                                 #
	// ########################################################################################
	ifstream g1_network_file(g1_network_file_name); //The file object

	if(g1_network_file.fail())// If we cannot locate the file
	{
		cerr<<"File: "<<g1_network_file_name<<" cannot be found\n";
		return -1;
	}

	// ------------------------------------------------------ 
	// -               Read in the graph                    -
	// ------------------------------------------------------
	map<int, list<int>> g1_neighbor_map; // Format: {node : [list of neighbors]} 

	int i, j; // Node i and j
	while(g1_network_file>>i>>j) // We assume that the nodes are separated by whitespaces
	{
		list<int> i_neighbors;
		// Insert operation checks if the node exists in the map, if so, the element is not inserted
		g1_neighbor_map.insert(map<int, list<int>>::value_type(i, i_neighbors));

		list<int> j_neighbors;
		// Insert operation checks if the node exists in the map, if so, the element is not inserted
		g1_neighbor_map.insert(map<int, list<int>>::value_type(j, j_neighbors));

		g1_neighbor_map[i].push_back(j);
		g1_neighbor_map[j].push_back(i);
	}

	// --------------------------------------------------------- 
	// -               Variable Declaration                    -
	// ---------------------------------------------------------
	int g1_size = g1_neighbor_map.size(); // Number of nodes in g1
	int g1_num_of_edges = 0; // Number of edges in g1

	int** g1_neighbor_sequence = new int*[g1_size]; // Format: [[neighbors of node0], [neighbors of node1] ...]
	int g1_degree_sequence[g1_size]; // Format: [degree_of_node0, degree_of_node1, ... ]

	// ----------------------------------------------------
	// -                  Assign neighbors                -
	// ----------------------------------------------------
	for(auto map_it = g1_neighbor_map.begin(); map_it != g1_neighbor_map.end(); ++map_it)
	{
		int i = map_it->first; // the node 
		list<int> neighbors = map_it->second; // the neighbors
		neighbors.unique(); // Remove duplicates (depends on the edgelist file format, there should be no duplicates by default)

		g1_degree_sequence[i] = neighbors.size();
		g1_neighbor_sequence[i] = new int[g1_degree_sequence[i]];
		g1_num_of_edges += g1_degree_sequence[i];

		int j = 0;
		for (auto list_it = neighbors.begin(); list_it != neighbors.end(); ++list_it)
		{
			g1_neighbor_sequence[i][j] = *list_it;	
			j++;
		}
	}

	g1_num_of_edges /= 2; // each edges is counted twice
	g1_network_file.close();

	// ########################################################################################
	// #                                   Construct G2 Begin                                 #
	// ########################################################################################
	ifstream g2_network_file(g2_network_file_name); //The file object

	if(g2_network_file.fail())// If we cannot locate the file
	{
		cerr<<"File: "<<g2_network_file_name<<" cannot be found\n";
		return -1;
	}

	// ------------------------------------------------------ 
	// -               Read in the graph                    -
	// ------------------------------------------------------
	map<int, list<int>> g2_neighbor_map; // Format: {node : [list of neighbors]} 

	int u, v; // Node i and j
	while(g2_network_file>>u>>v)
	{
		list<int> u_neighbors;
		// Insert operation checks if the node exists in the map, if so, the element is not inserted
		g2_neighbor_map.insert(map<int, list<int>>::value_type(u, u_neighbors));

		list<int> v_neighbors;
		// Insert operation checks if the node exists in the map, if so, the element is not inserted
		g2_neighbor_map.insert(map<int, list<int>>::value_type(v, v_neighbors));

		g2_neighbor_map[u].push_back(v);
		g2_neighbor_map[v].push_back(u);
	}

	// --------------------------------------------------------- 
	// -               Variable Declaration                    -
	// ---------------------------------------------------------
	int g2_size = g2_neighbor_map.size(); // Number of nodes in g2
	int g2_num_of_edges = 0; // Number of edges in g2

	int** g2_neighbor_sequence = new int*[g2_size]; // Format: [[neighbors of node0], [neighbors of node1] ...]
	int g2_degree_sequence[g2_size]; // Format: [degree_of_node0, degree_of_node1, ... ]

	// ----------------------------------------------------
	// -                  Assign neighbors                -
	// ----------------------------------------------------
	for(auto map_it = g2_neighbor_map.begin(); map_it != g2_neighbor_map.end(); ++map_it)
	{
		int u = map_it->first; // the node 
		list<int> neighbors = map_it->second; // the neighbors
		neighbors.unique(); // Remove duplicates (depends on the edgelist file format, there should be no duplicates by default)

		g2_degree_sequence[u] = neighbors.size();
		g2_neighbor_sequence[u] = new int[g2_degree_sequence[u]];
		g2_num_of_edges += g2_degree_sequence[u];

		int v = 0;
		for (auto list_it = neighbors.begin(); list_it != neighbors.end(); ++list_it)
		{
			g2_neighbor_sequence[u][v] = *list_it;	
			v++;
		}
	}

	g2_num_of_edges /= 2; // each edges is counted twice
	g2_network_file.close();

	// ##############################################
	// #        Output Network Information          #
	// ##############################################
	cout<<"G1:"<<endl;
	cout<<"Number of nodes: "<<g1_size<<endl;
	cout<<"Number of edges: "<<g1_num_of_edges<<endl;

	cout<<"------------------------------\n";
	
	cout<<"G2:"<<endl;
	cout<<"Number of nodes: "<<g2_size<<endl;
	cout<<"Number of edges: "<<g2_num_of_edges<<endl;
	
	// ########################################################
	// #             Construct the adjacency matrix           #
	// ########################################################
	
	// ------------------
	// -       C        -
	// ------------------
	int C[g1_size][g1_size] = {{0}}; // the adjacency matrix of g1
	for(int i = 0; i < g1_size; ++i)
	{
		for(int j_index = 0; j_index < g1_degree_sequence[i]; ++j_index)
		{
			int j = g1_neighbor_sequence[i][j_index];
			C[i][j] = 1;
		}
	}

	// ------------------
	// -       D        -
	// ------------------
	int D[g2_size][g2_size] = {{0}}; // the adjacency matrix of g2
	for(int u = 0; u < g2_size; ++u)
	{
		for(int v_index = 0; v_index < g2_degree_sequence[u]; ++v_index)
		{
			int v = g2_neighbor_sequence[u][v_index];
			D[u][v] = 1;
		}
	}

	// #########################################################################
	// #             Compute the percentage of node converage of g1	           #
	// #########################################################################
	double g1_node_coverage_percentage[g1_size][max_iter];
	for(int i = 0; i < g1_size; ++i)
	{
		int discovered[g1_size] = {0};
		discovered[i] = 1;
		int num_of_discovred_node = 1;
		list<int> g1_frontier;
		g1_frontier.push_back(i);

		for(int iter_num = 0; iter_num < max_iter; ++iter_num)
		{
			list<int> g1_new_frontier;
			for(auto it = g1_frontier.begin(); it != g1_frontier.end(); ++it)
			{
				for(int n = 0; n < g1_degree_sequence[*it]; ++n)
				{
					int nei = g1_neighbor_sequence[*it][n];
					if(!discovered[nei])
					{
						num_of_discovred_node++;
						g1_new_frontier.push_back(nei);
						discovered[nei] = 1;
					}
				}
			}
			double cov_percentage = (double)num_of_discovred_node / (double)g1_size;
			g1_node_coverage_percentage[i][iter_num] = cov_percentage;
			g1_frontier = g1_new_frontier;
		}
	}

	// #########################################################################
	// #             Compute the percentage of node converage of g2	           #
	// #########################################################################
	double g2_node_coverage_percentage[g2_size][max_iter];
	for(int u = 0; u < g2_size; ++u)
	{
		int discovered[g2_size] = {0};
		discovered[u] = 1;
		int num_of_discovred_node = 1;
		list<int> frontier;
		frontier.push_back(u);

		for(int iter_num = 0; iter_num < max_iter; ++iter_num)
		{
			list<int> new_frontier;
			for(auto it = frontier.begin(); it != frontier.end(); ++it)
			{
				for(int m = 0; m < g2_degree_sequence[*it]; ++m)
				{
					int nei = g2_neighbor_sequence[*it][m];
					if(!discovered[nei])
					{
						num_of_discovred_node++;
						new_frontier.push_back(nei);
						discovered[nei] = 1;
					}
				}
			}
			double cov_percentage = (double)num_of_discovred_node / (double)g2_size;
			g2_node_coverage_percentage[u][iter_num] = cov_percentage;
			frontier = new_frontier;
		}
	}

	// ###################################################
	// #              Compute the initial S              #
	// ###################################################
	double S_even[g1_size][g2_size]; // S_even is used as S at even iteration
	double S_odd[g1_size][g2_size]; // S_odd is used as S at odd iteration
	for(int i = 0; i < g1_size; ++i)
	{
		for(int u = 0; u < g2_size; ++u)
		{
			S_even[i][u] = (double) min(g1_degree_sequence[i], g2_degree_sequence[u]) / (double) max(g1_degree_sequence[i], g2_degree_sequence[u]);
		}
	}

	// ###################################################
	// #              Compute the initial b              #
	// ###################################################
	double b_g1[g1_size];
	double b_g2[g2_size];

	for(int i = 0; i < g1_size; ++i)
	{
		double max = 0.0;
		for(int u = 0; u < g2_size; ++u)
		{
			if(S_even[i][u] > max)
			{
				max = S_even[i][u];
			}
		}
		b_g1[i] = max;
	}

	for(int u = 0; u < g2_size; ++u)
	{
		double max = 0.0;
		for(int i = 0; i < g1_size; ++i)
		{
			if(S_even[i][u] > max)
			{
				max = S_even[i][u];
			}
		}
		b_g2[u] = max;
	}

	// #################################################
	// #              Initial Solution	               #
	// #################################################
	// Variables: g1_size, g2_size, g1_neighbor_sequence, g2_neighbor_sequence, g1_degree_sequence, g2_degree_sequence, g1_node_coverage_percentage, g2_node_coverage_percentage, S, b_g1, b_g2, max_iter
	
	double (*S)[g2_size];
	double (*S_new)[g2_size];

	for(int num_of_iter = 0; num_of_iter != max_iter; ++num_of_iter)
	{
		// -----------------------
		// -      Update S       -
		// -----------------------
		if (num_of_iter % 2) // if odd iteration
		{
			S = S_odd;
			S_new = S_even;
		}
		else // if even iteartion
		{
			S = S_even;
			S_new = S_odd;
		}
		// ---------------------------------------------------------
		// -        Sum of b value of neighbors & Threshold        -
		// ---------------------------------------------------------
		double sum_b_g1[g1_size] = {0.0};
		double g1_threshold[g1_size];
		for(int i = 0; i != g1_size; ++i)
		{
			g1_threshold[i] = g1_node_coverage_percentage[i][num_of_iter] * b_g1[i];
			for(int j_index = 0; j_index < g1_degree_sequence[i]; ++j_index)
			{
				int j = g1_neighbor_sequence[i][j_index];
				sum_b_g1[i] += b_g1[j];

			}
		}
		double sum_b_g2[g2_size] = {0.0};
		double g2_threshold[g2_size];
		for(int u = 0; u != g2_size; ++u)
		{
			g2_threshold[u] = g2_node_coverage_percentage[u][num_of_iter] * b_g2[u];
			for(int v_index = 0; v_index < g2_degree_sequence[u]; ++v_index)
			{
				int v = g2_neighbor_sequence[u][v_index];
				sum_b_g2[u] += b_g2[v];
			}
		}

		// ---------------------
		// -      New b        -
		// ---------------------
		double b_g1_new[g1_size] = {0.0};
		double b_g2_new[g2_size] = {0.0};

		// ------------------------------------------
		// -      Loop over all pairs of nodes      -
		// ------------------------------------------
		for(int i = 0; i < g1_size; ++i)
		{
			for(int u = 0; u < g2_size; ++u)
			{
				vector<array<double, 3>> B;
				double c = 0.0; // sum of similarity

				// i_neighbor_is_deleted[n] = 1 if the nth neighbor of i is deleted
				int i_neighbor_is_deleted[g1_degree_sequence[i]] = {0};
				int u_neighbor_is_deleted[g2_degree_sequence[u]] = {0};

				// ------------------------------------------------------------
				// -       Loop over all pairs of neighbors of i and u        -
				// ------------------------------------------------------------
				for(int j_index = 0; j_index < g1_degree_sequence[i]; ++j_index)
				{
					int j = g1_neighbor_sequence[i][j_index];
					for(int v_index = 0; v_index < g2_degree_sequence[u]; ++v_index)
					{
						if(!u_neighbor_is_deleted[v_index])
						{
							int v = g2_neighbor_sequence[u][v_index];
							if(S[j][v] == b_g1[j] == b_g2[v])
							{
								c += S[j][v];
								i_neighbor_is_deleted[j_index] = 1;
								u_neighbor_is_deleted[v_index] = 1;
								break;
							}
							else if(S[j][v] >= g1_threshold[j] || S[j][v] >= g2_threshold[v])
							{
								B.push_back( {(double)j_index, (double)v_index, S[j][v]} );
							}
						}
					}
				}
				// ----------------------------------------------------------------
				// -            Sort B by weight (the third element)              -
				// ----------------------------------------------------------------
				if(!B.empty())
				{
					sort(B.begin(), B.end(),[](const array<double, 3>& a, const array<double, 3>& b) {return a[2] > b[2];});
					for(int index = 0; index < B.size(); ++index)
					{
						if(B[index][2] > 0)
						{
							int j_index = (int)B[index][0];
							int v_index = (int)B[index][1];
							// ------------------------------------------------ 
							// -       If j and v have not been deleted       -
							// ------------------------------------------------
							if( (!i_neighbor_is_deleted[j_index]) && (!u_neighbor_is_deleted[v_index]) )
							{
								int j = g1_neighbor_sequence[i][j_index];
								int v = g2_neighbor_sequence[u][v_index];
								double similarity = B[index][2];
								double discrepancy = similarity;

								if(similarity == b_g1[j])
								{
									discrepancy = b_g2[v];
								}						
								else if(similarity == b_g2[v])
								{
									discrepancy = b_g1[j];
								}		
								else if(similarity < g1_threshold[j]) // similarity is greater than g2_threshold[v]
								{
									discrepancy = (similarity - g2_threshold[v]) / (b_g2[v] - g2_threshold[v]) * (b_g1[j] - g1_threshold[j]) + g1_threshold[j];
								}
								else if(similarity < g2_threshold[v]) // similarity is greater than g1_threshold[j]
								{
									discrepancy = (similarity - g1_threshold[j]) / (b_g1[j] - g1_threshold[j]) * (b_g2[v] - g2_threshold[v]) + g2_threshold[v];
								}
								c += 2 * similarity - discrepancy;

								i_neighbor_is_deleted[j_index] = 1;
								u_neighbor_is_deleted[v_index] = 1;
							}
						}
					}
				}

				// ------------------------------------
				// -      Compute new Similarity      -
				// ------------------------------------
				double maxi = max(sum_b_g1[i], sum_b_g2[u]);
				if(maxi == 0)
				{
					S_new[i][u] = 0.0;
				}
				else
				{
					S_new[i][u] = c / maxi;
				}

				// ------------------------------------------
				// -      Update b value if necessary       -
				// ------------------------------------------
				if(S_new[i][u] > b_g1_new[i])
				{
					b_g1_new[i] = S_new[i][u];
				}
				if(S_new[i][u] > b_g2_new[u])
				{
					b_g2_new[u] = S_new[i][u];
				}
			}
		}

		// -----------------------
		// -      Update b       -
		// -----------------------
		//! CAN BE OPTIMIZAED !!!
		for(int index = 0; index < g1_size; ++index)
		{
			b_g1[index] = b_g1_new[index];
		}
		for(int index = 0; index < g2_size; ++index)
		{
			b_g2[index] = b_g2_new[index];
		}
	}

	// #################################################
	// #           Extract the mapping from S          #
	// #################################################

	int num_of_pairs = g1_size * g2_size;
	array<double, 3> edge_weight_pairs[num_of_pairs]; //Format: [[i, u, S_new[i][u]]]
	int index = 0;
	for(int i = 0; i < g1_size; ++i)
	{
		for(int u = 0; u < g2_size; ++u)
		{
			edge_weight_pairs[index][0] = (double)i;
			edge_weight_pairs[index][1] = (double)u;
			edge_weight_pairs[index][2] = S_new[i][u];
			index++;
		}
	}
	sort(edge_weight_pairs, edge_weight_pairs + num_of_pairs, [](const array<double, 3>& a, const array<double, 3>& b) {return a[2] > b[2];});
	
	// ------------------------
	// -       Mapping        -
	// ------------------------
	//! HERE WE ASSUME THAT g1_size IS SMALLER, NOTE THAT THIS NEEDS TO BE UPDATED LATER
	int mapping[g1_size];

	//determine if a vertex has been seleted
	int g1_selected[g1_size] = {0};
	int g2_selected[g2_size] = {0};

	for(int index = 0; index < num_of_pairs; ++index)
	{
		int i = (int)edge_weight_pairs[index][0];
		int u = (int)edge_weight_pairs[index][1];
		if(!g1_selected[i] && !g2_selected[u])
		{
			mapping[i] = u;
			g1_selected[i] = 1;
			g2_selected[u] = 1;
		}
	}

	// ##########################
	// #      Initial EC        #
	// ########################## 
	int mapped_edges = 0;
	int total_edges = 0;
	int ini_objective = 0;
	for(int i = 0; i < g1_size; ++i)
	{
		int u = mapping[i];
		for(int j = 0; j < g1_size; ++j)
		{
			int v = mapping[j];
			ini_objective += C[i][j] * D[u][v];
			if(C[i][j])
			{
				total_edges += 1;
				if(D[u][v])
				{
					mapped_edges += 1;
				}
			}
		}
	}

	cout<<"------------------------------\n";
	cout<<"Initial Results:\n";
	double ini_ec = (double) mapped_edges / (double) total_edges;
	cout<<"Initial EC: "<<ini_ec<<endl;
	cout<<"Initial objective: "<<ini_objective<<endl;

	// ############################
	// #           Free           #
	// ############################
	delete[] g1_neighbor_sequence;
	delete[] g2_neighbor_sequence;

	return 0;
}
