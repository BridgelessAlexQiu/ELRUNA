#include <iostream>
#include <fstream>
#include <sstream>
#include <cstdlib>
#include "math.h"
#include <time.h>
#include <map>
#include <list>

using namespace std;

class Network
{
    typedef map<string, int , less<string> > MapString2Int;
	typedef map<int, list<int>, less<int> > MapInt2List;
	typedef map<int, string, less<int> > MapInt2Name;

	MapInt2Name mNames;
    
public:
    MapString2Int mapName;

	int **neighbor; //neighbor of each node of the network
	int size; //number of nodes
	int maxDeg;//maximum degree of the network
    int *deg; // degree of each node
    int *remNode;  //removed nodes
    int *newDeg;    //new degree of each node after each removing 
    float *nodeWeight; //weight of each node 
	float **edgeWeight; //weight of each edge
    int **remEdge;
    int numOfEdge; //number of edges 
	char* name; //name of the network
    
    //constructor, this function takes the network file and construct the graph of it. It finds the number of edges and the maximu degree of the network and assign to each node an ID.
    //Input parameter nam is the name of the file of the network.
	Network(char *nam); 
	
    //constructor.does nothing
    Network(void);
    
	//destructor
    ~Network(void); 
    
    //this function initialize some parameters of the network that should be determined during the alignment process. These paramters are weight of edges and nodes, new degree of each node that is equal to its degree at first and it detremines that there is no removed node at the beginning
    void skeletonInitialValue();
    
    //trim the network with respect to input t. It removes determined nodes in a way not to destroy their information to make the skeletone of the network. 
    //Input parameter t is the maximum degree for the nodes we want to be removed from the network. t could be at most 100.
    //result is the skeletone of the graph
    void makeSkeleton(int t);
    
    //this function removes nodes with degree one from the network
    //result is a network without any node of degree one.
    void removeDegOne();
    
    //this function removes the nodes with a degree equal or less than a determined input degree 
    //Input parameter degree identified the nodes are to be removed from the network.
    //result is a network without nodes of degree less than or equal to input degree.
    void removeDeg(int degree);
    
	//finds the corresponding name of a detremined ID. 
    //Input parameter id is the ID of the node we're looking for its name.
    //Output is the name of the corresponding node.
    string getName(int id)
	{
		return mNames[ id ];
	};
    
	//finds the corresponding id of a detremined name. 
    //Input parameter name is the name of the node we're looking for its ID.
    //Output is the ID of the corresponding node.    
	int getID(string name)
	{
		return mapName[ name ];
	};
private:
};
