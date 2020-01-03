#include "Alignment.h"
#include <fstream>
#include <cstdlib>

using namespace std;
//constructor
//finds the smaller network and the maximum degree of the input networks
//Inputs are two files of networks net1 and net2
Alignment::Alignment( Network net1, Network net2)
{
    //compare networks to find the biggest one
    if( net1.size > net2.size )
	{
		reverse = true;
		network1 = net2;
		network2 = net1;
	}
	else
	{
		reverse = false;
		network1 = net1;
		network2 = net2;
	}
    
	//maximum degree of the network
    if(network1.maxDeg > network2.maxDeg)
		maxDeg = network1.maxDeg;
	else
		maxDeg = network2.maxDeg;
    
    blast = new float*[network1.size];
    for (int c=0; c<network1.size; c++) {
        blast[c]=new float[network2.size];
    }
    for (int c1=0; c1<network1.size; c1++) {
        for (int c2=0; c2<network2.size; c2++) {
            blast[c1][c2]=0;
        }
    }
}

void Alignment::readblast(string blastFile) { 
    
    float ** temp = new float*[network1.size];
    for (int c=0; c<network1.size; c++) {
        temp[c]=new float[network2.size];
    }
    for (int c1=0; c1<network1.size; c1++) {
        for (int c2=0; c2<network2.size; c2++) {
            temp[c1][c2]=0;
        }
    }

    float max = 0 ; 
    //blast values
    
    ifstream inputFile;
    string token1,token2,line;
    float token3;
    inputFile.open(blastFile.c_str());
    while (getline(inputFile, line)) {
        istringstream tokenizer(line);
        getline(tokenizer, token1, '\t');
        getline(tokenizer, token2, '\t');
        tokenizer >> token3;
        if(max<token3) max = token3;
        temp[network1.mapName[token1]][network2.mapName[token2]]=token3;
    }
    
    //normalize between zero and 1
    for (int c1=0; c1<network1.size; c1++) 
        for (int c2=0; c2<network2.size; c2++) 
            blast[c1][c2] = temp[c1][c2]/max; 
}

