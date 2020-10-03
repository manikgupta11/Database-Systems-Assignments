#include <iostream>
#include <vector>
#include <string>
#include <fstream>
#include <sstream>
#include <climits>
#include<string.h>

using namespace std;

//dummy initalizes value of nodes in a block
#define dummy INT_MAX

int treeorder=3;

struct bnode{
    // valcount: nodes in block
    //value: value array    children:pointers array
    int valcount;
    int value[4];
    bnode *children[4];
    bnode *sibling;
    bnode *parent;
    bnode(){
        valcount = 0;

        for(int i=0; i<=treeorder; i++){
            value[i] = dummy;
        }
        for(int i=0; i<=treeorder; i++){
            children[i] = NULL;
        }
        parent = NULL;
        sibling = NULL;
    }
};

void split(bnode*,int);
void insert(bnode*, int);
void find(bnode*, int);
void range(bnode*, int ,int);
void count2(bnode*, int);
bnode *rootbnode;


void insert(bnode *curbnode, int val){
    bnode* childptr=curbnode->children[0];
    int curNodes=curbnode->valcount;
    int i;
    int leafnode;
    if(childptr==NULL) {
        //No child block, so insert in this block only, increment node value counter
        curbnode->valcount++;
        i=0;
        leafnode=1;
        //it has no child pointer so leaf node
        while(i<curNodes+1)   {
            if(val < curbnode->value[i]){ 
            //finding right place to insert value
              swap(curbnode->value[i], val);   
            }
            ++i;  
        } 
        
        if(curbnode->valcount==treeorder){
            //if values in block become equal to treeorder, then we split the block
            split(curbnode,leafnode);
        }
                
    }

    else {   
        //child block present
        i=0;
        leafnode=0;
        //since child block present, its not leaf node
        int cnodes=curbnode->valcount;
        while( i<curNodes+1){
            int cval=curbnode->value[i];
            if(val < cval){
                //if value less than current node value, insert in children block
                insert(curbnode->children[i], val);
                cnodes=curbnode->valcount;
                if(treeorder==cnodes){
                     //if values in block become equal to treeorder, then we split the block
                    split(curbnode,leafnode);
                }
                break;
            }
        ++i;
       } 
    }
    

}

void split(bnode *curbnode,int leafnode){
    
    int x=treeorder+1;
    //x = no of pointers = order + 1
    //dividing pointers after node splitting
    x/=2;

    int i=x;
    bnode *rightbnode = new bnode();

    curbnode->valcount = (treeorder+1)/2;
    //values in bloack would be halved after splitting

   
    if(leafnode==1){
        int leafptrs=treeorder-x;
        //new node will have ptrs equal to half the node before split
        rightbnode->valcount = leafptrs;
    }
    else{
        //split for non  leaf
        int nonleafptrs=treeorder-x-1;
        rightbnode->valcount = nonleafptrs;
    }
    rightbnode->parent = curbnode->parent;
    i=x;
    int j=0;
    while(i<treeorder+1){
        // copying values and ptrs of nodes(before split) to newly formed node
        int oldval=curbnode->value[i];
        bnode* oldptr=curbnode->children[i];
        
        rightbnode->value[j] = oldval;
        rightbnode->children[j] = oldptr;
        // values that shifted to new node will become dummies
        curbnode->value[i] = dummy;
        
        if(i != (treeorder+1)/2 ){

            curbnode->children[i] = NULL;
            curbnode->value[i] = dummy;
        }
        ++i;
        ++j;
    }
    int val = rightbnode->value[0];
    if(leafnode==0){
        //copying values and pointers after split
        int rnodes=rightbnode->valcount;
        size_t rnodesize = sizeof(int)*(rnodes+1);
        memcpy(&rightbnode->value, &rightbnode->value[1],rnodesize );
        int valcount=rightbnode->valcount;
        size_t rbsize = sizeof(rootbnode)*(rightbnode->valcount+1);
        memcpy(&rightbnode->children, &rightbnode->children[1], rbsize);
    
    }
    i=0;
    while(curbnode->children[i]!=NULL){
        curbnode->children[i]->parent = curbnode;
        ++i;
    }
    i=0;
    while(rightbnode->children[i]!=NULL){
        rightbnode->children[i]->parent = rightbnode;
        ++i;
    }
    bnode* rbbnode=rightbnode->sibling;
    bnode* cbbnode=curbnode->sibling;
    if(leafnode==1) {

        curbnode->sibling = rightbnode;
        rightbnode->sibling=cbbnode;

    }

    if(curbnode->parent==NULL){
        bnode *parent = new bnode();
        
        
        parent->value[0] = val;
        parent->valcount++; 
        parent->children[0] = curbnode;
        parent->children[1] = rightbnode;
        rightbnode->parent = parent;
        curbnode->parent =  parent;

        rootbnode = parent;
        return;
    }
    else{
        
        int cnodes=curbnode->valcount;
        bnode *newchildren = new bnode();
        newchildren = rightbnode;
        curbnode = curbnode->parent;
        for(i=0; i<=cnodes; i++){
            if(val < curbnode->value[i]){
                int temp=curbnode->value[i];
                curbnode->value[i]=val;
                val=temp;

            }
        }

        curbnode->valcount++;

        for(i=0; i<curbnode->valcount; i++){
            int nval=newchildren->value[0];
            int ccval=curbnode->children[i]->value[0];
            if( nval< ccval){
                bnode* temp=curbnode->children[i];
                curbnode->children[i]=newchildren;
                newchildren=temp;
                
            }
        }
        curbnode->children[i] = newchildren;
        i=0;
         while(curbnode->children[i]!=NULL){
            bnode* ccbnode=curbnode->children[i];
            ccbnode->parent = curbnode;
            ++i;
        }
    }

}


