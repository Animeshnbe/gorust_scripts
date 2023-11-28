//{ Driver Code Starts
#include <bits/stdc++.h>
using namespace std;
#define MAX 1000

class Solution
{
    public:
    int findK(int a[MAX][MAX],int n,int m,int k)
    {
 		// Your code goes here.
 		int r=0,c=0;
 		int i=0,j=0;
 		while (k>0){
     		for (j=c;j<m-c && k--;j++) ;
     		for (i=r+1;i<n-r && k--;i++) ;
     		for (j=m-c-2;j>=c && k--;j--) ;
     		c++;
     		for (i=n-r-2;i>r && k--;i--) ;
     		r++;
 		}
        cout<<i<<"L"<<j<<endl;
 		return a[i][j];
    }
};


int main(){
    int T=1;
    // cin>>T;
  
    while(T--)
    {
        int n,m;
        int k=0;
        //cin>>k;
        cin>>n>>m>>k;
        int a[MAX][MAX];
        
        for(int i=0;i<n;i++)
        {
            for(int j=0;j<m;j++)
            {
                cin>>a[i][j];
            }
        }
        Solution ob;
        cout<<ob.findK(a,n,m,k)<<endl;
        
       
    }
}
// } Driver Code Ends