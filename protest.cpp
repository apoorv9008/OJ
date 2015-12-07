#include<bits/stdc++.h>
using namespace std;

#define ll long long int
#define N 100005
#define pb push_back
#define mp make_pair
#define INF (ll)(1e18)
#define inf 0x7fffffff
#define inff 100000
#define ff first
#define ss second
#define MOD 1000000007
#define fast cin.sync_with_stdio(0);cin.tie(0)
#define rep(i,N) for(int i=0;i<N;i++)
#define frep(i,a,b) for(int i=a;i<=b;i++)
#define pii pair<int,int>
#define vii vector<int>
#define fill(A,v) memset(A,v,sizeof(A))
#define setbits(x) __builtin_popcount(x)
#define print(A,j,k) for(int ii=j;ii<=k;ii++)cout<<A[ii]<<" ";cout<<"\n"
#define all(x) (x).begin(), (x).end()
#define gcd __gcd
#define SQRT 350
#define CASES int t;cin>>t;while(t--)

set< vii > S;
set< vii > :: iterator it;

int main() {
	srand(time(NULL));
	freopen("range_testcases.txt" , "r" , stdin);
	freopen("temp_labfile.txt","w",stdout);
	int a,b,c,d,e,f,t;
	int left_arr[100000];
	int right_arr[100000];
	//a=0,b=100,c=0,d=100,e=0,f=100;

	scanf("%d",&t); // number fo variables (dynamica)
	for(int i=0;i<t;i++) {
	scanf("%d",&left_arr[i]);
	scanf("%d",&right_arr[i]);
	}
	for (int j=0; j<t; j++){
		for(int i=0;i<5;i++) {
			
				for(int l=0; l<j; l++)
					cout << ((left_arr[l]+right_arr[l])/2) << " ";			
			
				if (i == 0)
					cout << left_arr[j] << " ";
				else if(i == 1)
					cout << left_arr[j] + 1 << " ";
				else if (i == 2)
					cout << ((left_arr[j]+right_arr[j])/2) << " ";
				else if (i == 3)
					cout << right_arr[j] - 1 << " ";
				else
					cout << right_arr[j] << " ";
				
				
				for(int k=j+1; k<t; k++)				
					cout << ((left_arr[k]+right_arr[k])/2) << " ";
		cout <<"\n";
		}
	}

	fclose(stdin);
	fclose(stdout);
	freopen("temp_labfile.txt","r",stdin);
	freopen("labfile.txt" , "w" , stdout);
	int x;
	for(int i=0;i<t*5;i++) {
		vii V;
			for(int k = 0;k < t;k++) {
				cin >> x;
				V.pb(x);
			}
			S.insert(V);
	}

	for(it = S.begin();it != S.end();it++) {
		for(int j = 0;j < (*it).size();j++)
			cout << (*it)[j] << " ";
		cout << "\n";
	}
	fclose(stdin);
	fclose(stdout);

return 0;
}
