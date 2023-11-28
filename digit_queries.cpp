#include <bits/stdc++.h>
using namespace std;
typedef long long ll;

ll pow2(ll n, ll k){
    if (k == 0)
        return 1;
    if (k == 1)
        return n;
    
    ll Y = pow2(n, k / 2);
    ll X = 1;
    if (k & 1)
        X = n;
    
    return (Y * Y * X);
}

signed main(){
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);
    cout.tie(0);

    int q;
    cin>>q;
    ll k;
    while (q--){
        cin>>k;
        
        int j = 0,y;
        ll x;
        while (true){
            x = (9*pow2(10,j++))*j;
            if (k>x)
                k -= x;
            else{
                // cout<<x<<":"<<k<<endl;
                break;
            }
        }
        k--;
        x = pow2(10,j-1) + (k/ll(j));
        y = k%j;
        cout<<to_string(x)[y]<<endl;

        // if (y) {
        //     cout<<to_string(x)[y-1]<<endl;
        // } else {
        //     x--;
        //     cout<<(x%10)<<endl;
        // }

        // string x = "";
        // int j = 1;
        // while (x.size()<k){
        //     x += to_string(j++);
        // }
        // cout<<x[k-1]<<endl;
    }
}