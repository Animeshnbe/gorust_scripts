#include <bits/stdc++.h>
using namespace std;

signed main(){
    int m,n;

    cin>>n>>m;
    vector<int> aller(m);
    for (int i=0;i<m;i++)
        cin>>aler[i];

    cin>>m;
    vector<int> pois(m);
    for (int i=0;i<m;i++)
        cin>>pois[i];

    unordered_map<int,int> mp;

    for (int i=0;i<m;i++){
        mp[pois[i]] = max(mp[pois[i]],aler[i]);

    }

    int ans = 0;
    for (int i=0;i<n;i++){

    } 
}
