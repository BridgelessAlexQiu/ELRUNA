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

    vector<string> vector_p = {"0.25"};

    string network_type; // real_network vs random_network
	string network_label;

    network_type = argv[1];
	network_label = argv[2];

    vector<double> ec_result_vector;
	vector<double> s3_result_vector;
    
    cout<<network_label<<" network:"<<endl;
    string p = "0.25";

    string g1_name; // name of the first network
    string g2_name; // name of the second network


    g1_name = "../datasets/self_under_noise/" + network_type + "/" + network_label + "/" + network_label + "_g1.edges";
    g2_name = "../datasets/self_under_noise/" + network_type + "/" + network_label + "/" + network_label + "_" + p + "_g2.edges";


    // I need this code because they used char* 
    int n1 = g1_name.length();
    int n2 = g2_name.length();
    char name1[n1 + 1]; 
    char name2[n2 + 1];
    strcpy(name1, g1_name.c_str()); 
    strcpy(name2, g2_name.c_str());

    char* blastFile;
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
    Alignment alignment(network1, network2);
    
    alignment.align(lambda, alpha);

    float ec = alignment.getEC();
    float s3 = alignment.getS3();

    cout<<"EC: "<<ec<<endl;
    cout<<"S3: "<<s3<<endl;
    
    return 0;
}

