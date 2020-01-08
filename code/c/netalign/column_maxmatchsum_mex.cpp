#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#include "mex.h"

#if MX_API_VER < 0x07030000
typedef int mwIndex;
typedef int mwSize;
#endif // MX_API_VER

/*
 * compile with 
 * mex -O column_maxmatchsum_mex.cpp
 */ 

/**
 * n the number of nodes
 * m the number of nodes
 * nedges the number of edges
 * v1 is the source for each of the nedges 
 * v2 is the target for each of the nedges
 * weight is the weight of each of the nedges
 * mi is a vector saying which of v1 and v2 are used, length >= nedges
 */
double intmatch(int n, int m, 
        int nedges, int *v1, int *v2, double *weight, 
        int *mi)
{
    double ret, al;
	double *l1, *l2, *w;
	int *match1, *match2;
	int i, j, k, p, q, r, t1, t2;
	int *s, *t, *deg, *offset, *list, *index;

	l1 = new double[n];
	l2 = new double[n+m];
	s = new int[n+m];
	t = new int[n+m];
	offset = new int[n];
	deg = new int[n];
	list = new int[nedges + n];
    index = (int*)mxMalloc(sizeof(int)*(nedges+n));
	w = new double[nedges + n];
    match1 = new int[n];
	match2 = new int[n+m];
    
    // track modifications to t
    int *tmod, ntmod=0;
    tmod = new int[n+m];
    

	for (i = 0; i < n; i++) {
		offset[i] = 0;
		deg[i] = 1;
	}
	for (i = 0; i < nedges; i++) deg[v1[i]]++;
	for (i = 1; i < n; i++) offset[i] = offset[i-1] + deg[i-1];
	for (i = 0; i < n; i++) deg[i] = 0;
	for (i = 0; i < nedges; i++) {
		list[offset[v1[i]] + deg[v1[i]]] = v2[i];
		w[offset[v1[i]] + deg[v1[i]]] = weight[i];
        index[offset[v1[i]] + deg[v1[i]]] = i;
		deg[v1[i]]++;
	}
	for (i = 0; i < n; i++) {
		list[offset[i] + deg[i]] = m + i;
		w[offset[i] + deg[i]] = 0;
        index[offset[i] + deg[i]] = -1;
		deg[i]++;
	}
	for (i = 0; i < n; i++) {
		l1[i] = 0;
		for (j = 0; j < deg[i]; j++) {
			if (w[offset[i]+j] > l1[i]) l1[i] = w[offset[i] + j];
		}
	}
    // initialize the primal match
	for (i = 0; i < n; i++) {
		match1[i] = -1;
	}
    // initialize the dual variables l2
	for (i = 0; i < n + m; i++) {
		l2[i] = 0;
		match2[i] = -1;
	}
    // initialize t once
    for (j=0; j < n+m; j++) {
        t[j] = -1;
    }
    
	for (i = 0; i < n; i++) {
        for (j=0; j<ntmod; j++) {
            t[tmod[j]] = -1;
        }
        ntmod = 0;
        
        // clear the queue and add i to the head
		s[p = q = 0] = i;
		for(; p <= q; p++) {
			if (match1[i] >= 0) break;
			k = s[p];
			for (r = 0; r < deg[k]; r++) {
				j = list[offset[k] + r];
				if (w[offset[k] + r] < l1[k] + l2[j] - 1e-8) continue;
				if (t[j] < 0) {
					s[++q] = match2[j];
					t[j] = k;
                    tmod[ntmod]=j; // save our modification to t
                    ntmod++;
					if (match2[j] < 0) {
						for(; j>=0 ;) {
							k = match2[j] = t[j];
                            // reusing p here is okay because we'll
                            // stop below
                            p = match1[k];
                            match1[k] = j;
                            j = p;
						}
                        break; // we found an alternating path and updated
					}
				}
			}
		}
		if (match1[i] < 0) {
			al = 1e20;
			for (j = 0; j < p; j++) {
				t1 = s[j];
				for (k = 0; k < deg[t1]; k++) {
					t2 = list[offset[t1] + k];
					if (t[t2] < 0 && l1[t1] + l2[t2] - w[offset[t1] + k] < al) {
						al = l1[t1] + l2[t2] - w[offset[t1] + k];
					}
				}
			}
			for (j = 0; j < p; j++) l1[s[j]] -= al;
			//for (j = 0; j < n + m; j++) if (t[j] >= 0) l2[j] += al;
            for (j=0; j<ntmod; j++) { l2[tmod[j]] += al; }
			i--;
			continue;
		}
	}
    
	ret = 0;
	for (i = 0; i < n; i++) {
		for (j = 0; j < deg[i]; j++) {
			if (list[offset[i] + j] == match1[i]) {
				ret += w[offset[i] + j];
			}
		}
	}        
    
    // build the matching indicator 
    for (i=0; i<nedges; i++) {
        mi[i] = 0;
    }
    for (i=0; i<n; i++) {
        if (match1[i] < m) {
            for (j = 0; j < deg[i]; j++) {
                if (list[offset[i] + j] == match1[i]) {
                    mi[index[offset[i]+j]] = 1;
                }
            }
        }
    }
    
    mxFree(index);
    
    delete[] l1;
    // fails after here
    delete[] l2;
    // fails after here
    delete[] s;
    // fails before here
    delete[] t;
    delete[] offset;
    delete[] deg;
    // fails before here
    delete[] list;
    delete[] w;
    delete[] match1;
    delete[] match2;
    delete[] tmod;
    
	return ret;
}


