#include<bits/stdc++.h>

using namespace std;

int main() {
srand(time(NULL));
freopen("range_testcases.txt" , "r" , stdin);
freopen("labfile_random.txt","w",stdout);

int t;
cin >> t;

while(t--) {
	int l , r;
	cin >> l >> r;
	int a = l + rand() % (r - l + 1);
	cout << a << " ";
}

return 0;
}


