#include <bits/stdc++.h>
 
using namespace std;
 
#define ll long long int
#define N (int)1e5 + 5
#define pb push_back
#define mp make_pair
#define INF (ll)(1e18)
#define inf 0x7fffffff
#define inff 100000
#define ff first
#define ss second
#define sz(x) ((int) (x).size())
#define MOD (int)(1e9+7)
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

int A[N];

int main(int argc, char const *argv[])
{

	freopen("input_at1.txt" , "w" , stdout);
	int n;
	//cin >> n;
	n = 100;
	cout << n << "\n";
	rep(i , n) {
		//cin >> A[i];
		A[i] = rand() % 100000000;
		cout << A[i] << "\n";
	}
	sort(A , A + n);
	fclose(stdout);
	freopen("output_at1.txt" , "w" , stdout);
	rep(i , n)
		cout << A[i] << "\n";
	fclose(stdout);

	return 0;
}