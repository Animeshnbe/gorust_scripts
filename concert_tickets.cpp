#include <bits/stdc++.h>
using namespace std;
typedef long long ll;

signed main() {
    int n,m,t;
    cin>>n>>m;
    set<pair<int,int>> pr;
    vector<int> cust(m);
    for (int i=0;i<n;i++){
        cin>>t;
        pr.insert({-t,i});
    }
    // sort(pr.begin(),pr.end());

    for (int i=0;i<m;i++){
        cin>>t;
        auto it = pr.lower_bound({-t,-1});
        if (it == pr.end()) cout<<-1<<endl;
        else {
            cout<<-(it->first)<<endl;
            pr.erase(it);
        }
    }

    // ############### Different approach
    // sort(cust.begin(),cust.end(),[](pair<int,int>&a, pair<int,int>&b){
    //     if (a.first < b.first) return true;
    //     if (a.first == b.first && a.second>b.second) return true;
    //     return false;
    // });

    // vector<int> ans(m,-1);
    // int k = n;
    // for (int i=0;i<m;i++){
    //     auto it = upper_bound(pr.begin(),pr.end(),make_pair(cust[i],-1));
    //     cout<<(*(--it))<<endl;
    //     while (it!=pr.begin() && (*(--it)).second==0);

    //     if ((*it).second){
    //         ans[i] = (*it).first;
    //         pr[it-pr.begin()].second = 0;
    //         k--;
    //     }
    //     // pr.erase(it);
        
    //     if (k==0) break;
    // }

    // ############### Different question
    // int l = n-1;
    // for (int i=m-1;i>=0;i--){
    //     while (l>=0 && pr[l]>cust[i].first) l--;
    //     if (l>=0){
    //         ans[cust[i].second] = pr[l];
    //         l--;
    //     }
    //     else
    //         break;
    // }
    // for (int i:ans)
    //     cout<<i<<endl;

    return 0;
}