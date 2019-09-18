#include<iostream>

using namespace std;

int main()
{
	double** d = new double* [5];
	for(int i = 0; i < 5; ++i)
	{
		d[i] = new double[5];
	}

	double** dd = d;
	dd[3][3] = 100;
	cout<<d[3][3]<<endl;

	for(int i = 0; i < 5; ++i)
	{
		delete[] d[i];
	}
	delete[] d;

	return 0;
}