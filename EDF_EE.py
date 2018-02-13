import operator 
import sys

def EDF_EE(filename):
	file=open(filename,'r')
	print 'File name is:', filename

	temp_list=[]
	run=[]
	finallist=[]
	details=[]
	line=[]
	firstline_details={}
	task_details={}
	Num_Of_Possible_Outcomes=0
	Diff_Combination=[]
	Total_Combinations=0


	def file_length_calculation(file_name):
		with open(file_name) as f_line:
			for i, d in enumerate(f_line):
				#print i 
				pass
		return i + 1
		
	File_Length=file_length_calculation(filename)
	#print File_Length

	with open(filename) as f_line:
		for i in range(1,File_Length):
			task_details[i]={}   #initialization of each task list		
			#print task_details[i]
			
		for n in range(0,File_Length):
			line=f_line.readline()  # reading each line from file
			line_details=line.split(' ')  #spliting each line based on ' ' 
			#print line_details
			
			# information from first_line from file
			
			if n==0:
				firstline_details["No_of_tasks"]=int(line_details[0])
				firstline_details["Total_exe_time"]=int(line_details[1])
				firstline_details["ActivePower_List@1188Mhz"]=int(line_details[2])
				firstline_details["ActivePower_List@918Mhz"]=int(line_details[3])
				firstline_details["ActivePower_List@648Mhz"]=int(line_details[4])
				firstline_details["ActivePower_List@384Mhz"]=int(line_details[5])
				firstline_details['IdlePower_List@LowestFrequency_List']=str(line_details[6])		
				firstline_details['IdlePower_List@LowestFrequency_List']=int(line_details[6].replace('\n',''))
				
				Exec_Power_List=firstline_details["ActivePower_List@1188Mhz"]/float(firstline_details["Total_exe_time"])
				Idle_Power_List=firstline_details["IdlePower_List@LowestFrequency_List"]/float(firstline_details["Total_exe_time"])
				#print firstline_details
				
			for j in range(1,File_Length):
				if n==j:
				
					task_details[j]['Task_Name']=line_details[0]
					task_details[j]['Period']=int(line_details[1])
					task_details[j]['Deadline']=task_details[j]['Period']
					task_details[j]['WCET@1188MHz']=int(line_details[2])
					task_details[j]['Execution_Time']=task_details[j]['WCET@1188MHz']
					task_details[j]['Remain_Execution_Time']=task_details[j]['WCET@1188MHz']
					
					task_details[j]['WCET@918MHz']=int(line_details[3])
					task_details[j]['WCET@648MHz']=int(line_details[4])
					line_details[5]=str(line_details[5])
					task_details[j]['WCET@384MHz']=line_details[5].replace('\n','')
					task_details[j]['WCET@384MHz']=int(line_details[5])

	New_List=[]
	for n in range(1,File_Length):
		New_List.append({'Task_Name':task_details[n]['Task_Name'],'Period':task_details[n]['Period'],0:task_details[n]['WCET@1188MHz'],1:task_details[n]['WCET@918MHz'],2:task_details[n]['WCET@648MHz'],3:task_details[n]['WCET@384MHz']})

	#print New_List    


	Power_List={1188:0.625,918:0.447,648:0.307,348:0.212}
	Frequency_List={0:1188,1:918,2:648,3:348}

	Energy_List={0:firstline_details["ActivePower_List@1188Mhz"]/float(1000),1:firstline_details["ActivePower_List@918Mhz"]/float(1000),2:firstline_details["ActivePower_List@648Mhz"]/float(1000),3:firstline_details["ActivePower_List@384Mhz"]/float(1000)}
	utilization=0.0
	Total_Energy_Calculated=0.0
	for a in range(0,4):
		for b in range(0,4):
			for c in range(0,4):
				for d in range(0,4):
					for e in range(0,4):						
						utilization=(float(New_List[0][a])/float(New_List[0]['Period']))+(float(New_List[1][b])/float(New_List[1]['Period']))+(float(New_List[2][c])/float(New_List[2]['Period']))+(float(New_List[3][d])/float(New_List[3]['Period']))+(float(New_List[4][e])/float(New_List[4]['Period']))

						
						Total_Combinations=Total_Combinations+1
						if utilization<1:

							Total_Energy_Calculated=(New_List[0][a]*(Energy_List[a]))+(New_List[1][b]*(Energy_List[b]))+(New_List[2][c]*(Energy_List[c]))+(New_List[3][d]*(Energy_List[d]))+(New_List[4][e]*(Energy_List[e]))
							Num_Of_Possible_Outcomes=Num_Of_Possible_Outcomes+1
							Diff_Combination.append({'w1 @':Frequency_List[a],'w2 @':Frequency_List[b],'w3 @':Frequency_List[c],'w4 @':Frequency_List[d],'w5 @':Frequency_List[e],'w1_Exec_Time':New_List[0][a],'w2_Exec_Time':New_List[1][b],'w3_Exec_Time':New_List[2][c],'w4_Exec_Time':New_List[3][d],'w5_Exec_Time':New_List[4][e],'Total_Energy_List':Total_Energy_Calculated})

	print "Total_Combinations :",Total_Combinations
	print "Possible_Combinations :",Num_Of_Possible_Outcomes

	Diff_Combination.sort(key=operator.itemgetter('Total_Energy_List'))

	print "Best Of Diff_Combination:",Diff_Combination[0]['Total_Energy_List']
	print Diff_Combination[0]
	

	task_details={1:{'#':'1','Task_Name':'w1','Period':task_details[1]['Period'],'Deadline':task_details[1]['Period'],'Execution_Time':Diff_Combination[0]['w1_Exec_Time'],'Remain_Execution_Time':Diff_Combination[0]['w1_Exec_Time'],'Frequency_List':Diff_Combination[0]['w1 @']},
		   2:{'#':'2','Task_Name':'w2','Period':task_details[2]['Period'],'Deadline':task_details[2]['Period'],'Execution_Time':Diff_Combination[0]['w2_Exec_Time'],'Remain_Execution_Time':Diff_Combination[0]['w2_Exec_Time'],'Frequency_List':Diff_Combination[0]['w2 @']},
		   3:{'#':'3','Task_Name':'w3','Period':task_details[3]['Period'],'Deadline':task_details[3]['Period'],'Execution_Time':Diff_Combination[0]['w3_Exec_Time'],'Remain_Execution_Time':Diff_Combination[0]['w3_Exec_Time'],'Frequency_List':Diff_Combination[0]['w3 @']},
		   4:{'#':'4','Task_Name':'w4','Period':task_details[4]['Period'],'Deadline':task_details[4]['Period'],'Execution_Time':Diff_Combination[0]['w4_Exec_Time'],'Remain_Execution_Time':Diff_Combination[0]['w4_Exec_Time'],'Frequency_List':Diff_Combination[0]['w4 @']},
		   5:{'#':'5','Task_Name':'w5','Period':task_details[5]['Period'],'Deadline':task_details[5]['Period'],'Execution_Time':Diff_Combination[0]['w5_Exec_Time'],'Remain_Execution_Time':Diff_Combination[0]['w5_Exec_Time'],'Frequency_List':Diff_Combination[0]['w5 @']}}


	Idle_State={'Task_Name':'IDLE'}
	queue=[]



	def EDF_Scheduler (x):
		if x==0:
			for y in range(1,File_Length):
				temp_list.append(task_details[y])   
				
		for y in range(1,File_Length):
			task_details[y]['Deadline']=task_details[y]['Deadline']-1
	
			if (x % task_details[y]['Period']==0 and x!=0):
				task_details[y]['Deadline']=task_details[y]['Deadline']+task_details[y]['Period']
				task_details[y]['Remain_Execution_Time']=task_details[y]['Execution_Time']
				temp_list.append(task_details[y])
				
		if len(temp_list)!=0:
			temp_list.sort(key=operator.itemgetter('Deadline'))
			queue.append(temp_list[0])
			

			run.append(temp_list[0]['Task_Name'])
			
			if temp_list[0]['Remain_Execution_Time']>0:
				temp_list[0]['Remain_Execution_Time']=temp_list[0]['Remain_Execution_Time']-1
				
				if temp_list[0]['Remain_Execution_Time']==0:
						temp_list.remove(temp_list[0])
						
		else:
			queue.append(Idle_State)

	#temp_list=[]
	maxUtilzation=1
	u=0.0
	Exec_Frequency_List=1188
	Idle_Frequency_List=384
	Exec_Power_List=firstline_details["ActivePower_List@1188Mhz"]/float(firstline_details["Total_exe_time"])
	Idle_Power_List=firstline_details["IdlePower_List@LowestFrequency_List"]/float(firstline_details["Total_exe_time"])
	TotalIdlePower_List=[] 

	for y in range(1,File_Length):
			u=u+task_details[y]['Execution_Time']/float(task_details[y]['Period'])
			
	if u<=maxUtilzation:
		print "Start_time  Task_Name End_time  Frequency_List_used  Energy_List_Consumed"
		
		for z in range(0,1000):
			EDF_Scheduler (z)
		
		Total_Energy_List=0
		Idle_Time=0
		
		for t in range(0,len(queue)):
			z=t+1
			if t==0:
				start=0
			if z!=len(queue):   
				if queue[t]['Task_Name']!=queue[z]['Task_Name']:
					end=t+1
					if queue[t]['Task_Name']!='IDLE':
						Total_Energy_List=Total_Energy_List+(end-start)*Power_List[queue[t]['Frequency_List']]
						print " ",start,"        ",queue[t]['Task_Name'],"       ",end,"        ",queue[t]['Frequency_List'],"        ",(end-start)*Power_List[queue[t]['Frequency_List']]," J"
					else: 
						Total_Energy_List=Total_Energy_List+(end-start)*0.84
						Idle_Time=Idle_Time+(end-start)
						print " ",start,"        ",queue[t]['Task_Name'],"      ",end,"       ","IDLE","        ",(end-start)*0.84," J"
						TotalIdlePower_List.append((end-start)*Idle_Power_List)				
					start=t+1
			if z==len(queue):
				if queue[t]['Task_Name']!='IDLE':
					print " ",start,"        ",queue[t]['Task_Name'],"       ",len(queue),"        ",queue[t]['Frequency_List'],"        ",(len(queue)-start)*Power_List[queue[t]['Frequency_List']]," J"
					Total_Energy_List=Total_Energy_List+(end-start)*Power_List[queue[t]['Frequency_List']]
				else:
					print " ",start,"        ",queue[t]['Task_Name'],"      ",len(queue),"       ","IDLE","        ",(len(queue)-start)*0.84," J"
					Idle_Time=Idle_Time+end-start
					Total_Energy_List=Total_Energy_List+(end-start)*0.84
					TotalIdlePower_List.append((len(queue)-startt)*Idle_Power_List)
		print "Total Energy_List Consumed : ",Total_Energy_List,"J"
		print "Total Idle Time :",Idle_Time
		print "Idle Time Percentage :",Idle_Time/float(10), "%"
		IdleSum=0
		for i in TotalIdlePower_List:
			IdleSum=IdleSum+i
		print("Total Energy_List Consumed by IDLE state:" ,IdleSum)
		print("% of  otal Energy_List Consumed by IDLE state:",IdleSum/round(Total_Energy_List,3)*100,"%")

	else:
		print "EDF_scheduling can't be acheived"