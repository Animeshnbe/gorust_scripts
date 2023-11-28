#include <bits/stdc++.h>
using namespace std;
typedef long long ll;

int MOD=1e9+7;

int pow1(ll n, ll k){
    if (k == 0)
        return 1;
    if (k == 1)
        return n;
    ll X = 1;
    if (k % 2)
        X = n % MOD;
    ll Y = pow1(n, k / 2) % MOD;
    return int((((Y * Y) % MOD) * X) % MOD);
}

ll pow2(ll n, ll k){
    if (k == 0)
        return 1;
    if (k == 1)
        return n;
    
    ll Y = pow1(n, k / 2);
    ll X = 1;
    if (k & 1)
        X = n;
    
    return (Y * Y * X);
}

// set<string> rec(int n, string& s){
//     if (n==1) return {s};

//     set<string> perm;
//     if (n==2) {
//         string nex{s[1],s[0]};
//         // cout<<nex<<endl;
//         perm.insert(s);
//         perm.insert(nex);
//         return perm;
//     }

//     // cout<<"Moe "<<s<<endl;
    
//     string q = s.substr(1);
//     set<string> ans = rec(n-1,q);
//     char c, st = s[0];
    
//     for (string p:ans){
//         c = '#';
//         for (int i=0;i<n;i++){
//             if (i>0 && p[i-1] == st) continue;
//             string nex = p.substr(0,i);
//             nex.push_back(st);
//             if (i<n-1)
//                 nex += p.substr(i);
//             perm.insert(nex);
//         }
//     }

//     return perm;
// }

// bool valid(vector<int>& c, int r, int c1){
//     if (c.empty()) return true;
//     for (int i=0;i<r;i++){
//         if (c[i]==c1 || abs(r-i)==abs(c[i]-c1)) return false;
//     }
//     return true;
// }

map<char,vector<int>> d = {{'D',{0,1}},{'U',{0,-1}},{'L',{-1,0}},{'R',{1,0}}};
int rec(string& s, int x, int y, int cur, vector<vector<bool>>& vis){
    
    // if (vis[x][y]) {
    //     // cout<<"Bad cell "<<x<<":"<<y<<endl;
    //     return 0;
    // }
    if (x==0 && y==6) return int(cur==48);

    vis[x][y] = true;
    int nx, ny, ans=0;
    if (s[cur]=='?'){
        for (auto it:d){
            nx = x + it.second[0];
            ny = y + it.second[1];
            if (nx<0 || nx>=7 || ny<0 || ny>=7 || vis[nx][ny]) 
                continue;

            // if (y==0)
                // cout<<"At "<<x<<":"<<y<<", Going to "<<nx<<":"<<ny<<endl;
            ans += rec(s,nx,ny,cur+1,vis);
        }
    } else {
        nx = x + d[s[cur]][0];
        ny = y + d[s[cur]][1];
        if (nx>=0 && nx<7 && ny>=0 && ny<7 && !vis[nx][ny]) {
            ans = rec(s,nx,ny,cur+1,vis);
        }
    }
    vis[x][y] = false;
    return ans;
}

signed main(){
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);
    cout.tie(0);
    
    int n=7;
    string s;
    vector<vector<bool>> vis(7, vector<bool> (7,false));
    cin>>s;
    // vis[0][0] = true;
    cout<<rec(s,0,0,0,vis)<<endl;
}