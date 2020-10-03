import math
import sys
import time

def main():
	start_time = time.time()

	print("############# starting execution ###############")
	input_file=sys.argv[1]
	output_file=sys.argv[2]
	fx=open("metadata.txt",'r')
	main_memory_in_mb=int(sys.argv[3])
	order=sys.argv[4]
	sort_order=sys.argv[5:]
	main_memory=main_memory_in_mb*1024*1024

	columns=[]
	columns_size=[]

	tuple_size=0
	no_of_tuples=0
	for i in fx:
		i.replace(" ","")
		columns.append(i.split(',')[0])
		columns_size.append(int(i.split(',')[1]))
	f0=open(input_file,'r')
	for i in f0:
		no_of_tuples+=1
	# sort_order=["col0","col1","col2"]
	sort_order_indices=[]
	for i in sort_order:
		sort_order_indices.append(columns.index(i))
	# print(sort_order_indices)
	print("columns: ",columns)
	print("columnss size: ",columns_size)
	print("no of tuples: ",no_of_tuples)
	tuple_size=sum(columns_size)+len(columns)*2-1
	file_size=no_of_tuples*tuple_size
	print("file size: ",file_size)

	# no_of_splits=math.ceil(file_size/main_memory)
	# records_in_one_file=math.ceil(no_of_tuples/no_of_splits)
	records_in_one_file2=math.floor(main_memory/tuple_size)
	no_of_splits2=math.ceil(no_of_tuples/records_in_one_file2)
	# print("no of splits: ",no_of_splits)
	# print("records in a file: ",records_in_one_file)
	print("no of splits: ",no_of_splits2)
	print("records in a file: ",records_in_one_file2)
	split(input_file,columns_size,records_in_one_file2,sort_order_indices,no_of_splits2,order)
	merge(columns_size,sort_order_indices,output_file,order,no_of_splits2)
	# your code
	elapsed_time = time.time() - start_time
	print("\nTime elapsed(in seconds): ",elapsed_time)

def split(input_file,columns_size,records_in_one_file2,sort_order_indices,no_of_splits2,order):
	print("\n############# phase1:splitting and sorting files ###############")
	input_file=sys.argv[1]
	f1=open(input_file,'r')
	tuples=[]
	j=0	
	fileno=0
	for line in f1:
		y=[]
		m=0
		for i in columns_size:
			y.append(line[m:m+i])
			m=m+2+i
		
		# y[2]=y[2].rstrip()
		
		tuples.append(y)
		# print(tuples)
		# print(len(tuples))
		j+=1
		if(j==records_in_one_file2):
			fn=lambda x:[x[i] for i in sort_order_indices]
			print("Sorting tuples for file: ",fileno)
			if(order=="asc"):
				tuples.sort(key=fn )
			elif(order=="desc"):
				tuples.sort(key=fn ,reverse=True)
			# tuples.sort()

			# print(fileno)
			f=open(str(fileno)+".txt","w+")
			print("Writing tuples for file: ",fileno)
			for k in tuples:
				f.write("  ".join(k))
				f.write("\n")
			fileno+=1
			f.close()
			tuples.clear()
			j=0

	fn=lambda x:[x[i] for i in sort_order_indices]
	print("Sorting tuples for file: ",fileno)
	if(order=="asc"):
		tuples.sort(key=fn )
	elif(order=="desc"):
		tuples.sort(key=fn ,reverse=True)
	# print(fileno)
	# print(len(tuples))
	f=open(str(fileno)+".txt","w+")
	print("Writing tuples for file: ",fileno)
	for k in tuples:
		# print(k)
		f.write("  ".join(k))
		f.write("\n")
	f.close()
	tuples.clear()

def merge(columns_size,sort_order_indices,output_file,order,no_of_splits2):
	print("\n############# Phase2: Merging sorted files ###############")
	
	fptr=[]
	for i in range(no_of_splits2):
		fo=open(str(i)+".txt")
		fptr.append(fo)
	
	list1=[]

	for j in range(len(fptr)):
		line1=fptr[j].readline()
		if not line1:
			break
		# print(line1.split("  "))

		y=[]
		m=0
		for i in columns_size:
			y.append(line1[m:m+i])
			m=m+2+i
			# print(y)
		# print("ok")
		# print(y)
		list1.append([y,j])
	
	opf=open(output_file,"w+")
	opf=open(output_file,"a+")
	# cntr=0
	print("Writing to output file ")
	while True:
		# cntr+=1
		# print(len(list1))
		if(len(list1)==0): 
			opf.close()
			break
		fn=lambda x:[x[0][i] for i in sort_order_indices]
		# fn=lambda x:x[0][3]
		# print(min(list1,key=fn))
		# opf.write("  ".join(min(list1,key=fn)[0]))
		# opf.write("\n")
		
		if order=="asc":
			opf.write("  ".join(min(list1,key=fn)[0]))
			opf.write("\n")
			ind=min(list1,key=fn)[1]
			list1.remove( min(list1,key=fn) )
		elif order=="desc":
			opf.write("  ".join(max(list1,key=fn)[0]))
			opf.write("\n")
			ind=max(list1,key=fn)[1]
			list1.remove( max(list1,key=fn) )

		# print("fptr: ",ind)
		
		line2=fptr[ind].readline()
		# print(line2)
		if not line2:
			continue
		y=[]
		m=0
		for i in columns_size:
			y.append(line2[m:m+i])

			m=m+2+i

		print
		list1.append([y,ind])


	print("############# Execution completed ###########")
	opf.close()

if __name__=="__main__":
	main()


