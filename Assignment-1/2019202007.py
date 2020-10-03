import csv
import sys
import sqlparse
import operator
from prettytable import PrettyTable

metadata_info={}
table_values={}
identifierList = []
join_table=[]
join_values=[]

def main():
    query=str(sys.argv[1])
    query=query.split(';')[0]
    #print("sysargs: ",query)
    try:
        readMetaData()
        readTables()    
        #query="Select table1.A, table1.B fRoM table1, table2 where table1.A < 0"
        evaluateQuery(query)

    except Exception as e:
        print("Error: ", str(e))

def readMetaData():
    """
    Reads metadata.txt file and constructs metadata_info dictionary 
    where key is table name and value is list of columns in that table

    """
    fp=open("metadata.txt",'r')
    attr=[]
    table_started=0
    for i in fp:
        i=i.strip()
        if i=='<begin_table>':
            attr=[]
            table_started=1
        elif table_started==1:
            table_name=i
            table_started=2
        elif i=='<end_table>':
            metadata_info[table_name]=attr
            table_started=0
        elif table_started==2:
            attr.append(table_name+'.'+ i)
    #print("metadata: ",metadata_info)  
            
def readTables():
    """
    Reads csv files for all tables and constructs table_values dictionary
    where key is table name and value is list of list of entries in that table

    """
    for key in metadata_info:
        table=key
        row=[]
        with open(table+".csv", 'r') as csvfile: 
            csvreader = csv.reader(csvfile) 
            for i in csvreader: 
                #print(row)
                row.append(i)
     
        table_values[table]=row
    #print("table_values: ",table_values)

    
def evaluateQuery(query):

        parsedQuery=sqlparse.parse(query)[0].tokens
        getid=sqlparse.sql.IdentifierList(parsedQuery).get_identifiers()
    		
        for i in getid:
            identifierList.append(str(i))

        #print(identifierList)

        processtable()
        processwhere()
        processaggregate()
        processprojection()
                
def processtable():
     """
     checks no of tables used in query.
     If 2 tables are used, join them.
     join_table stores columns of joined table
     join_values stores values of joined table

     """
     tables=str(identifierList[3].replace(" ",""))
     #print(tables)

     if(len(tables.split(','))==2): table1,table2=tables.split(",")[0],tables.split(",")[1]
     else: table1,table2=tables,""

     #print(table1)
     
     if(table1 not in metadata_info):
        print(table1," is not present in metadata")
        exit()

     for i in metadata_info[table1]:
        join_table.append(i)
     
     for i in table_values[table1]:
        join_values.append(i)
     
     if(len(tables.split(','))==2):
        if(table1 not in metadata_info):
            print(table1," is not present in metadata")
            exit()

        for i in metadata_info[table2]:
            join_table.append(i)

        join_values.clear()
        for i in table_values[table1]:
            for j in table_values[table2]:
                temp=i+j
                join_values.append(temp)

     #print("join table_values: ",join_table)
     #print("length of join table: ",len(join_values))
        
