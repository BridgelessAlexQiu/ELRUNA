#include "Alignment.h"
#include <iostream>
#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include <sstream>
#include <vector>

using namespace std;

exception er;

int main(int argc, char* argv[])
{
    double lambda;  //a is alpha that controlls the factor of edgeweights
    double alpha;
    int degree = 10; //controlls the step of making the skeleton

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

        // I need this code because they used char* 
        int n1 = g1_name.length();
        int n2 = g2_name.length();
        char name1[n1 + 1]; 
        char name2[n2 + 1];
        strcpy(name1, g1_name.c_str()); 
        strcpy(name2, g2_name.c_str());

        char* blastFile;
        try 
        {
            if(argc < 3) {
                cout << "There should be two files as input!" <<endl;
                return -1;
            }
            else //input arguments
            {
                int i = 1; //counter for input parameters
                i++;
                i++;
                
                while (i<argc) //check all the input parameters
                {
                    if ( ( strlen(argv[i]) == 2 ) && ( argv[i][0]=='-' ) && ( i + 1 < argc) ) //wether or not the parameter has started with '-' and has a value
                    {
                        i++; //to read the value of input parameter
                        if( argv[i-1][1]=='l' )
                        {
                            lambda = atof(argv[i]);
                            if( lambda <0 || lambda > 1) //the value of a should be between zero and one
                            {
                                cout << "Error : value of a must be between 0 and 1" << endl;
                                return -1;
                            }
                        }
                        else if( argv[i-1][1]=='d')
                        {
                            degree = atoi(argv[i]);
                            if( degree > 100)
                            {
                                cout << "Error : value of t must be between 0 and 100" << endl;
                                return -1;
                            }
                        }
                        else if(argv[i-1][1]=='b')
                        {
                            blastFile=argv[i];
                        }
                        else if(argv[i-1][1]=='a')
                        {
                            alpha = atof(argv[i]);
                        }

                        i++;// to reach the next input parameter if there is
                    }
                    else
                    {
                        cout <<  strlen(argv[i])<<i+1 << argc << endl;
                        cout << "Error in argument : " << argv[i] << endl; 
                        return -1;
                    }
                }
            } //end else

            //construct the networks
            Network network1(name1); 
            Network network2(name2);
            bool reverse = false; //it means size of first input network is bigger than second one
            
            if(network1.size > network2.size)
                reverse = true;
            //making the skeletons of the networks 

            network1.makeSkeleton(degree);
            network2.makeSkeleton(degree);
            
            //align two networks with each other
            Alignment alignment( network1, network2);
            if(alpha!=1) {
                alignment.readblast(blastFile);
            }
            
            alignment.align(lambda, alpha);
            
            //making the name for output file
            stringstream strm;
            strm << name1 << "-" << name2;
            alignment.outputEvaluation(strm.str());
            alignment.outputAlignment(strm.str());

            float ec = alignment.getEC();
            float s3 = alignment.getS3();
            
            ec_result_vector.push_back(ec);
            s3_result_vector.push_back(s3);
            
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

