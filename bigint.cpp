#include <iostream>
#include <stack>
#include <string>
#include <algorithm>
using namespace std;

string rem_zeros(string n, bool bin=false){
    int ctr1=0;
    while(ctr1<n.length() && n[ctr1]=='0'){
        ctr1++;
    }
    if (ctr1==n.length()){
        return (bin)?"":"0";
    }
    string n1=n.substr(ctr1,n.length()-ctr1);
    return n1;
}

string add(string n1, string n2){
    string res="";
    if (n2=="0")
        return n1;
    if (n1=="0")
        return n2;
    short onedig=0,carry=0;
    long int ctr1=n1.length()-1,ctr2=n2.length()-1;
    while(ctr1>=0 || ctr2>=0){
        if (ctr1<0){
            if (carry>0){
                onedig = (int)(n2[ctr2]-'0')+carry;
                carry = onedig/10;
                onedig%=10;
                res=to_string(onedig)+res;
            } else
                res=n2[ctr2]+res;
            ctr2--;
        } else if (ctr2<0){
            if (carry>0){
                onedig = (int)(n1[ctr1]-'0')+carry;
                carry = onedig/10;
                onedig%=10;
                res=to_string(onedig)+res;
            } else
                res=n1[ctr1]+res;
            ctr1--;
        } else {
            onedig = (int)(n1[ctr1]-'0')+(int)(n2[ctr2]-'0')+carry;
            carry = onedig/10;
            onedig%=10;
            res=to_string(onedig)+res;
            ctr1--;
            ctr2--;
        }
    }
    if (carry>0)
        res=to_string(carry)+res;
    return rem_zeros(res);
}

bool compare(string n1,string n2){
    n1=rem_zeros(n1);
    n2=rem_zeros(n2);
    if (n1.length()>n2.length())
        return true;
    if (n1.length()==n2.length()){
        for (int i=0;i<n1.length();i++){
            if (n1[i]>n2[i])
                return true;
            if (n1[i]<n2[i])
                return false;
        }
    }
    return false;
}

string subtract(string n1, string n2){
    string temp="";
    if (compare(n2,n1)){
        temp=n1;
        n1=n2;
        n2=temp;
    }
    string res="";
    short onedig=0,borrow=0,subtractee;
    long int ctr1=n1.length()-1,ctr2=n2.length()-1;
    while(ctr1>=0){
        if (ctr2<0){
            if (borrow>0){
                if ((int)(n1[ctr1]-'0')>0){
                    onedig = (int)(n1[ctr1]-'1');
                    borrow = 0;
                } else
                    onedig = 9;
                res=to_string(onedig)+res;
            } else{
                res=n1.substr(0,ctr1+1)+res;
                break;
            }
            ctr1--;
        } else {
            subtractee = ((int)(n2[ctr2]-'0')+borrow);
            if ((int)(n1[ctr1]-'0')<subtractee){
                onedig = 10+((int)(n1[ctr1]-'0'))-subtractee;
                borrow = 1;
            } else {
                onedig = (int)(n1[ctr1]-'0')-subtractee;
                borrow = 0;
            }
            res=to_string(onedig)+res;
            ctr1--;
            ctr2--;
        }
    }
    if (temp=="")
        return rem_zeros(res);
    else
        return "-"+rem_zeros(res);
}

string mult(string n1, string n2){
    short onedig,carry=0;
    long int pos=n2.length()-1;
    string res,multres="0",zeros="";
    while (pos>=0){
        res="";
        for (int i=n1.length()-1;i>=0;i--){
            onedig = (int)(n1[i]-'0')*(int)(n2[pos]-'0')+carry;
            carry = onedig/10;
            res = to_string(onedig%10)+res;
        }
        if (carry>0){
            res = to_string(carry)+res;
            carry=0;
        }
        multres=add(multres,res+zeros);
        pos--;
        zeros+="0";
    }
    return rem_zeros(multres);
}

string fact(string n){
    n=rem_zeros(n);
    if (n=="0")
        return "1";
    if (n=="2" || n=="1")
        return n;
    // cout<<"Hello"<<endl;
    string fn = fact(subtract(n,"1"));
    // cout<<fn<<endl;
    return mult(n,fn);
}

string bytwo(string n){
    n=rem_zeros(n);
    string q="";
    short carry=0,div;
    for (int i=0;i<n.length();i++){
        if (carry)
            div = (10+(n[i]-'0'));
        else
            div = (n[i]-'0');
        q+=to_string(div/2);
        carry=div%2;
    }

    // return rem_zeros(q);
    
}

string binaryd(string n){
    n=rem_zeros(n);
    if (n=="0") return "0";
    string ans = "";

    while (!n.empty()){
        
        string q="";
        short carry=0,div;
        for (int i=0;i<n.length();i++){
            if (carry)
                div = (10+(n[i]-'0'));
            else
                div = (n[i]-'0');
            q.push_back('0'+(div>>1));
            carry=div%2;
        }

        
        n = rem_zeros(q,true);
        // cout<<n<<endl;
        if (carry)
            ans.push_back('1');
        else
            ans.push_back('0');
        // cout<<ans<<endl;
    }

    reverse(ans.begin(),ans.end());
    return ans;
}

string binaryd(string n){
    n=rem_zeros(n);
    if (n=="0") return "0";
    string ans = "";
        
    while (!n.empty()){
        
        string q="";
        short carry=0,div;
        for (int i=0;i<n.length();i++){
            if (carry)
                div = (10+(n[i]-'0'));
            else
                div = (n[i]-'0');
            q.push_back('0'+(div>>1));
            carry=div%2;
        }

        
        n = rem_zeros(q,true);
        // cout<<n<<endl;
        if (carry)
            ans.push_back('1');
        else
            ans.push_back('0');
        // cout<<ans<<endl;
    }

    reverse(ans.begin(),ans.end());
    return ans;
}

