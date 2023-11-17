#include <bits/stdc++.h>
using namespace std;

int main(){
    
    vector<int> arr = {0,1,0,1,0};
    int k = 2,n=arr.size();
    int ans=0,pc;
    for (int i = 0; i < n;i++) {
        unordered_map<int,int> f;
        pc = 0;
        for (int j = i; j < n;j++){
            f[arr[j]]++;
            pc += (f[arr[j]]-1);
            // int val = f[arr[j]];
            
            if (pc >= k) {
                // cout<<"found "<<i<<":"<<j<<endl;
                ans++;
                // break;
            }
        }
    }

    cout << ans << endl;
}