//{ Driver Code Starts
#include <bits/stdc++.h>
using namespace std;
#define MAX 1000

class Solution{
    public:
    int findK(vector<int> l, vector<int> u, int mx)
    {
        vector<pair<int, int>> arr;
        int n = l.size();
        for(int i = 0; i < n; i++) {
            arr.push_back({l[i], u[i]});
        }
        sort(arr.begin(), arr.end());
        int ans = 0;

        int left = 0, right = INT_MAX;
        while(left <= right) {
            int mid = (left + right) / 2;
            int sum = 0;
            int cl = 0, cr = 0;
            vector<pair<int, int>> z;

            for(int i = 0; i < n; i++) {
                if(arr[i].second < mid) {
                    sum += arr[i].first;
                    cl++;
                }
                else if(arr[i].first > mid) {
                    sum += arr[i].first;
                    cr++;
                }
                else
                    z.push_back(arr[i]);
            }

            int lr = n / 2 - cl;
            int rr = n / 2 - cr;
            if(lr < 0) {
                right = mid - 1;
                continue;
            }
            else if(rr < 0) {
                left = mid + 1;
                continue;
            }

            for(int j = 0; j < lr; j++) {
                sum += z[j].first;
            }
            for(int j = 0; j < rr; j++) {
                sum += mid;
            }
            sum += mid;

            if(sum > mx) {
                right = mid - 1;
            }
            else {
                left = mid + 1;
                ans = mid;
            }
        }
 		return ans;
    }
};


int main(){
    int T=1;
    // cin>>T;
  
    // while(T--)
    // {
    //     int n,m;
    //     int k=0;
    //     //cin>>k;
    //     cin>>n>>m>>k;
    //     int a[MAX][MAX];
        
    //     for(int i=0;i<n;i++)
    //     {
    //         for(int j=0;j<m;j++)
    //         {
    //             cin>>a[i][j];
    //         }
    //     }
    //     Solution ob;
    //     cout<<ob.findK(a,n,m,k)<<endl;
        
       
    // }
    
        Solution ob;
        // vector<int> l = {1, 1, 3};
        // vector<int> u = {5, 3, 4};
        // int mx = 6;
        
        vector<int> l = {1, 3, 6};
        vector<int> u = {2, 5, 6};
        int mx = 12;
        cout<<ob.findK(l, u, mx)<<endl;
}
// } Driver Code Ends