string expo(string b, string e){
    if (rem_zeros(e)=="0")
        return "1";
    int n = e.length();
    if (e[n-1]=='0' || e[n-1]=='2' || e[n-1]=='4' || e[n-1]=='6' || e[n-1]=='8') {
        string half_e = expo(b,bytwo(e));

        return mult(half_e,half_e);
    } else {
        return mult(b,expo(b,subtract(e,"1")));
    }
}

string gcd(string mx, string mn){
    if (mx==mn)
        return mn;
    if (mn=="1")
        return "1";
    string smaller=mn;
    bool expo_backoff=true;
    while (expo_backoff){
        expo_backoff=false;
        while (compare(mx,mn)){
            mx=subtract(mx,mn);
            mn=mult(mn,"2");
            expo_backoff=true;
        }
        // cout<<mn<<" : "<<mx<<endl;
        // cout<<"backoff start"<<endl;
        if (mx=="0" || (expo_backoff==false && mx==mn))
            return smaller;
        mn=smaller;
    }
    // while (compare(mx,mn)){
    //     mx=subtract(mx,mn);
    //     // cout<<mx<<" ";
    // }
    // cout<<endl;
    // if (mx==mn)
    //     return mn;
    
    // cout<<"stack end "<<mx<<":"<<mn<<endl;
    return gcd(mn,mx);
}

string apply_op(char op,string n1,string n2){
    if (op=='+'){
        if (n1[0]=='-')
            return subtract(n2,n1.substr(1,n1.length()));
        else
            return add(n1,n2);
        //n2 will never be -ve
    }
    if (op=='-'){
        if (n1[0]=='-')
            return "-"+add(n1.substr(1,n1.length()),n2);
        else
            return subtract(n1,n2);
    }
    return mult(n1,n2);
}

int main(){
    string n;
    cin>>n;
    cout<<binaryd(n)<<endl;
    // string inp;
    // short typ;
    // cin>>typ;
    // cin>>inp;
    // switch(typ){
    //     case 1:{
    //         // cout<<subtract("987654321","123456789")<<endl;
    //         string n1,n2,n3,n4;
    //         string stk="";
    //         short j=0;
    //         char op;
    //         for (long int i=0;i<inp.length();i++){
    //             if (inp[i]=='+'){
    //                 while(j>0){
    //                     if (j==1){
    //                         n1 = apply_op(stk[stk.length()-1],n1,n2);
    //                         n2 = "";
    //                     } else if (j==2) {
    //                         n2 = apply_op(stk[stk.length()-1],n2,n3);
    //                         n3 = "";
    //                     } else if (j==3) {
    //                         n3 = apply_op(stk[stk.length()-1],n3,n4);
    //                         n4 = "";
    //                     }
    //                     stk = stk.substr(0,stk.length()-1);
    //                     j--;
    //                 }
    //                 stk+='+';
    //                 j=(j+1)%4;
    //             } else if(inp[i]=='-'){
    //                 while(j>0){
    //                     if (j==1){
    //                         n1 = apply_op(stk[stk.length()-1],n1,n2);
    //                         n2 = "";
    //                     }
    //                     else if (j==2){
    //                         n2 = apply_op(stk[stk.length()-1],n2,n3);
    //                         n3 = "";
    //                     }
    //                     else if (j==3){
    //                         n3 = apply_op(stk[stk.length()-1],n3,n4);
    //                         n4 = "";
    //                     }
    //                     stk = stk.substr(0,stk.length()-1);
    //                     j--;
    //                 }
    //                 stk+='-';
    //                 j=(j+1)%4;
    //             } else if(inp[i]=='x'){
    //                 while (j>0 && stk[stk.length()-1]=='x'){
    //                     if (j==1){
    //                         n1 = mult(n1,n2);
    //                         n2 = "";
    //                     }
    //                     else if (j==2){
    //                         n2 = mult(n2,n3);
    //                         n3 = "";
    //                     }
    //                     else if (j==3){
    //                         n3 = mult(n3,n4);
    //                         n4 = "";
    //                     }
    //                     stk = stk.substr(0,stk.length()-1);
    //                     j--;
    //                 }
    //                 stk+='x';
    //                 j=(j+1)%4;
    //             } else {
    //                 if (j==0)
    //                     n1+=inp[i];
    //                 else if (j==1)
    //                     n2+=inp[i];
    //                 else if (j==2)
    //                     n3+=inp[i];
    //                 else
    //                     n4+=inp[i];
    //             }
    //         }
    //         while(j>0){
    //             if (j==1){
    //                 n1 = apply_op(stk[stk.length()-1],n1,n2);
    //             }
    //             else if (j==2){
    //                 n2 = apply_op(stk[stk.length()-1],n2,n3);
    //             }
    //             else if (j==3){
    //                 n3 = apply_op(stk[stk.length()-1],n3,n4);
    //             }
    //             stk = stk.substr(0,stk.length()-1);
    //             j--;
    //         }
    //         cout<<n1<<endl;
    //         break;
    //     }
    //     case 2:{
    //         string b=inp,e;
    //         cin>>e;
    //         cout<<expo(b,e)<<endl;
    //         break;
    //     }
    //     case 3:{
    //         string n1=inp,n2;
    //         cin>>n2;
    //         string mx,mn;
    //         if (compare(n1,n2)){
    //             mx=n1;
    //             mn=n2;
    //         } else {
    //             mx=n2;
    //             mn=n1;
    //         }
    //         cout<<gcd(mx,mn)<<endl;
    //         break;
    //     }
    //     case 4:
    //         cout<<fact(inp)<<endl;
    //         break;
    // }

    // string res = expo("287352697307","11");
    return 0;
}