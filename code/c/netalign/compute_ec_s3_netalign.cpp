/*
This program (for Netalign):
    1. Reads the two network file
    2. Reads the output alignment file (separated by tab)
    3. Compute the EC and S3
*/
#include <iostream>
#include <fstream>
#include <numeric>
#include <map>
#include <list>
#include <algorithm>
#include <vector>
#include <tuple>
#include <set>
#include <array>
#include <string>
#include <sstream>
#include <math.h>

using namespace std;

bool float_equal(double d1, double d2);

// arg list: g1.edges g2.edges max_iter [flag]
int main(int argc, char* argv[])
{
    vector<string> vector_p = {"0", "0.01", "0.03", "0.05", "0.07", "0.09", "0.11", "0.13", "0.15", "0.17", "0.19", "0.21", "0.23", "0.25"};
	
	string network_type; // real_network vs random_network
	string network_label;

    network_type = argv[1];
	network_label = argv[2];

    vector<double> ec_result_vector;
	vector<double> s3_result_vector;

    cout<<network_label<<" network:"<<endl;

    for(int unique_i = 0; unique_i < vector_p.size(); ++unique_i)
	{
		string p = vector_p[unique_i];

		string g1_network_file_name; // name of the first network
		string g2_network_file_name; // name of the second network
        string output_file_name;

		// the file types of random network and newman real networks are edgeslist
		if(network_label != "newman" && network_type != "random_network")
		{
			g1_network_file_name = "../datasets/self_under_noise/" + network_type + "/" + network_label + "/" + network_label + "_g1.edges";
			g2_network_file_name = "../datasets/self_under_noise/" + network_type + "/" + network_label + "/" + network_label + "_" + p + "_g2.edges";
		}
		else
		{
			g1_network_file_name = "../datasets/self_under_noise/" + network_type + "/" + network_label + "/" + network_label + "_g1.edgelist";
			g2_network_file_name = "../datasets/self_under_noise/" + network_type + "/" + network_label + "/" + network_label + "_" + p + "_g2.edgelist";
			if(network_type == "random_network" && unique_i == 12)
			{
				cout<<"EC: \n";
				cout<<"[";
				for(int i = 0; i < ec_result_vector.size(); ++i)
				{
					cout<<ec_result_vector[i]<<", ";
				}
				cout<<"]\n";

				cout<<"S3: \n";
				cout<<"[";
				for(int i = 0; i < s3_result_vector.size(); ++i)
				{
					cout<<s3_result_vector[i]<<", ";
				}
				cout<<"]\n";

				return 0; // p = 0.21 for random network
			} 
		}

        output_file_name = "output/netalign/self_under_noise/" + network_type + "/" + network_label + "/" + network_label + "_" + p + ".txt";

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

        // ######################################
        // #       Read in the output file      #
        // ######################################
        ifstream output_file(output_file_name); //The file object

        if(output_file.fail())// If we cannot locate the file
        {
            ec_result_vector.push_back(0.0);
            s3_result_vector.push_back(0.0);
        }
        else
        {
            // Construct mappings
            int mapping[g1_size];

            for(int i = 0; i < g1_size; ++i)
            {
                mapping[i] = -1;
            }

            string line;
            while (getline(output_file, line))  //reading network file
            {
                istringstream linestream(line);
                string node1, node2;
                
                //read the first node in a row
                getline(linestream, node1, '\t'); //first node
                if(node1.length() == 0) continue;
                int i1 = stoi(node1);

                getline(linestream, node2, '\t'); //second node
                int i2 = stoi(node2);

                mapping[i1] = i2;
                
            }
            output_file.close();
            
            // ###########################
            // #       Initial EC        #
            // ###########################
            int mapped_edges= 0;
            for(int i = 0; i < g1_size; ++i)
            {
                int u = mapping[i];
                if(u != -1)
                {
                    for(int j_index = 0; j_index < g1_degree_sequence[i]; ++j_index)
                    {
                        int j = g1_neighbor_sequence[i][j_index];
                        int v = mapping[j];
                        if(v != -1)
                        {
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
                }
            }

            double ini_ec = (double) mapped_edges / (double) (2 * g1_num_of_edges); // ! each mapped edges is counted twice
            ec_result_vector.push_back(ini_ec);

            // ##########################
            // #       Initial S3       #
            // ##########################
            mapped_edges /= 2; // ! each mapped edges is counted twice
            double ini_s3 = 0.0;
            if(g1_size == g2_size)
            {
                double denominator = (double) g1_num_of_edges + (double) g2_num_of_edges - (double) mapped_edges;
                ini_s3 = (double) mapped_edges / denominator;
                s3_result_vector.push_back(ini_s3);
            }
            else
            {
                cout<<"The code for computing S3 on networks with different sizes is not finished yet\n";
            }
        }
        
        // ###########################
        // #           Free          #
        // ###########################
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

    }// end of main for

    cout<<"EC: \n";
	cout<<"[";
	for(int i = 0; i < ec_result_vector.size(); ++i)
	{
		cout<<ec_result_vector[i]<<", ";
	}
	cout<<"]\n";

	cout<<"S3: \n";
	cout<<"[";
	for(int i = 0; i < s3_result_vector.size(); ++i)
	{
		cout<<s3_result_vector[i]<<", ";
	}
	cout<<"]\n";

	return 0;
}

bool float_equal(double d1, double d2)
{
	return ((fabs(d1 - d2) <= std::numeric_limits<double>::epsilon()));
}
