#include <bits/stdc++.h>
using namespace std;

#define ll long long int
#define ld long double
#define pint pair<int,int>
#define vl vector<ll>
#define mp map<ll, ll>

#define MOD 1000000007
#define PI 3.1415926535897932384626433832795

#define ee cout<<"\n"
#define sall(v) sort(v.begin(), v.end())
#define time() cerr << "Time : " << (double)clock() / (double)CLOCKS_PER_SEC << "s\n"
#define fo(i, n) for (ll i = 0; i < n; i++)

vector<ll> Tree;
void make_Tree(vector<ll> &v) {
    ll i;
    ll n = v.size();
    while (n & (n - 1))
        n++;
    v.resize(n);
    Tree.resize(2 * n);

    for (i = 0; i < n; i++)
        Tree[n + i] = v[i];
    
    for (i = n - 1; i >= 1; i--)
        Tree[i] = Tree[2*i] + Tree[2*i + 1];
}
ll segment(ll node, ll node_left, ll node_right, ll query_left, ll query_right) {
    if (query_left <= node_left && node_right <= query_right)
        return Tree[node];
    
    if (query_right < node_left || node_right < query_left)
        return 0;
    
    ll last_left = (node_left + node_right) / 2;
    return segment(2 * node, node_left, last_left, query_left, query_right) + segment(2 * node + 1, last_left + 1, node_right, query_left, query_right);
}
void update_Tree(ll index, ll val) {
    // 1base indexing
    ll n = Tree.size() / 2;
    ll diff = val - Tree[n + index - 1];
    for (ll i = n + index - 1; i >= 1; i /= 2) {
        Tree[i] += diff;
    }
}

//ver 2
int getMid(int s, int e) { return s+(e-s)/2; }

int getMinUtil(int *st, int s, int e, int qs, int qe, int cur){

    if (qs <= s && qe >= e)
        return st[cur];

    if (e < qs || s > qe)
        return INT_MAX;

    int mid = getMid(s, e);
    return min(getMinUtil(st, s, mid, qs, qe, 2*cur+1),getMinUtil(st, mid+1, e, qs, qe, 2*cur+2));
}

int getMinST(int *st, int n, int qs, int qe){
    if (qs > qe){
        qs = qs+qe;
        qe = qs-qe;
        qs = qs-qe;
    }
    // qe--;
    if (qs < 0 || qe > n-1){
        // cout<<"Invalid Input";
        return -1;
    }

    return getMinUtil(st, 0, n-1, qs, qe, 0);
}

int constructSTUtil(vector<int>& arr, int ss, int se, int *st, int si){

    if (ss == se){
        st[si] = arr[ss];
        return arr[ss];
    }

    int mid = getMid(ss, se);
    st[si] = min(constructSTUtil(arr, ss, mid, st, si*2+1), constructSTUtil(arr, mid+1, se, st, si*2+2));
    return st[si];
}

int *constructST(vector<int>& arr, int n){
    int x = (int)(ceil(log2(n)));

    //Maximum size of segment tree
    int max_size = 2*(int)pow(2, x) - 1;

    int *st = new int[max_size];
    constructSTUtil(arr, 0, n-1, st, 0);
    return st;
}

class nSum{
    vector<vector<int>> sums;
    void generateSums(int l,int r,int k,int T,vector<int> &curr,vector<int> &nums){
        if(k == 2){
            while(l < r){
                int currSum = nums[l] + nums[r];
                if(currSum == T){
                    curr.push_back(nums[l++]);
                    curr.push_back(nums[r--]);
                    sums.push_back(curr);
                    curr.pop_back();
                    curr.pop_back();
                    while(l < r && nums[l] == nums[l-1]) l++;
                    while(l < r && nums[r] == nums[r+1]) r--;
                }
                else if(currSum < T) l++;
                else r--;
            }
            return;
        }
        
        while(l < r){
            curr.push_back(nums[l]);
            generateSums(l+1,r,k-1,T-nums[l],curr,nums);
            curr.pop_back();
            l++;
            while(l < r && nums[l] == nums[l-1]) l++; //remove duplicates
        }
    }
    
