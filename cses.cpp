#include <bits/stdc++.h>
using namespace std;
#define int long long
int mod=1e9+7,n;
// int dp[100001][1001];

int rec(int i, int s, vector<vector<int>>& proj, vector<vector<int>>& dp){ //return best score of P1 in l-r when P#turn starts
    if (i==n)
        return 0;
    
    if (s!=-1 && dp[i][s]!=-1)
        return dp[i][s];
    int ans = rec(i+1,s,proj,dp);
    if (proj[i][1]>s)
        ans = max(ans,proj[i][2]+rec(i+1,proj[i][0],proj,dp));

    return dp[i][s] = ans;
}
// 1,5+5,7 2,5+5,6 3,5+5,5 4,5+4,5
signed main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);
    cout.tie(0);
    cin>>n;
    int a,b,r;
    vector<vector<int>> proj(n);
    for (int i=0;i<n;i++){
        cin>>a>>b>>r;
        proj[i] = {b,a,r};
    }
    sort(proj.begin(),proj.end());

    vector<vector<int>> dp(n+1, vector<int> (proj[n-1][0],-1));

    cout<<rec(0,-1,proj,dp)<<endl;
    return 0;
}