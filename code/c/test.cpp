#include<iostream>
#include<vector>

using namespace std;

int main()
{
	// vector<int> v(1000000);

	// for(int i = 0; i < 50000; ++i)
	// {
	// 	v[i] = i;
	// }

	// v.resize(50000);

	//or
	
	vector<int> v;
	v.reserve(1000000);
	for(int i = 0; i < 50000; ++i)
	{
		v.push_back(i);
	}
	v.shrink_to_fit();

	return 0;
}