    public:
    vector<vector<int>> fourSum(vector<int> &nums, int target) {
        int k = 4;
        sort(nums.begin(),nums.end());
        vector<int> curr;
        generateSums(0,nums.size()-1,k,target,curr,nums);
        return sums;
    }
};

const ll maxN = 100001;
vector<ll> inF(maxN), F(maxN), isPrime(maxN), adj[maxN];
mp vis;
void dfs(ll node) {
    if (vis[node])
        return;
    vis[node] = 1;
    for (auto child : adj[node])
        dfs(child);

    return;
}

class DSU{
    public:
    vector<int> rank, par;
    DSU(int n){
        rank.resize(n,0);
        par.resize(n,-1);
    }
    int find(int x){
        if (par[x]==-1)
            return x;
        return par[x] = find(par[x]);
    }
    void unite(int x,int y){
        int px = find(x);
        int py = find(y);
        if (px!=py){
            if (rank[px]>rank[py])
                par[py] = px;
            else if (rank[py]>rank[px])
                par[px] = py;
            else {
                par[py] = px;
                rank[px]++;
            }
        }
    }
};

int KMP(string& s, string& pat){
    vector<int> lps(pat.size(),0);
    int i=1, len=0, m=pat.size(), n=s.size();
    while (i<m) {
        if (pat[i] == pat[len]) {
            len++;
            lps[i] = len;
            i++;
        } else {
            if (len != 0) 
                len = lps[len-1];
            else
                lps[i++] = 0;
        }
    }
    i=0;
    int j = 0;
    while ((n-i) >= (m-j)) {
        if (pat[j] == s[i]) {
            j++;
            i++;
        }

        if (j == m) {
            return i-j; // optional
            j = lps[j - 1]; // further matches
        }
        else if (i<n && pat[j] != s[i]) {
            if (j)
                j = lps[j-1];
            else
                i++;
        }
    }

    return -1;
}

const int ALPHABET_SIZE = 26;
struct TrieNode{
    struct TrieNode *children[ALPHABET_SIZE];
    bool isEndOfWord;
};
struct TrieNode *getNode(void){
    struct TrieNode *pNode =  new TrieNode;
    pNode->isEndOfWord = false;
    for (int i = 0; i < ALPHABET_SIZE; i++)
        pNode->children[i] = NULL;
 
    return pNode;
}
void insert(struct TrieNode *root, string key){
    struct TrieNode *pCrawl = root;
 
    for (int i = 0; i < key.length(); i++) {
        int index = key[i] - 'a';
        if (!pCrawl->children[index])
            pCrawl->children[index] = getNode();
 
        pCrawl = pCrawl->children[index];
    }
    pCrawl->isEndOfWord = true;
}
bool search(struct TrieNode *root, string key){
    struct TrieNode *pCrawl = root;
 
    for (int i = 0; i < key.length(); i++) {
        int index = key[i] - 'a';
        if (!pCrawl->children[index])
            return false;
 
        pCrawl = pCrawl->children[index];
    }
    return (pCrawl->isEndOfWord);
}
// struct TrieNode *troot = getNode();