/**
 * M : rows of Q
 * N : columns of Q
 * Qp : column pointers for Q (Q is compressed column); length >= N+1
 * Qr : row indices for Q; length >= Qp[N]
 * Qv : values for Q; length >= Qp[N]
 * m : rows of bipartite L
 * n : columns of bipartite L
 * nedges : number of edges in L (nedges < M)
 * li : first index of edges in L; length >= nedges
 * lj : second index of edges in L; length >= nedges
 * q [out] : output variable for the biggest maximum match sum of a column of Q;
 *      length >= N
 * mi [out] : the first index of selected edges in Q; length >= Qp[N]
 * mj [out] : the second index of selected edges in Q; length >= Qp[N]
 * outmedges [out] : the number of edges in mi and mj used
 */
void column_maxmatchsum(int M, int N, mwIndex *Qp, mwIndex *Qr, double *Qv,
        int m, int n, int nedges, double *li, double *lj,
        double *q, double *mi, double *mj, int *outmedges)
{
    int medges=0; // count the number of edges in the output m
    
    // convert li and lj to integers
    int *ili, *ilj;
    
    ili = (int*)mxMalloc(sizeof(int)*nedges);
    ilj = (int*)mxMalloc(sizeof(int)*nedges);
    
    for (int i=0; i<nedges; i++) {
        ili[i] = ((int)li[i]) - 1;
        ilj[i] = ((int)lj[i]) - 1;
    }
    
    // allocate memory for the big to small vertex maps
    int *lwork1, *lind1, *lwork2, *lind2;
    lwork1 = (int*)mxMalloc(sizeof(int)*m);
    lind1 = (int*)mxMalloc(sizeof(int)*m);
    lwork2 = (int*)mxMalloc(sizeof(int)*n);
    lind2 = (int*)mxMalloc(sizeof(int)*n);
    
    // allocate memory for the edges of the small matching in each column
    int *se1, *se2, *sqi, *sqj, *smi;
    double *sw;
    int max_col_nonzeros = 0;
    for (int j=0; j<N; j++) {
        int col_nonzeros = (int)(Qp[j+1]-Qp[j]);
        if (col_nonzeros >= max_col_nonzeros) {
            max_col_nonzeros = col_nonzeros;
        }
    }
    se1 = (int*)mxMalloc(sizeof(int)*max_col_nonzeros);
    se2 = (int*)mxMalloc(sizeof(int)*max_col_nonzeros);
    sw = (double*)mxMalloc(sizeof(double)*max_col_nonzeros);
    sqi = (int*)mxMalloc(sizeof(int)*max_col_nonzeros);
    sqj = (int*)mxMalloc(sizeof(int)*max_col_nonzeros);
    smi = (int*)mxMalloc(sizeof(int)*max_col_nonzeros);
    
    for (int i=0; i<m; i++) {
        lind1[i] = -1;
    }
    for (int i=0; i<n; i++) {
        lind2[i] = -1;
    }
    for (int j=0; j<N; j++) {
        // for each column in Q, we form the maximum possible
        // sum of all the elements, subject to the constraint that 
        // it's a valid matching in the elements from ili, ilj
        int smalledges = 0;
        int nsmall1 = 0; // number of vertices on side 1 of column matching
        int nsmall2 = 0; // number of vertices on side 2 of column matching
        for (mwIndex nzi=Qp[j]; nzi<Qp[j+1]; nzi++) {
            int i = (int)Qr[nzi];
            int v1 = ili[i];
            int v2 = ilj[i];
            int sv1=-1, sv2=-1;
            if (lind1[v1] < 0) {
                // add it to the map
                sv1 = nsmall1;
                lind1[v1] = sv1;
                lwork1[sv1] = v1;
                nsmall1++;
            } else {
                sv1 = lind1[v1];
            }
            if (lind2[v2] < 0) {
                // add it to the map
                sv2 = nsmall2;
                lind2[v2] = sv2;
                lwork2[sv2] = v2;
                nsmall2++;
            } else {
                sv2 = lind2[v2];
            }
            
            se1[smalledges] = sv1;
            se2[smalledges] = sv2;
            sw[smalledges] = Qv[nzi];
            sqi[smalledges] = i;
            sqj[smalledges] = j;
            smalledges++;
        }
        
        if (smalledges == 0) {
            q[j] = 0.;
            continue;
        }
        
        q[j] = intmatch(nsmall1, nsmall2,
                    smalledges, se1, se2, sw, 
                    smi);
        
        
        // add the selected edges to mi, mj
        for (int k=0; k<smalledges; k++) {
            if (smi[k] > 0) {
                mi[medges] = (double)(sqi[k]+1);
                mj[medges] = (double)(sqj[k]+1);
                medges++;
            }
        }
                    
        // reset the maps from big to small
        for (int k=0; k<nsmall1; k++) {
            lind1[lwork1[k]] = -1;
        }
        for (int k=0; k<nsmall2; k++) {
            lind2[lwork2[k]] = -1;
        }
    }
    if (outmedges) {
        *outmedges = medges;
    }
}

