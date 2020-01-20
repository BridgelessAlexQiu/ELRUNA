#include "Alignment.h"
#include <iostream>
#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include <vector>
#include <sstream>

using namespace std;

int main(int argc, char* argv[])
{
	double aa = 0.0001, bb = 0, cc = 1; // weighting parameters in the paper
    
	int it = 2;     // Number of iterations when calculating the similarity
	int rr = 0;     // The type of randomness
	int pp = 0;     // The percentage of randomness
	int nn = 1;     // The number of random networks
	
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

		string g1_name; // name of the first network
		string g2_name; // name of the second network

		// the file types of random network and newman real networks are edgeslist
		if(network_label != "newman" && network_type != "random_network")
		{
			g1_name = "../datasets/self_under_noise/" + network_type + "/" + network_label + "/" + network_label + "_g1.edges";
			g2_name = "../datasets/self_under_noise/" + network_type + "/" + network_label + "/" + network_label + "_" + p + "_g2.edges";
		}
		else
		{
			g1_name = "../datasets/self_under_noise/" + network_type + "/" + network_label + "/" + network_label + "_g1.edgelist";
			g2_name = "../datasets/self_under_noise/" + network_type + "/" + network_label + "/" + network_label + "_" + p + "_g2.edgelist";
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

        try
        {
            
            if(argc < 3) {
                cout << "There should be two files as input!" <<endl;
                return -1;
            }
            else //input arguments
            {
                // I need this code because they used char* 
                int n1 = g1_name.length(); 
                int n2 = g2_name.length();
                char name1[n1 + 1]; 
                char name2[n2 + 1];
                strcpy(name1, g1_name.c_str()); 
                strcpy(name2, g2_name.c_str());

                //construct the first network
                Network network1(name1);
    
                //construct the first network
                Network network2(name2);
                
                bool reverse = false; //it means size of first input network is bigger than second one
                
                if(network1.size > network2.size)
                    reverse = true;
                
                //Initializes the alignment class
                Alignment alignment( network1, network2 );
                
                //Calculates the similarity values
                alignment.setSimilarities(it, bb, cc);
                
                //Aligns two networks
                alignment.align(aa);
                
                //calculation of evaluating measures
                int CCCV = 0, CCCE = 0; //LCCS based on vertex and edge
                float EC = 0, NC = 0, IC = 0, S3 = 0;
                CCCV += alignment.CCCV;
                CCCE += alignment.CCCE;
                EC += alignment.EC;
                NC += alignment.NC;
                IC += alignment.IC;
                S3 += alignment.S3;

                ec_result_vector.push_back(EC);
                s3_result_vector.push_back(S3);
                
                //making the name for output file
                stringstream strm;
                strm << "(" << name1 << "-" << name2;
                if( rr > 0 )
                    strm << rr << "r" << pp;
                strm << ")" << "-a" << aa << "-b" << bb << "-c" << cc << "-i" << it;
                
                //no random alignment
                if(rr == 0)
                {
                    alignment.outputEvaluation(strm.str());
                    alignment.outputAlignment(strm.str());
                }
                //random alignment
                else
                {
                    int edgeNum; //percent of randome edges should be removed
                    
                    for( int i = 1; i < nn; i++ )
                    {
                        
                        //cout << "-------------------------------> Random Netowrk:  " << i << endl; //print the iteration number
                        Network network2(name2);
                        edgeNum = pp * network2.numOfEdge / 100;
                        
                        if( rr == 1) //construct the random graph with removing edges randomly
                        {
                            network2.randomEdgeRemoval( edgeNum );
                        }
                        else if(rr == 2) //construct the random graph with adding edges randomly
                        {
                            network2.randomEdgeAddition( edgeNum );
                        }
                        else if(rr == 3) //construct the random graph with removing and adding edges randomly
                        {
                            network2.randomEdgeRemoval( edgeNum );
                            network2.randomEdgeAddition( edgeNum );
                        }
                        
                        //find the alignment
                        Alignment alignment( network1, network2 );
                        alignment.setSimilarities(it, bb, cc);
                        alignment.align(aa);
                        
                        //calculate the eavluation measurements
                        CCCV += alignment.CCCV;
                        CCCE += alignment.CCCE;
                        EC += alignment.EC;
                        NC += alignment.NC;
                        IC += alignment.IC;
                        
                        //print the results in files
                        alignment.outputEvaluation(strm.str());
                        alignment.outputAlignment(strm.str());
                    }
                
                }
            }
        }
        catch(exception &e)
        {
            cout << "Error in arguments or input files!" << endl;
            e.what();
            return -1;
        }

    }

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



