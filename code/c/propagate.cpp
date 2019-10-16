// // #########################
	// // #       C, D & E        #
	// // #########################
	// int g3_size = 2 * g1_size; // we only consider the subgraph of G2 induced by mappings of vertices in G1
	// map<int, int> g2_induced_degree_sequence; // same as above
	//
	// int** C = new int*[g1_size]; // C
	// for(int i = 0; i < g1_size; ++i)
	// {
	// 	C[i] = new int[g1_size];
	// 	for(int j = 0; j < g1_size; ++j)
	// 	{
	// 		C[i][j] = 0;
	// 	}
	// }
	//
	// int** D = new int*[g2_size]; // D
	// for(int u = 0; u < g2_size; ++u)
	// {
	// 	D[u] = new int[g2_size];
	// 	for(int v = 0; v < g2_size; ++v)
	// 	{
	// 		D[u][v] = 0;
	// 	}
	// }
	//
	// Eigen::SparseMatrix<int> E (g3_size, g3_size); // The adjacency matrix of G3. default value is 0
	//
	// // -------------------
	// // -        D        -
	// // -------------------
	// for(int u = 0; u < g2_size; ++u)
	// {
	// 	for(int v_index = 0; v_index < g2_degree_sequence[u]; ++v_index)
	// 	{
	// 		int v = g2_neighbor_sequence[u][v_index];
	// 		D[u][v] = 1;
	// 	}
	// }
	// // -----------------------
	// // -        C & E        -
	// // -----------------------
	// vector<tri_int> triplet_list_for_E;
	// triplet_list_for_E.reserve(2 * g1_size + 2 * g1_num_of_edges + 2 * g2_num_of_edges);
	// for(int i = 0; i < g1_size; ++i)
	// {
	// 	int u = mapping[i];
	// 	int induced_degree_of_u = 0;
	// 	int matrix_index_of_u = g1_size + i;
	//
	// 	for(int k = 0; k < g1_size; ++k)
	// 	{
	// 		int v = mapping[k];
	// 		int matrix_index_of_v = g1_size + k;
	// 		if(D[u][v] == 1)
	// 		{
	// 			triplet_list_for_E.push_back(tri_int(matrix_index_of_u, matrix_index_of_v, 1));
	// 			induced_degree_of_u += 1;
	// 		}
	// 	}
	// 	g2_induced_degree_sequence[u] = induced_degree_of_u;
	//
	// 	//Bridges between G1 and G2
	// 	triplet_list_for_E.push_back(tri_int(matrix_index_of_u, i, 1));
	// 	triplet_list_for_E.push_back(tri_int(i, matrix_index_of_u, 1));
	//
	// 	for(int j_index = 0; j_index < g1_degree_sequence[i]; ++j_index)
	// 	{
	// 		int j = g1_neighbor_sequence[i][j_index];
	// 		C[i][j] = 1;
	// 		triplet_list_for_E.push_back(tri_int(i, j, 1));
	// 	}
	// }
	// E.setFromTriplets(triplet_list_for_E.begin(), triplet_list_for_E.end());
	//
	// // #################################
	// // #       Initial violation       #
	// // #################################
	// Eigen::Matrix<double, Eigen::Dynamic, 1> initial_violation;
	// initial_violation.resize(g3_size, 1);
	// double total_violation_sum = 0.0;
	//
	// for(int i = 0; i < g1_size; ++i)
	// {
	// 	int u = mapping[i];
	// 	int matrix_index_of_u = g1_size + i;
	// 	int conserved_edges = 0;
	//
	// 	for(int j_index = 0; j_index < g1_degree_sequence[i]; ++j_index)
	// 	{
	// 		int j = g1_neighbor_sequence[i][j_index];
	// 		int v = mapping[j];
	// 		conserved_edges += D[u][v];
	// 	}
	// 	double violation_of_i = (double) (g1_degree_sequence[i] - conserved_edges) / (g1_degree_sequence[i]);
	// 	double violation_of_u = (double) (g2_induced_degree_sequence[u] - conserved_edges) / (g2_induced_degree_sequence[u]);
	//
	// 	total_violation_sum = total_violation_sum + violation_of_i + violation_of_u;
	//
	// 	initial_violation[i] = violation_of_i;
	// 	initial_violation[matrix_index_of_u] = violation_of_u;
	// }
	//
	// // ################################################################
	// // #      Quantify the degree of mismatching (random walk)        #
	// // ################################################################
	// double alpha = 0.5; // damping factor
	// int power_method_max_iter = 100;
	// double tolerance = 0.000001;
	//
	// // --------------------------------------------------------------------
	// // -        Transition matrix, initial R & normalized violation       -
	// // --------------------------------------------------------------------
	// Eigen::SparseMatrix<double> left_stochastic_E (g3_size, g3_size);
	// vector<tri_double> triplet_list_for_sto_E;
	// triplet_list_for_E.reserve(2 * g1_size + 2 * g1_num_of_edges + 2 * g2_num_of_edges);
	//
	// initial_violation.normalize();
	//
	// Eigen::Matrix<double, Eigen::Dynamic, 1> R;
	// R.resize(g3_size, 1);
	//
	// for(int i = 0; i < g3_size; ++i)
	// {
	// 	R[i] = (double) 1.0 / g3_size;
	// }
	//
	// for (int k=0; k<E.outerSize(); ++k)
	// {
	// 	for (Eigen::SparseMatrix<int>::InnerIterator it(E,k); it; ++it)
	// 	{
	// 		int c = it.col();
	// 		int r = it.row();
	// 		if(c <= g1_size)
	// 		{
	// 			triplet_list_for_sto_E.push_back(tri_double(r, c, (double) 1.0 / (g1_degree_sequence[c] + 1)));
	// 		}
	// 		else
	// 		{
	// 			int u = mapping[c - g1_size];
	// 			triplet_list_for_sto_E.push_back(tri_double(r, c, (double) 1.0 / (g2_induced_degree_sequence[u] + 1)));
	// 		}
	// 	}
	// }
	// left_stochastic_E.setFromTriplets(triplet_list_for_sto_E.begin(), triplet_list_for_sto_E.end());
	//
	// // ----------------------------
	// // -        Random walk       -
	// // ----------------------------
	// cout<<"Ramdom walk starts:\n";
	// for(int iteration = 1; iteration <= power_method_max_iter; ++iteration)
	// {
	// 	cout<<"Iteration: "<<iteration<<endl;
	// 	auto R_new = alpha* left_stochastic_E * R + (1 - alpha) * initial_violation;
	// 	double error = (R_new - R).lpNorm<1>();
	//
	// 	R = R_new;
	// 	if(error < tolerance * g1_size) break;
	// }
	//
	// // -------------------------------------
	// // -       Rank vertices in g1          -
	// // -------------------------------------
	// vector<array<double, 2>> node_ranking_pari(g3_size);
	//
	// int index = 0;
	// for(int i = 0; i < g3_size; ++i)
	// {
	// 	node_ranking_pari[index][0] = i;
	// 	node_ranking_pari[index][1] = R[i];
	// 	index++;
	// }
	//
	// sort(node_ranking_pari.begin(), node_ranking_pari.end(), [](const array<double, 2>& a, const array<double, 2>& b) {return a[1] > b[1];});
	//
	// vector<int> nodes_in_g1_by_ranking;
	// nodes_in_g1_by_ranking.reserve(g1_size);
	// for(int i = 0; i < g3_size; ++i)
	// {
	// 	if(node_ranking_pari[i][0] < g1_size)
	// 	{
	// 		nodes_in_g1_by_ranking.push_back(i);
	// 	}
	// }
	
	// for(int i = 0; i < g1_size; ++i)
	// {
	// 	delete [] C[i];
	// }
	// delete[] C;
	// for(int i = 0; i < g2_size; ++i)
	// {
	// 	delete [] D[i];
	// }
	// delete[] D;