//produce a mapping between nodes of two network with respect to input parameter a. 
//Input parameter a acontrols the factor edgeWeight in assigning the scores to the nodes. a should be between 0 and 1.
void Alignment::align(double lambda, double alpha)
{
    bool flag;  //check wether or not all the nodes of the smaller network are aligned?
    
    //temporary
    float temp; 
    float a1,a11;   
    float a2,a22; 
    float MINSCORE = -100000;
    int coeff;
    if(network2.numOfEdge>network1.numOfEdge) {
        coeff = network2.numOfEdge/network1.numOfEdge;
    }
    else {
        coeff = network1.numOfEdge/network2.numOfEdge;
        
    }
    int maxNode; // node with max score
    bool *alignNodes1 = new bool[network1.size]; //aligned nodes of the smaller network
    bool *alignNodes2 = new bool[network2.size]; //aligned nodes of the bigger network
    alignment = new int[network1.size]; //alignment array
    float *nodeScore1 = new float[network1.size]; //scores of nodes of smaller network
    float *nodeScore2 = new float[network2.size]; //scores of nodes of bigger network
    double **alignScore = new double*[network1.size]; //this matrix contains the score of each matching pair
    int *best = new int[network1.size]; //array of best align scores
    float ss;
    //initial values
    for(int c1=0; c1<network1.size; c1++)
        alignScore[c1]=new double[network2.size];       
    for(int c1=0; c1<network1.size; c1++)
        alignNodes1[c1]=false;
    for(int c1=0; c1<network2.size; c1++)
        alignNodes2[c1]=false;    
    for(int c1=0; c1<network1.size; c1++)
        alignment[c1]=-1;
    for(int c1=0; c1<network1.size; c1++)
        best[c1]=-1;
    
    ofstream NS;
    //initialize nodeScore fro both networks
    for(int c1=0; c1< network1.size; c1++)
        nodeScore1[c1]=(1-lambda)*network1.nodeWeight[c1];
    for(int c1=0; c1< network2.size; c1++)
        nodeScore2[c1]=(1-lambda)*network2.nodeWeight[c1];
    
    //find max score 
    //finding the nodescore
    for (int c1=0; c1<network1.size; c1++){
        for (int c2=0; c2<network1.size; c2++) 
            nodeScore1[c1]+= lambda*network1.edgeWeight[c1][c2];
    }
    for (int c1=0; c1<network2.size; c1++){
        for (int c2=0; c2<network2.size; c2++)
            nodeScore2[c1] += lambda*network2.edgeWeight[c1][c2];
     } 

    //======first network
    float max = -10000;
    for (int c1=0; c1<network1.size; c1++) {
        if (max < nodeScore1[c1]) {
            max = nodeScore1[c1];
        }
    }

    //====== second network
    for (int c1=0; c1<network2.size; c1++) {
        if (max < nodeScore2[c1]) {
            max = nodeScore2[c1];
        }
    }
    
    //normalize with respect to max
    for (int c1=0; c1<network1.size; c1++) {
        nodeScore1[c1] = nodeScore1[c1]/max; 
    }    
    
    for (int c1=0; c1<network2.size; c1++) {
        nodeScore2[c1] = nodeScore2[c1]/max;  
    }    
    //END of normalization
    
    //finding the alignscore
    for(int c1=0; c1<network1.size; c1++)
        for(int c2=0; c2<network2.size; c2++){
            alignScore[c1][c2] = (nodeScore1[c1]>nodeScore2[c2])? nodeScore2[c2]:nodeScore1[c1];
            alignScore[c1][c2] = alpha * (alignScore[c1][c2]);
            alignScore[c1][c2] += (1-alpha)*blast[c1][c2]; //adding similarity
        } 
    
    int counter = 0;
    flag=true;
    int temp1,temp2;
    
    int counteralign=0;
    while(flag){ //there is some unaligned nodes in determined iteration
        //find the maximum value of each row of alignscore and save it in array "best"
        for(int c1=0; c1<network1.size; c1++)
        {       
            if(!alignNodes1[c1]){
                temp=MINSCORE;
                for(int c2=0; c2<=network2.size; c2++)
                    if(temp<alignScore[c1][c2] && !alignNodes2[c2]){
                        if(alignScore[c1][c2]==temp) {
                            temp1 = (network1.deg[c1]>network2.deg[c2]) ? network2.deg[c2]/network1.deg[c1]:network1.deg[c1]/network2.deg[c2];
                            temp2 = (network1.deg[c1]>network2.deg[best[c1]]) ? network2.deg[best[c1]]/network1.deg[c1]:network1.deg[c1]/network2.deg[best[c1]];
                            if(temp1 > temp2) {
                                best[c1]=c2;
                                temp = alignScore[c1][c2];
                            }
                        }
                        else {
                            best[c1]=c2;
                            temp = alignScore[c1][c2];
                        }
                    }
            }
        }

        //doing the alignment
        //find the maximum value of array "best" that means the best score in matrix "alignScore"
        temp=MINSCORE;
        flag=false;
        
        for(int c1=0; c1<network1.size; c1++)
            if(temp<alignScore[c1][best[c1]] && !alignNodes1[c1] && !alignNodes2[best[c1]]){ //=
                flag=true; //still there is node that is not aligned
                if(alignScore[c1][best[c1]]==temp) {
                    
                    if(network1.deg[c1] > network1.deg[maxNode]) {
                         maxNode = c1;
                        temp = alignScore[c1][best[c1]];
                    }
                }
                else {
                    temp = alignScore[c1][best[c1]];
                    maxNode = c1;
                }
            }
        if(flag){ //there is some node in first network that are not still aligned 
            
            alignment[maxNode]=best[maxNode]; //align two nodes;
       
            alignNodes1[maxNode]=true;
            alignNodes2[best[maxNode]]=true;
            //align degree one neighbors together
            for(int j=0; j<network1.deg[maxNode]; j++)
                for(int k=0; k<network2.deg[best[maxNode]]; k++)
                    if( !alignNodes1[network1.neighbor[maxNode][j]] && !alignNodes2[network2.neighbor[best[maxNode]][k]])
                    {
                        if(network1.deg[network1.neighbor[maxNode][j]]==1 && network2.deg[network2.neighbor[best[maxNode]][k]]==1)
                        {
                            alignment[network1.neighbor[maxNode][j]] = network2.neighbor[best[maxNode]][k];
                            
                            alignNodes1[network1.neighbor[maxNode][j]] = true;
                            alignNodes2[network2.neighbor[best[maxNode]][k]] = true;
                        }
                    }
           
            
            //update the align scores
            for(int c1=0; c1 <network1.deg[maxNode]; c1++)
                for(int c2=0; c2<network2.deg[best[maxNode]]; c2++)
                    alignScore[ network1.neighbor[maxNode][c1]][network2.neighbor[best[maxNode]][c2]]=alignScore[ network1.neighbor[maxNode][c1]][network2.neighbor[best[maxNode]][c2]]+(coeff/max); 
        }
        counter = counter + 1;
        if ( counter % 1000 == 0)
            cout << counter << endl;
    }//end flag
    
    //memory leak
    delete [] alignNodes1;
    delete [] alignNodes2;
    delete [] nodeScore1;
    delete [] nodeScore2;
    delete [] best;
    
    for(int j=0; j<network1.size; j++)
    {
        delete [] alignScore[j];
    } 
    delete [] alignScore;
    
    
    evaluate(); //calculate the measurment evaluations
}