void mexFunction(int nlhs, mxArray *plhs[],
                 int nrhs, const mxArray *prhs[])
{
    int M, N, m, n; // the dimensions of Q, size of A and size of B
    double *li, *lj;
    
    int nedges = 0;
    
    int curarg = 0;
    
    M = (int)mxGetM(prhs[curarg]); // number of rows
    N = (int)mxGetN(prhs[curarg]); // number of columns
    mwIndex *Qp = mxGetJc(prhs[curarg]); // column pointer
    mwIndex *Qr = mxGetIr(prhs[curarg]); // row indices
    double *Qv = mxGetPr(prhs[curarg]); // values
    curarg++;
    
    nedges = mxGetNumberOfElements(prhs[curarg]);
    li = mxGetPr(prhs[curarg++]);
    lj = mxGetPr(prhs[curarg++]);
    m = (int)mxGetScalar(prhs[curarg++]);
    n = (int)mxGetScalar(prhs[curarg++]);
    
    int minnm = n;
    if (m < minnm) minnm = m;
    
    plhs[0] = mxCreateDoubleMatrix(1,N,mxREAL);    
    plhs[1] = mxCreateDoubleMatrix(Qp[N],1,mxREAL);
    plhs[2] = mxCreateDoubleMatrix(Qp[N],1,mxREAL);
    plhs[3] = mxCreateDoubleMatrix(1,1,mxREAL);
    
    
    // assert(nedges == M)
    
    double *q = mxGetPr(plhs[0]);
    
    int medges = 0;
    double *mi = mxGetPr(plhs[1]);
    double *mj = mxGetPr(plhs[2]);
    
    column_maxmatchsum(M, N, Qp, Qr, Qv,
            m, n, nedges, li, lj,
            q, mi, mj, &medges);
    
    (*mxGetPr(plhs[3])) = (double)medges; // number of edges used in mi, mj
    
}
  