def processwhere():
     """
     processes where condition,perform comparisons and project 
     required columns

     """

     if(len(identifierList)==5):
         conditional_query=str(identifierList[4].replace(" ",""))
         conditional_query=conditional_query.split("where")[1]
         andop,orop=0,0
         where_condition="";where_condition_2=""

         if(len(conditional_query.split("and"))==2): 
            andop=1
            where_condition=conditional_query.split("and")[0]
            where_condition_2=conditional_query.split("and")[1]  

         elif(len(conditional_query.split("or"))==2): 
            orop=1
            where_condition=conditional_query.split("or")[0]
            where_condition_2=conditional_query.split("or")[1] 

         else:
            where_condition=conditional_query
         
         # print("full condition: "+conditional_query)
         # print("cond1: "+where_condition)
         # print("cond2: "+where_condition_2)

         operators=['=','<','>','>=','<=']
         operator1='';condition_table='';condition_value=''
         operator2='';condition_table_2='';condition_value_2=''

         for i in operators:
            if(len(where_condition.split(i))==2):
                condition_table=where_condition.split(i)[0]
                condition_value=where_condition.split(i)[1]
                operator1=i

         if(orop==1 or andop==1):
             for i in operators:
                if(len(where_condition_2.split(i))==2):
                    condition_table_2=where_condition_2.split(i)[0]
                    condition_value_2=where_condition_2.split(i)[1]
                    operator2=i

         # print("condition 1 and 2: operator, table, value")
         # print(operator1)
         # print(condition_table)
         # print(condition_value)

         # print(operator2)
         # print(condition_table_2)
         # print(condition_value_2)

         if(condition_table not in join_table):
            print(condition_table," is not present in metadata")
            exit()

         condition_table_index=join_table.index(condition_table)

         if(orop==1 or andop==1):
             if(condition_table_2 not in join_table):
                print(condition_table_2," is not present in metadata")
                exit()
             condition_table_index_2=join_table.index(condition_table_2)

         if(identifierList[1]=="*"):
            cols_to_project=join_table
         else:
            cols_to_project=identifierList[1].replace(" ","")
            cols_to_project=cols_to_project.split(',')
       
         #print(cols_to_project)
         #print("columns to project: ",cols_to_project)
         colList=[]
         for col in cols_to_project: 
             #print(col)

             ind=join_table.index(col)
             
             colList.append(ind)

         #print(colList)
         
         ans=[]
         
         for i in join_values:
            temp=[]
            for col in colList:
                temp.append(i[col])

            ops = { "<": operator.lt, ">": operator.gt,"<=": operator.le, ">=": operator.ge,"=": operator.eq } 

            if(andop):
                if(    (ops[operator1](int(i[condition_table_index]),int(condition_value)))   and    (ops[operator2](int(i[condition_table_index_2]),int(condition_value_2)))    ):
                    ans.append(temp)

            elif(orop):
                if(    (ops[operator1](int(i[condition_table_index]),int(condition_value)))   or    (ops[operator2](int(i[condition_table_index_2]),int(condition_value_2)))    ):
                    ans.append(temp)
            else:
                #print(int(i[condition_table_index]))
                if(    (ops[operator1](int(i[condition_table_index]),int(condition_value)))   ):
                    
                    ans.append(temp)

         #print(len(ans))
         t = PrettyTable(cols_to_project)
         for i in ans:
            t.add_row(i)

         print(t)



def processaggregate():
    """
    process aggregate functions min,max,sum,avg

    """

    if(len(identifierList)==5):
        return
    aggregatefn=identifierList[1].replace(" ","")
   
    if(identifierList[1]=='*'):
        t = PrettyTable(join_table)
        for i in join_values:
            t.add_row(i)
        print(t)

    elif(len(identifierList[1].split('('))==2):
        
        aggregatefn1=aggregatefn.split('(')[0].lower()
        aggregatecol=aggregatefn.split('(')[1].split(')')[0]
        aggregatecolindex=join_table.index(aggregatecol)
        aggregatelist=[]
        for i in join_values:
            aggregatelist.append(int(i[aggregatecolindex]))
        # print("aggregatefn: ",aggregatefn1 )
        # print("aggregatecol: ",aggregatecol)
        # print("aggregatelist: ",aggregatelist) 

       
        
        if(aggregatefn1=="max"):
            print(identifierList[1])
            print(max(aggregatelist))

        elif(aggregatefn1=='min'):
            print(identifierList[1])
            print(min(aggregatelist))

        elif(aggregatefn1=='sum'):
            print(identifierList[1])
            print(sum(aggregatelist))

        elif(aggregatefn1=='avg'):
            print(identifierList[1])
            print(sum(aggregatelist)/len(aggregatelist))

        elif(aggregatefn1=='distinct'):
            x = PrettyTable()
            x.field_names =[identifierList[1]]
            for i in set(aggregatelist):
                x.add_row([i])
            print(x)

        else:
            print(aggregatefn1," is not a valid aggregate function")

    else:
        pass


def processprojection():
     """
     process columns to be projected from relation
    
     """
     
     if(len(identifierList)==5):
        return
     if(identifierList[1]=="*"):
        return
     if(len(identifierList[1].split('('))==2):
        return     
     cols=identifierList[1]

     cols=cols.split(',')
     #print(cols)
     #print(func)
     colList=[]
     for col in cols: 
         if col in join_table:
             colList.append(join_table.index(col))
         else:
             print(col,"is not present in table")
             return
         
     #print(colList)
  
     t = PrettyTable(cols)
     
     for i in join_values:
        temp=[]
        for col in colList:
            
            temp.append(i[col])
        t.add_row(temp)

     print(t)
   
    
if __name__ == "__main__":
    main()