//calculate the evaluation measurments EC (Edge Correctness), IC (Interaction Correctness), NC (Node Correctness), CCCV and CCCE (largest Common Connected subraph with recpect to Vertices and Edges)
void Alignment::evaluate(void)
{
	CCCV = getCCCV(); //calculate CCCV
	CCCE = getCCCE(); //calculate CCCE
	EC = getEC();     //calculate Edge Correctness
    S3 = getS3();      //calculate S3
}

//calculate CCCV
//return the number of vertices of largest common connected subgraph of the alignment
int Alignment::getCCCV(void)
{
    int *subGraph;
    int compNum = 1; //number of connected components
	int *q = new int[network1.size]; //nodes that are already processed 
	comp = new int[network1.size]; //dtermines the connected component each node belongs to.
    for(int i=0; i<network1.size; i++)
	{
		comp[i] = network1.size;
		q[i] = i;
	}
    
	int last = 0;
    
	//for each node of the network
    for(int i=0; i<network1.size; i++)
	{
		if(comp[i]==network1.size)
		{
			q[0] = i;
			comp[i] = compNum;
			compNum++;
			last = 1;
            //finds all connected nodes tho the node i that is not alredy in a connected component
			for(int k=0; k<last; k++)
				for(int j=0; j<network1.deg[q[k]]; j++)
                    //the node is not already processed
					if( comp[q[k]] < comp[network1.neighbor[q[k]][j]])
					{
                        if (alignment[q[k]] != -1)
                            for( int l=0; l < network2.deg[alignment[q[k]]]; l++ )
                                if(network2.neighbor[alignment[q[k]]][l] == alignment[network1.neighbor[q[k]][j]])
                                {
                                    comp[network1.neighbor[q[k]][j]] = comp[q[k]];
                                    q[last] = network1.neighbor[q[k]][j];
                                    last++;
                                }
					}
		}
	}
    
	subGraph = new int[compNum-1]; //array of connected components
	for(int i=0; i<compNum-1; i++)
		subGraph[i] = 0;
	for(int i=0; i<network1.size; i++)
		subGraph[comp[i]-1]++; //number of nodes in a definit connected component
    
	//find the component with maximum nodes
    maxComp = 0;
	for(int i=0; i<compNum-1; i++)
	{
		if(subGraph[maxComp] < subGraph[i])
			maxComp = i;
	}
    
    int temp = subGraph[maxComp];
    
    //memory leak
    delete [] subGraph;
    delete [] q;
    
	return temp;
}

//calculate the evaluation measurment CCCE
//return the number of edges of largest common connected subgraph of the alignment
int Alignment::getCCCE(void)
{
	int edgeComp = 0;
    ofstream CC;
    //for each node of first network
	for(int i=0; i<network1.size; i++)
	{
        //for each neighbor of node i
		for(int j=0; j<network1.deg[i]; j++)
            //for each neighbor l of a node in second network that is aligned with node i
			if (alignment[i] != -1)
                for( int l=0; l < network2.deg[alignment[i]]; l++ )
                    if(network2.neighbor[ alignment[i] ][l] == alignment[network1.neighbor[i][j]])
                        if( comp[i]-1 == maxComp){
                            edgeComp++;
                        }
	}
    
	return ( edgeComp / 2 );
}

