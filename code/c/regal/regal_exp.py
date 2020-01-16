import numpy as np
import argparse
import networkx as nx
import time
import os
import sys
try: import cPickle as pickle
except ImportError:
	import pickle
from scipy.sparse import csr_matrix

import xnetmf
from config import *
from alignments import *

def parse_args():
    parser = argparse.ArgumentParser(description="Run REGAL.")
    
    parser.add_argument('--nt', nargs='?', default='none', help="network type")
    
    parser.add_argument('--nl', nargs='?', default='none', help="network label")
    
    parser.add_argument('--attributes', nargs='?', default=None,
	                    help='File with saved numpy matrix of node attributes, or int of number of attributes to synthetically generate.  Default is 5 synthetic.')
                        
    parser.add_argument('--attrvals', type=int, default=2,
	                    help='Number of attribute values. Only used if synthetic attributes are generated')
                        
    parser.add_argument('--dimensions', type=int, default=128,
	                    help='Number of dimensions. Default is 128.')
                        
    parser.add_argument('--k', type=int, default=10,
	                    help='Controls of landmarks to sample. Default is 10.')

    parser.add_argument('--untillayer', type=int, default=2,
                        help='Calculation until the layer for xNetMF.')
    parser.add_argument('--alpha', type=float, default = 0.01, help = "Discount factor for further layers")
    parser.add_argument('--gammastruc', type=float, default = 1, help = "Weight on structural similarity")
    parser.add_argument('--gammaattr', type=float, default = 1, help = "Weight on attribute similarity")
    parser.add_argument('--numtop', type=int, default=0,help="Number of top similarities to compute with kd-tree.  If 0, computes all pairwise similarities.")
    parser.add_argument('--buckets', default=2, type=float, help="base of log for degree (node feature) binning")
    return parser.parse_args()

def main(args):
    network_type = args.nt
    network_label = args.nl

    # --------- noises --------- #
    vector_p = ["0", "0.01", "0.03", "0.05", "0.07", "0.09", "0.11", "0.13", "0.15", "0.17", "0.19", "0.21", "0.23", "0.25"]
    if network_type == "random_network":
        vector_p = vector_p[:-2] # random network only to 0.21
        print(vector_p)

    print("{} network".format(network_label))

    for p in vector_p:
        network_name = "datasets/self_under_noise/" + network_type + "/" + network_label + "/" + network_label + "_" + p + ".txt"
        emb_name = "emb/self_under_noise/" + network_type + "/" + network_label + "/" + network_label + "_" + p + ".emb"
        output_name = "output/self_under_noise/" + network_type + "/" + network_label + "/" + network_label + "_" + p + ".txt"

        #Load in attributes if desired (assumes they are numpy array)
        if args.attributes is not None:
            args.attributes = np.load(args.attributes, allow_pickle=True) #load vector of attributes in from file
            print args.attributes.shape

        #Learn embeddings and save to output
        print "learning representations..."
        before_rep = time.time()

        learn_representations(args, network_name, emb_name)
        after_rep = time.time()
        print("Learned representations in %f seconds" % (after_rep - before_rep))

        #Score alignments learned from embeddings (read in the embedding)
        embed = np.load(emb_name, allow_pickle=True)
        emb1, emb2 = get_embeddings(embed)
        before_align = time.time()
        if args.numtop == 0:
            args.numtop = None
        # Zirou's comment: compute the SIMILARITY MATRIX (NOT A PERMUTATION MATRIX) based on the embeddings.
        alignment_matrix = get_embedding_similarities(emb1, emb2, num_top = args.numtop) # This is our similarity matrix

        #Report scoring and timing
        after_align = time.time()
        total_time = after_align - before_align
        print("Align time: "), total_time

        score_alignment_matrix(alignment_matrix, topk = 1, out_name = output_name)

#Should take in a file with the input graph as edgelist (args.input)
#Should save representations to args.output
def learn_representations(args, network_name, emb_name):
	nx_graph = nx.read_edgelist(network_name, nodetype = int, comments="%")
	print "read in graph"
	adj = nx.adjacency_matrix(nx_graph)#.todense()
	print "got adj matrix"

	graph = Graph(adj, node_attributes = args.attributes)
	max_layer = args.untillayer
	if args.untillayer == 0:
		max_layer = None
	alpha = args.alpha
	num_buckets = args.buckets #BASE OF LOG FOR LOG SCALE
	if num_buckets == 1:
		num_buckets = None
	rep_method = RepMethod(max_layer = max_layer,
							alpha = alpha,
							k = args.k,
							num_buckets = num_buckets,
							normalize = True,
							gammastruc = args.gammastruc,
							gammaattr = args.gammaattr)
	if max_layer is None:
		max_layer = 1000
	print("Learning representations with max layer %d and alpha = %f" % (max_layer, alpha))
	representations = xnetmf.get_representations(graph, rep_method)
	pickle.dump(representations, open(emb_name, "w"))

# ======================================================== #
#         Redefine score_alignment_matrix function         #
# ======================================================== #
def score_alignment_matrix(alignment_matrix, topk = None, out_name = None, topk_score_weighted = False, true_alignments = None):
	n_nodes = alignment_matrix.shape[0] # size of the network (we assume two graphs are of same size)

	output_file = open(out_name, 'w')

	selected = [0] * n_nodes;

	if not sp.issparse(alignment_matrix):
		sorted_indices = np.argsort(alignment_matrix)

	for node_index in range(n_nodes):
		if sp.issparse(alignment_matrix):
			row, possible_alignments, possible_values = sp.find(alignment_matrix[node_index])
			node_sorted_indices = possible_alignments[possible_values.argsort()] # Sort in descending order!!!!

		else:
			node_sorted_indices = sorted_indices[node_index]

		for i2 in range(1, n_nodes+1):
			target = node_sorted_indices[-i2]
			if not selected[target]:
				output_file.write("{}\t{}\n".format(node_index, target))
				selected[target] = 1
				break
			if i2 == args.numtop:
				print("WARNING, node {} is unaligned".format(node_index))

	output_file.close()

if __name__ == "__main__":
	args = parse_args()
	main(args)
