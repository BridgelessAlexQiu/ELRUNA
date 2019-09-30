// If matrices are not symmetric, something is not right
for(int i = 1; i <= g1_size; ++i)
{
    for(int j = 1; j <= g1_size; ++j)
    {
        if(C.get(i,j) != C.get(j, i))
        {
            cerr<<"The matrix C is not symmetric, something is not right"<<endl;
            return -1;
        }
    }
}
for(int u = 1; u <= g2_size; ++u)
{
    for(int v = 1; v <= g2_size; ++v)
    {
        if(D.get(u, v) != D.get(v, u))
        {
            cerr<<"The matrix D is not symmetric, something is not right"<<endl;
            return -1;
        }
    }
}