//calculate the evaluation measurment EC
//returns the percent of edges that are mapped correctly in alignment 
float Alignment::getEC(void)
{
	int totalScore=0;
    
	//for each node i in first network
    for(int i=0; i<network1.size; i++)
	{
        //for each neighbor j of node i
        for(int j=0; j<network1.deg[i]; j++)
			//for each neighbor l of a node in second network that is aligned with node i
            if (alignment[i] != -1)
                for( int l=0; l < network2.deg[alignment[i]]; l++ ) {
                    if(network2.neighbor[ alignment[i] ][l] == alignment[ network1.neighbor[i][j] ]) {
                        totalScore++;
                    }
                }
	}
    
	//minimum number of edges of two networks
    int minEdge = ( network1.numOfEdge > network2.numOfEdge)? network2.numOfEdge : network1.numOfEdge;
    //calculate EC(edge correctness)
	return ( (float) totalScore ) / ( 2 * network1.numOfEdge );
}

float Alignment::getS3(void)
{
	int totalScore=0;
    int* alignnodes = new int[network1.size];
    int num_edge_net2=0;
    
	//for each node i in first network
    for(int i=0; i<network1.size; i++)
	{
        alignnodes[i]=alignment[i];
        //for each neighbor j of node i
        for(int j=0; j<network1.deg[i]; j++)
			//for each neighbor l of a node in second network that is aligned with node i
            if (alignment[i] != -1)
                for( int l=0; l < network2.deg[alignment[i]]; l++ ) {
                    if(network2.neighbor[ alignment[i] ][l] == alignment[ network1.neighbor[i][j] ]) {
                        totalScore++;
                    }
                }
	}
    totalScore=totalScore/2;
    
    for(int i=0; i<network1.size; i++)
        if (alignment[i] != -1)
            for(int j=0; j<network2.deg[alignnodes[i]]; j++)
                for(int l=0; l<network1.size; l++)
                    if(network2.neighbor[alignnodes[i]][j]==alignnodes[l])
                        num_edge_net2++;
    num_edge_net2=num_edge_net2/2;
	//minimum number of edges of two networks
    int minEdge = ( network1.numOfEdge > network2.numOfEdge)? network2.numOfEdge : network1.numOfEdge;
    //calculate EC(edge correctness)
	return ( (float) totalScore ) / ( minEdge + float(num_edge_net2) - totalScore );
}

//print the evaluation measurments in a file with input parameter name
//Input parameter name determines the file that result are to be written in.
void Alignment::outputEvaluation(string name)
{
	string outFile = name;
    //add a definit suffix to the file
	outFile.append(".eval");
	ofstream outputFile( outFile.c_str());
    
    //print in console
    
	outputFile << "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++" << endl;
	outputFile << "*** CONNECTED COMPONENTS SIZE : " << endl;
	outputFile << "Nodes = " << CCCV << endl;
	outputFile << "Edges = " << CCCE << endl;
    
	outputFile << "===============================================================" << endl;
	if(reverse)
	{
		outputFile << "G1:  Nodes : " << network2.size << "  - Edges : " << network2.numOfEdge << endl;
		outputFile << "G2:  Nodes : " << network1.size << "  - Edges : " << network1.numOfEdge << endl;
	}
	else
	{
		outputFile << "G1:  Nodes : " << network1.size << "  - Edges : " << network1.numOfEdge << endl;
		outputFile << "G2:  Nodes : " << network2.size << "  - Edges : " << network2.numOfEdge << endl;
	}
    
	outputFile << "EC : " << EC << endl;
	outputFile << "S3 : " << S3 << endl;
}

//print the alignment(mapping) in a file with input parameter name
//Input parameter name determines the file that mapping is to be written in.    
void Alignment::outputAlignment(string name)
{
	string alignFile = name;
    
	alignFile.append(".alignment");
    
    
	ofstream alignmentFile( alignFile.c_str());
	if(reverse)
		for(int i=0; i<network1.size; i++)
            alignmentFile << network1.getName( alignment[ i ] ) << ' ' << network2.getName( i )<< endl;
	else
		for(int i=0; i<network1.size; i++)
            alignmentFile << network1.getName( i ) << ' ' << network2.getName( alignment[ i ] )<< endl;
}
//instructor
Alignment::Alignment(void)
{
}
//destructor
Alignment::~Alignment(void)
{
}
