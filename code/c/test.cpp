#include<iostream>
#include<vector>
#include<string>
#include<map>
#include<sstream>

using namespace std;

int main()
{
	multimap<double, string, greater <double> > M;
	M.insert(multimap<double, string>::value_type(0.27829, "ad")); 
	M.insert(multimap<double, string>::value_type(0.67829, "ae"));
	M.insert(multimap<double, string>::value_type(0.17829, "ab"));
	M.insert(multimap<double, string>::value_type(0.97829, "af"));
	M.insert(multimap<double, string>::value_type(1.1829, "af"));

	multimap<double, string>::iterator it;
	int index = 1;
	for(it = M.begin(); it != M.end(); )
	{
		if(index == 3)
		{
			M.erase(it++);
		}
		else
		{
			cout<<it->first<<endl;
			it++;
		}
		index++;	
	}

	// int i = 10;
	// int d = 20;
	// string str = std::to_string(i) + " " + std::to_string(d);

	// string a = "10";
	// string b = "20";
	// cout<<stoi(a)<<" "<<stoi(b)<<endl;

	// string pair = "12 13";
	// istringstream iss(pair);
	// int a, b;
	// iss>>a>>b;
	// cout<<a<<" "<<b<<endl;

	return 0;
}
