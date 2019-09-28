#include <iostream>
#include <fstream>
#include <numeric>
#include <map>
#include <list>
#include <algorithm> 
#include <vector>
#include <tuple>
#include <array>
#include <string>

using namespace std;

bool float_equal(double d1, double d2);

// arg list: g1.edges g2.edges max_iter [flag]
int main(int argc, char* argv[])
{
	char* g1_network_file_name; // name of the first network
	char* g2_network_file_name; // name of the second network
	int max_iter; // The diameter of the graph
	bool use_default_alignment_method = 1; // 0: use the advanced alignment method; 1: default alignment method

	// If the number of additional argumnets is incorrect
	if(argc != 4 && argc != 5)
	{
		cerr << "Please make sure you pass exactly two input files, one max_iter, and possibly one flag \n";
		return -1;
	}
	
	// Assign the network files and the number of iterations
	g1_network_file_name = argv[1];
	g2_network_file_name = argv[2];
	max_iter = atoi(argv[3]);
	if(argc == 5)
	{
		use_default_alignment_method = atoi(argv[4]);
	}

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
	map<string, int> g1_name_id_mapping; // Format: {name : id}

	string i_name, j_name; // Node i and j
	while(g1_network_file>>i_name>>j_name) // We assume that the nodes are separated by whitespaces
	{
		// -----------------------------------------------------
		// -   Assign an id to i (if has not been assigned)    - 
		// -----------------------------------------------------
		g1_name_id_mapping.insert(map<string, int>::value_type(i_name, (int)g1_name_id_mapping.size()));
		int i = g1_name_id_mapping[i_name];
		
		// --------------------------------------------------------------------------
		// -       Create spaces for i's neighbors (if has not been created)        -
		// --------------------------------------------------------------------------
		list<int> i_neighbors;
		// Insert operation checks if the node exists in the map, if so, the element is not inserted
		g1_neighbor_map.insert(map<int, list<int>>::value_type(i, i_neighbors));

		// -----------------------------------------------------
		// -   Assign an id to j (if has not been assigned)    - 
		// -----------------------------------------------------
		g1_name_id_mapping.insert(map<string, int>::value_type(j_name, (int)g1_name_id_mapping.size()));
		int j = g1_name_id_mapping[j_name];

		// --------------------------------------------------------------------------
		// -       Create spaces for j's neighbors (if has not been created)        -
		// --------------------------------------------------------------------------
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

		int j_index = 0;
		for (auto list_it = neighbors.begin(); list_it != neighbors.end(); ++list_it)
		{
			g1_neighbor_sequence[i][j_index] = *list_it;	
			j_index++;
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
	map<string, int> g2_name_id_mapping; // Format: {name : id}

	string u_name, v_name; // Node u and v
	while(g2_network_file>>u_name>>v_name)
	{
		// -----------------------------------------------------
		// -   Assign an id to u (if has not been assigned)    - 
		// -----------------------------------------------------
		g2_name_id_mapping.insert(map<string, int>::value_type(u_name, (int)g2_name_id_mapping.size()));
		int u = g2_name_id_mapping[u_name];

		list<int> u_neighbors;
		// Insert operation checks if the node exists in the map, if so, the element is not inserted
		g2_neighbor_map.insert(map<int, list<int>>::value_type(u, u_neighbors));

		// -----------------------------------------------------
		// -   Assign an id to v (if has not been assigned)    - 
		// -----------------------------------------------------
		g2_name_id_mapping.insert(map<string, int>::value_type(v_name, (int)g2_name_id_mapping.size()));
		int v = g2_name_id_mapping[v_name];

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

		int v_index = 0;
		for (auto list_it = neighbors.begin(); list_it != neighbors.end(); ++list_it)
		{
			g2_neighbor_sequence[u][v_index] = *list_it;	
			v_index++;
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
	cout<<"Average degree: "<<(double) (2 * g1_num_of_edges) / (g1_size) <<endl;

	cout<<"------------------------------\n";
	
	cout<<"G2:"<<endl;
	cout<<"Number of nodes: "<<g2_size<<endl;
	cout<<"Number of edges: "<<g2_num_of_edges<<endl;
	cout<<"Average degree: "<<(double) (2 * g2_num_of_edges) / (g2_size) <<endl;
	
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
	double** S_even = new double*[g1_size]; // S_even is used as S at even iteration
	for(int i = 0; i < g1_size; ++i)
	{
		S_even[i] = new double[g2_size];
	}
	double** S_odd = new double*[g1_size]; // S_odd is used as S at odd iteration
	for(int i = 0; i < g1_size; ++i)
	{
		S_odd[i] = new double[g2_size];
	}

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

	double** S;
	double** S_new;

	for(int num_of_iter = 0; num_of_iter != max_iter; ++num_of_iter)
	{
		cout<<"Iteration: "<<num_of_iter<<endl;
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
		double sum_b_g1[g1_size];
		for(int i = 0; i < g1_size; ++i)
		{
			sum_b_g1[i] = 0.0;
		}

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
		double sum_b_g2[g2_size];
		for(int u = 0; u < g2_size; ++u)
		{
			sum_b_g2[u] = 0.0;
		}

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
		for(int i = 0; i < g1_size; ++i)
		{
			b_g1_new[i] = 0.0;
		}
		double b_g2_new[g2_size] = {0.0};
		for(int u = 0; u < g2_size; ++u)
		{
			b_g2_new[u] = 0.0;
		}

		// ------------------------------------------
		// -      Loop over all pairs of nodes      -
		// ------------------------------------------
		for(int i = 0; i < g1_size; ++i)
		{
			for(int u = 0; u < g2_size; ++u)
			{
				int reserved_size = g1_degree_sequence[i] * g2_degree_sequence[u];
				int total_pairs_in_B = 0;
				vector<array<double, 3>> B (reserved_size);
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
							if(float_equal(S[j][v], b_g1[j]) && float_equal(b_g1[j], b_g2[v]))
							{
								if(S[j][v] < 0) // this should never happen
								{
									cout<<S[j][v]<<" "<<b_g1[j]<<endl;
								}
								c += S[j][v];
								i_neighbor_is_deleted[j_index] = 1;
								u_neighbor_is_deleted[v_index] = 1;
								break;
							}
							else if(S[j][v] >= g1_threshold[j] || S[j][v] >= g2_threshold[v])
							{
								B[total_pairs_in_B] = {(double)j_index, (double)v_index, S[j][v]};
								total_pairs_in_B += 1;
							}
						}
					}
				}
				B.resize(total_pairs_in_B);	
			
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

								if(float_equal(similarity, b_g1[j]))
								{
									discrepancy = b_g2[v];
								}						
								else if(float_equal(similarity, b_g2[v]))
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

				if(float_equal(maxi, 0.0)) // if(maxi <= 0.0 || c <= 0.0)
				{
					S_new[i][u] = 0.0;
				}
				else
				{
					S_new[i][u] = c / maxi;
					if(S_new[i][u] < -1) cout<<S_new[i][u]<<endl;
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

	//! HERE WE ASSUME THAT g1_size IS SMALLER, NOTE THAT THIS NEEDS TO BE UPDATED LATER
	int mapping[g1_size];
	// determine if a vertex has been seleted
	int g1_selected[g1_size] = {0};
	int g2_selected[g2_size] = {0};

	if(use_default_alignment_method)
	{
		// #########################################
		// #           Alignment method 1          #
		// #########################################
		int num_of_pairs = g1_size * g2_size;
		vector<array<double, 3>> edge_weight_pairs(num_of_pairs); 

		int index = 0;
		for(int i = 0; i < g1_size; ++i)
		{
			for(int u = g2_size - 1; u >= 0; --u)
			{
				edge_weight_pairs[index][0] = (double)i;
				edge_weight_pairs[index][1] = (double)u;
				edge_weight_pairs[index][2] = S_new[i][u];
				index++;
			}
		}
		sort(edge_weight_pairs.begin(), edge_weight_pairs.end(), [](const array<double, 3>& a, const array<double, 3>& b) {return a[2] > b[2];});
		
		// ------------------------
		// -       Mapping        -
		// ------------------------
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
	}

	else
	{
		// ############################################
		// #            Alignment method 2            #
		// ############################################
		int num_of_aligned_node = 0;

		while(num_of_aligned_node != g1_size)
		{
			double max_similarity = -10000.0;
			int max_i;
			int max_u;
			for(int i = 0; i < g1_size; ++i)
			{
				if(!g1_selected[i])
				{
					for(int u = g2_size - 1; u >= 0; --u)
					{
						if(!g2_selected[u])
						{
							if(S_new[i][u] > max_similarity)
							{
								max_i = i;
								max_u = u;
								max_similarity = S_new[i][u];
							}
						}
					}
				}
			}
			num_of_aligned_node++;
			mapping[max_i] = max_u;
			g1_selected[max_i] = 1;
			g2_selected[max_u] = 1;

			for(int i_nei_index = 0; i_nei_index < g1_degree_sequence[max_i]; ++i_nei_index)
			{
				int i_nei = g1_neighbor_sequence[max_i][i_nei_index];
				if(!g1_selected[i_nei])
				{
					for(int u_nei_index = 0; u_nei_index < g2_degree_sequence[max_u]; ++u_nei_index)
					{
						int u_nei = g2_neighbor_sequence[max_u][u_nei_index];
						if(!g2_selected[u_nei])
						{
							S_new[i_nei][u_nei] += 1;
						}
					}
				}
			}
		}
	}

	// ##########################
	// #       Initial EC       #
	// ##########################
	int mapped_edges = 0;
	for(int i = 0; i < g1_size; ++i)
	{
		int u = mapping[i];
		for(int j_index = 0; j_index < g1_degree_sequence[i]; ++j_index)
		{
			int j = g1_neighbor_sequence[i][j_index];
			int v = mapping[j];
			for(int u_nei_index = 0; u_nei_index < g2_degree_sequence[u]; ++u_nei_index)
			{
				int u_nei = g2_neighbor_sequence[u][u_nei_index];
				if(v == u_nei)
				{
					mapped_edges += 1;
					break;
				}
			}
		}
	}
	
	cout<<"------------------------------\n";
	cout<<"Initial Results:\n";
	double ini_ec = (double) mapped_edges / (double) (2 * g1_num_of_edges);
	cout<<"Initial EC: "<<ini_ec<<endl;
	cout<<"Initial objective: "<<mapped_edges<<endl;

	// ############################
	// #           Free           #
	// ############################
	for(int i = 0; i < g1_size; ++i)
	{
		delete[] g1_neighbor_sequence[i];
	}
	delete[] g1_neighbor_sequence;

	for(int u = 0; u < g2_size; ++u)
	{
		delete[] g2_neighbor_sequence[u];
	}
	delete[] g2_neighbor_sequence;

	for(int i = 0; i < g2_size; ++i)
	{
		delete[] S_even[i];
	}
	delete[] S_even;

	for(int i = 0; i < g2_size; ++i)
	{
		delete[] S_odd[i];
	}
	delete[] S_odd;

	return 0;
}

bool float_equal(double d1, double d2)
{
	return ((fabs(d1 - d2) <= std::numeric_limits<double>::epsilon()));
}