ll pow1(ll n, ll k)
{
    if (k == 0)
        return 1;
    if (k == 1)
        return n;
    ll X = 1;
    if (k % 2 == 1)
        X = n % MOD;
    ll Y = pow1(n, k / 2) % MOD;
    return (((Y * Y) % MOD) * X) % MOD;
}
void fact_compute() {
    ll N = maxN - 1;
    F[0] = 1;
    F[1] = 1;
    for (ll i = 2; i <= N; i++)
    {
        F[i] = (F[i - 1] * (i)) % MOD;
    }
    inF[N] = pow1(F[N], MOD - 2) % MOD;
    for (ll i = N - 1; i >= 0; i--)
    {
        inF[i] = (inF[i + 1] * (i + 1)) % MOD;
    }
}
void sieve(){
    for (ll i = 2; i < maxN; i++)
        isPrime[i] = 1;
    
    for (ll i = 2; i < maxN; i++) {
        for (ll j = 2 * i; j < maxN; j += i) {
            isPrime[j] = 0;
        }
    }
}
int ncr(int n, int r){
    //pascal triangle
    vector<vector<int>> pre(n+1, vector<int>(n+1,0));
    for (int i=0;i<=n;i++){
        for (int j=0;j<=min(i,r);j++){
            if (j==0 || j==i)
                pre[i][j] = 1;
            else
                pre[i][j] = pre[i-1][j] + pre[i-1][j-1];
        }
    }
    return pre[n][r];
}

ll gcd(ll n, ll m)
{
    if (!m)
        return n;
    return gcd(m, n % m);
}

int partition(vector<int>& arr, int l, int r) { 
    int pivot = arr[r], i = l; 
    for (int j=l; j<r; j++) { 
        if (arr[j] <= pivot) { 
            swap(arr[i], arr[j]); 
            i++; 
        }
    } 
    swap(arr[r], arr[i]); 
    return i; 
} 

void set_io(string name = ""){
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);
    cout.tie(0);
    // if (size(name)) {
        // string filename = "out.txt";
        // string
        if (!freopen((name + ".txt").c_str(), "r", stdin)) cerr << "INPUT FAILED";
        if (!freopen((name + "out.txt").c_str(), "w", stdout)) cerr << "OUTPUT FAILED";
    // }
}

ll calc(ll M, ll rndNum, vl &v, vector<vector<ll> > &dp){
    ll n = v.size();
    if(rndNum==(n/2)+1)
    {
        return 0;
    }
    if(dp[rndNum][M]!=-1)
    return dp[rndNum][M];
    ll res = -1;
    for(ll i=0;i<n;i++)
    {
        for(ll j=i+1;j<n;j++)
        {
            if(((1<<i)&M)==0&&((1<<j)&M)==0)
            {
                ll tempRes = (rndNum)*(v[i]&v[j]);
                ll newM = ((M|(1<<i))|(1<<j));
                res = max(res,tempRes+calc(newM,rndNum+1,v,dp));
            }
        }
    }
    return dp[rndNum][M] = res;
}

int solve(int k,vector<int>& e){
    
}
string formatDouble(double number, int precision) {
    std::ostringstream oss;
    oss << std::fixed << std::setprecision(precision) << number;
    std::string formatted = oss.str();

    // Remove trailing zeroes
    size_t found = formatted.find_last_not_of('0');
    if (found != std::string::npos && found != formatted.size() - 1) {
        formatted.erase(found + 1);
    }

    return formatted;
}
signed main(){
    set_io("put");
    ll testCase;
    cin>>testCase;
    
    for (int i=0;i<testCase;i++){
        int n,l=2,h=n/2;
        cin>>n;
        vector<int> elf(n);
    
        for (int j=0;j<n;j++){
            cin>>elf[j];
            // l = min(l,elf[i]);
        }
        sort(elf.begin(),elf.end());
        double ans;
        if (n==5){
            double m1  = (elf[n-1]+elf[n-2])/2.0-(elf[0]+elf[2])/2.0;
            double m2 = (elf[n-1]+elf[n-3])/2.0-(elf[0]+elf[1])/2.0;
            ans = max(m1,m2);
        }
        else
            ans  = (elf[n-1]+elf[n-2])/2.0-(elf[0]+elf[1])/2.0;
        // while (l<h){
        //     int mid=(l+h)/2;
        //     solve(mid,elf)
        // }
        // solve();
        // string a = formatDouble(ans,6);
        // if (a.back()=='.')
        //     a.pop_back();
        cout<<"Case #"<<i+1<<": "<<ans<<endl;
    }
    return 0;
}