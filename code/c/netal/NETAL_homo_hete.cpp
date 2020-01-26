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
    vector<string> homo_network_name = {"dblp", "digg", "elegan", "facebook"};
    vector<string> hete_network_name = {"ecoli_yeast", "flickr_lastfm", "flickr_myspace", "offline_online", "syne_yeast"};

	double aa = 0.0001, bb = 0, cc = 1; // weighting parameters in the paper
    
	int it = 2;     // Number of iterations when calculating the similarity
	int rr = 0;     // The type of randomness
	int pp = 0;     // The percentage of randomness
	int nn = 1;     // The number of random networks
	
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

        // I need this code because they used char* 
        int n1 = g1_network_file_name.length(); 
        int n2 = g2_network_file_name.length();
        char name1[n1 + 1]; 
        char name2[n2 + 1];
        strcpy(name1, g1_network_file_name.c_str()); 
        strcpy(name2, g2_network_file_name.c_str());

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

        cout<<"EC: "<<EC<<endl;
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

        // I need this code because they used char* 
        int n1 = g1_network_file_name.length(); 
        int n2 = g2_network_file_name.length();
        char name1[n1 + 1]; 
        char name2[n2 + 1];
        strcpy(name1, g1_network_file_name.c_str()); 
        strcpy(name2, g2_network_file_name.c_str());

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

        cout<<"EC: "<<EC<<endl;

    }
   
    return 0;
}



