//1795a
#include <bits/stdc++.h>
using namespace std;

vector<int> largestDivisibleSubset(vector<int>& nums) {
        int n = nums.size();
        unordered_map<int,vector<int>> mp;
        sort(nums.begin(),nums.end(),greater<int>());

        bool flag;
        for (int i=0;i<n;i++){
            flag = true;
            for (auto& x:mp){
                if (x.first%nums[i]==0){
                    flag = false;
                    x.second.push_back(nums[i]);
                    
                }
            }
            // cout<<"Flag "<<nums[i]<<' '<<flag<<'\n';
            if (flag){
                
                mp[nums[i]] = vector<int>();
                cout<<"After inserting to "<<nums[i]<<'\n';
            }
            cout<<"Iter"<<endl;
            for (auto x:mp)
                cout<<x.first<<' '<<x.second.size()<<'\n';
        }

        int ans = 0, key;
        for (auto x:mp){
            cout<<x.first<<' '<<x.second.size()<<'\n';
            if (x.second.size()>ans){
                ans = x.second.size();
                key = x.first;
            }
        }
        cout<<mp[2].size();
        return mp[key];
    }

bool is_divisor(int a, int b) {
    return b % a == 0;
}

int main(){
    int t,n;
    cin>>t;
    while (t--){
        cin>>n;
        vector<pair<int,int>> mins;
        vector<int> sec;
        int beauty = 0,e,m;
        for(int i=0; i<n; i++){
            cin>>m;
            priority_queue<int, vector<int>, greater<int>> ar;
            for (int j=0;j<m;j++){
                cin>>e;
                ar.push(e);
            }
            mins.push_back({ar.top(),i});
            beauty += ar.top();
            ar.pop();
            sec.push_back(ar.top());
        }
        sort(mins.begin(),mins.end());
        bool f = true;
        if (n>1){
            if (sec[mins[0].second] > mins[1].first && sec[mins[0].second] > sec[mins[1].second])
                beauty = beauty-mins[1].first+sec[mins[0].second];
            else
                beauty = beauty+sec[mins[1].second]-mins[1].first;

            for (int i=2; i<n; i++)
                beauty = beauty+sec[mins[i].second]-mins[i].first;
                
            
        }
        cout<<beauty<<endl;

    }
}