void find(bnode *curbnode, int val){
    bnode* childptr=curbnode->children[0];
    int curNodes=curbnode->valcount;
    int i;
    if(childptr==NULL){
        i=0;
        while(i<curNodes+1){
            if(val == curbnode->value[i])
            {   
                cout<<"YES"<<endl;
                return;
            }
            ++i;
       } 
       
    }
    else{
      i=0;
       while( i<=curNodes+1){
            if(val < curbnode->value[i]){
                find(curbnode->children[i], val);
                return;
            }
            ++i;
       } 
    }
   
    cout<<"NO"<<endl;

}

void range(bnode *curbnode, int val1,int val2)
{
    bnode* childptr=curbnode->children[0];
    int curNodes=curbnode->valcount;
    int i;

    if(childptr==NULL)  {
        int count=0;
        while(true) {
            i=0;
            while(i<curNodes+1){
                if(val1 <= curbnode->value[i]){

                    if(val2 >= curbnode->value[i]){   
                        ++count;
                    }
                }
                else if(curbnode->value[i] > val2 ) {
                    break;
                }
                ++i;
                
            }
            if(curbnode->sibling!=NULL){
                curbnode =  curbnode->sibling;
            }
            else{ 
                break; 
            }
        }
       cout<<count<<endl;
       
    }
    else {
        i=0;
       while( i<curNodes+1){
            if(val1 <= curbnode->value[i]) {
                range(curbnode->children[i], val1,val2);
                return;
            }
            ++i;
       } 
    }
}

void count2(bnode *curbnode, int val1)
{   int val2=val1;
    bnode* childptr=curbnode->children[0];
    int curNodes=curbnode->valcount;
    int i;

    if(childptr==NULL)  {
        int count=0;
        while(true) {
            i=0;
            while(i<curNodes+1){
                if(val1 <= curbnode->value[i]){

                    if(val2 >= curbnode->value[i]){   
                        ++count;
                    }
                }
                else if(curbnode->value[i] > val2 ) {
                    break;
                }
                ++i;
                
            }
            if(curbnode->sibling!=NULL){
                curbnode =  curbnode->sibling;
            }
            else{ 
                break; 
            }
        }
       cout<<count<<endl;
       
    }
    else {
        i=0;
       while( i<curNodes+1){
            if(val1 <= curbnode->value[i]) {
                range(curbnode->children[i], val1,val2);
                return;
            }
            ++i;
       } 
    }
}


int main(int argc, char *argv[]){
    
    if(argc==1) {
        printf("Enter file name \n"); 
        exit(0);
    }
    if(argc>2) {
        printf("Too many arguments. Only file name required \n"); 
        exit(0);
    }

    char* file;
    file=argv[1];
     

    treeorder=3;
   
    rootbnode = new bnode();

    std::fstream filestream(file, ios::in );

    if( filestream.is_open() ==0 ){
        cout<<"Failed to open file"<<endl;
        exit(0);
    }
    std::string line;
    std::string command;
    int value1,value2;


        while (filestream >> command){
            
            if(command == "insert"||command == "INSERT"){
                filestream >> value1;
                insert(rootbnode, value1);
            }

            else if(command=="range"||command=="RANGE"){
              
                filestream >> value1>>value2;;
                range(rootbnode, value1, value2);
            }
            else if(command=="find"||command=="FIND"){
                
                filestream >> value1;
                find(rootbnode, value1);
            }
            else if(command=="count"||command=="COUNT"){
                
                filestream >> value1;
                count2(rootbnode, value1);
            }
            else{
                cout<<"ONLY these command allowed: 1)insert 2)range 3)find 4) count \n";
            }
        }
       
    return 0;
}