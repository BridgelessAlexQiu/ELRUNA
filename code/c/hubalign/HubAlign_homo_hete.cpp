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
    double lambda = 0.1;  //a is alpha that controlls the factor of edgeweights
    double alpha = 1.0;
    int degree = 10; //controlls the step of making the skeleton

    vector<string> homo_network_name = {"dblp", "digg", "elegan", "facebook"};
    vector<string> hete_network_name = {"ecoli_yeast", "flickr_lastfm", "flickr_myspace", "offline_online", "syne_yeast"};

    // ################################ 
    // #          Homogeneous         #
    // ################################ 
    for(int i = 0; i < homo_network_name.size(); ++i)
    {
        string network_type = "homogeneous";
	    string network_label = homo_network_name[i];

        cout<<network_type<<"/"<<network_label<<" network:"<<endl;

        string g1_network_file_name = "../datasets/" + network_type +"/" + network_label + "/" + network_label + "_g1.edges"; // name of the first network
		string g2_network_file_name = "../datasets/" + network_type +"/" + network_label + "/" + network_label + "_g2.edges";  // name of the second network

        cout<<network_label<<" network:"<<endl;

        // I need this code because they used char* 
        int n1 = g1_network_file_name.length();
        int n2 = g2_network_file_name.length();
        char name1[n1 + 1]; 
        char name2[n2 + 1];
        strcpy(name1, g1_network_file_name.c_str()); 
        strcpy(name2, g2_network_file_name.c_str());

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
        
        cout<<"EC: "<<ec<<endl;
    }

    // ################################ 
    // #         Heterogeneous        #
    // ################################ 
    for(int i = 0; i < hete_network_name.size(); ++i)
    {
        string network_type = "heterogeneous";
	    string network_label = hete_network_name[i];
        auto place = network_label.find("_");
        string g1_name = network_label.substr(0, place);
        string g2_name = network_label.substr(place+1);

        cout<<network_type<<"/"<<network_label<<" network:"<<endl;

        string g1_network_file_name = "../datasets/" + network_type +"/" + network_label + "/" + g1_name + ".edges"; // name of the first network
		string g2_network_file_name = "../datasets/" + network_type +"/" + network_label + "/" + g2_name + ".edges";  // name of the second network

        cout<<network_label<<" network:"<<endl;

        // I need this code because they used char* 
        int n1 = g1_network_file_name.length();
        int n2 = g2_network_file_name.length();
        char name1[n1 + 1]; 
        char name2[n2 + 1];
        strcpy(name1, g1_network_file_name.c_str()); 
        strcpy(name2, g2_network_file_name.c_str());

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
        
        cout<<"EC: "<<ec<<endl;

    }

    return 0;
}

