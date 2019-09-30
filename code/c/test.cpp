#include<iostream>
#include<vector>
#include<map>
#include "eigen/Eigen/SparseCore"

typedef Eigen::Triplet<double> T;
using namespace std;

int main()
{
	Eigen::Matrix<int, 3, 1> M;
	M[0] = 10;
	Eigen::Matrix<int, 3, 1> N;
	N = M;
	cout<<N[0]<<endl;
	N[0] = 20;
	cout<<M[0]<<endl;
	cout<<N[0]<<endl;
	return 0;
}