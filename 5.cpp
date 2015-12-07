#include<iostream> 
int main()
{
std::ios::sync_with_stdio(false);
	long int q,t,n;
   
	std::cin>>t;
	for(int i=0; i<t; i++)
	{
		std::cin>>n;
		q=0;
		while(n!=0)
		{
			n=n/5;
			q+=n;
		}
				std::cout<<q<<"\n";
	}
	return 0;
}