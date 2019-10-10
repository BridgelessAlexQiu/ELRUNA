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
#include "eigen/Eigen/SparseCore"
#include "eigen/Eigen/Core"
#include "eigen/Eigen/Dense"

typedef Eigen::Triplet<int> tri_int;
typedef Eigen::Triplet<double> tri_double;

using namespace std;

bool float_equal(double d1, double d2);

// arg list: g1.edges g2.edges max_iter [flag]
int main(int argc, char* argv[])
{
	char* g1_network_file_name; // name of the first network
	char* g2_network_file_name; // name of the second network
	int max_iter; //

	// If the number of additional argumnets is incorrect
	if(argc != 4)
	{
		cerr << "Please make sure you pass exactly two input files, one max_iter\n";
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
	int* g1_degree_sequence = new int[g1_size]; // Format: [degree_of_node0, degree_of_node1, ... ]

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
	int* g2_degree_sequence = new int[g2_size]; // Format: [degree_of_node0, degree_of_node1, ... ]

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

	cout<<"------------------------------\n";

	// -------------------------------------------------
	// -       trasition matrix of two networks        -
	// -------------------------------------------------
	Eigen::SparseMatrix<double> A (g1_size, g1_size); // G1
	Eigen::SparseMatrix<double> B (g2_size, g2_size); // G2

	vector<tri_double> triplet_list_for_A;
	vector<tri_double> triplet_list_for_B;

	triplet_list_for_A.reserve(2 * g1_num_of_edges);
	triplet_list_for_B.reserve(2 * g2_num_of_edges);

	for(int i = 0; i < g1_size; ++i)
	{
		for(int j_index = 0; j_index < g1_degree_sequence[i]; ++j_index)
		{
			int j = g1_neighbor_sequence[i][j_index];
			triplet_list_for_A.push_back(tri_double(i, j, (double) 1.0 / g1_degree_sequence[j]));
		}
	}
	A.setFromTriplets(triplet_list_for_A.begin(), triplet_list_for_A.end());

	for(int u = 0; u < g2_size; ++u)
	{
		for(int v_index = 0; v_index < g2_degree_sequence[u]; ++v_index)
		{
			int v = g2_neighbor_sequence[u][v_index];
			triplet_list_for_B.push_back(tri_double(u, v, (double) 1.0 / g2_degree_sequence[v]));
		}
	}
	B.setFromTriplets(triplet_list_for_B.begin(), triplet_list_for_B.end());

	// ----------------------------------------------------------
	// -         Similarity Matrix & Teportation Matrix         -
	// ----------------------------------------------------------
	Eigen::Matrix<double, Eigen::Dynamic, Eigen::Dynamic> S;
	S.resize(g2_size, g1_size);
	for(int u = 0; u < g2_size; ++u)
	{
		for(int i = 0; i < g1_size; ++i)
		{
			S(u, i) = (double) 1.0 / (g1_size * g2_size);
		}
	}
	Eigen::Matrix<double, Eigen::Dynamic, Eigen::Dynamic> H;
	H = S;

	// --------------------------------
	// -            IsoRank           -
	// --------------------------------
	double alpha = 0.5;
	double tolerance = 0.00000001;
	for(int iter = 1; iter <= max_iter; ++iter)
	{
		cout<<"Iteration: "<<iter<<endl;
		auto S_new = alpha * B * S * A.transpose() + (1 - alpha) * H;
		double error = (S_new - S).lpNorm<1>();
		S = S_new;
		if(error < tolerance * g1_size * g2_size) break;
	}

	//! HERE WE ASSUME THAT g1_size IS SMALLER, NOTE THAT THIS NEEDS TO BE UPDATED LATER
	int mapping[g1_size];
	map<int, int> inverse_mapping;

	// determine if a vertex has been seleted
	int g1_selected[g1_size] = {0};
	int g2_selected[g2_size] = {0};

	// ###############################
	// #           Alignment         #
	// ###############################
	int num_of_pairs = g1_size * g2_size;
	vector<array<double, 3>> edge_weight_pairs(num_of_pairs);

	int index = 0;
	for(int i = 0; i < g1_size; ++i)
	{
		for(int u = g2_size - 1; u >= 0; --u)
		{
			edge_weight_pairs[index][0] = (double)i;
			edge_weight_pairs[index][1] = (double)u;
			edge_weight_pairs[index][2] = S(u, i);
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
			inverse_mapping[u] = i;
			g1_selected[i] = 1;
			g2_selected[u] = 1;
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
	cout<<"Initial EC Isorank: "<<ini_ec<<endl;

	// ---------------------------
	// -           Free          -
	// ---------------------------
	delete[] g1_degree_sequence;
	delete[] g2_degree_sequence;

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

}
