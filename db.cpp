#include <vector>
#include <iostream>
#include <set>
using namespace std;

int rec(vector<pair<int,int>>& strips, int cuts){
    if (cuts==k) {
        int s=0;
        for (auto& p:strips)
            s += (p.first*p.second);
    }

    int ans = 0;
    for (auto it=strips.begin();it!=strips.end();it++){
        auto p = *it;
        it = strips.erase(it);
        for (int i=1;i<=p.first/2;i++) {
            strips.insert(it,{i,p.second});
            strips.insert(it,{p.first-i,p.second});
            ans = min(ans,rec(strips,cuts+1));
        }
    }
    
}
int main(){
    int t;
    cin>>t;
    vector<bool> ans(100,true);
    bool f = false;
    int n;
    for (int i=0;i<t;i++){
        int r;
        cin>>r;
        
        set<int> lines;
        for (int j=0;j<r;j++){
            cin>>n;
            lines.insert(n);
        }
        for (int j=0;j<100;j++){
            if (ans[j] && lines.find(j+1)==lines.end())
                ans[j] = false;
        }
    }

    for (int i=0;i<100;i++){
        if (ans[i]) cout<<i+1<<" ";
    }
}