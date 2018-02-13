
import operator 
import sys

def EDF(filename):

	file=open(filename,'r')
	print 'File name is:', filename

	temp_list=[]
	run=[]
	finallist=[]
	details=[]
	line=[]
	firstline_details={}
	task_details={}


	def file_length_calculation(file_name):
		with open(file_name) as f_line:
			for i, l in enumerate(f_line):
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
			
			#extracting information from first_line from file
			
			if n==0:
				firstline_details["No_of_tasks"]=int(line_details[0])
				firstline_details["Total_exe_time"]=int(line_details[1])
				firstline_details["ActivePower@1188Mhz"]=int(line_details[2])
				firstline_details["ActivePower@918Mhz"]=int(line_details[3])
				firstline_details["ActivePower@648Mhz"]=int(line_details[4])
				firstline_details["ActivePower@384Mhz"]=int(line_details[5])
				firstline_details['IdlePower@LowestFrequency']=str(line_details[6])		
				firstline_details['IdlePower@LowestFrequency']=int(line_details[6].replace('\n',''))
				
				Exec_Power=firstline_details["ActivePower@1188Mhz"]/float(firstline_details["Total_exe_time"])
				Idle_Power=firstline_details["IdlePower@LowestFrequency"]/float(firstline_details["Total_exe_time"])
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
				

				
				


	Idle_State={'Task_Name':'IDLE'}
	queue=[]

	#print Idle_State

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
	Exec_Frequency=1188
	Idle_Frequency=384
	Exec_Power=firstline_details["ActivePower@1188Mhz"]/float(firstline_details["Total_exe_time"])
	Idle_Power=firstline_details["IdlePower@LowestFrequency"]/float(firstline_details["Total_exe_time"])
	TotalIdlePower=[]
	for y in range(1,File_Length):
			u=u+task_details[y]['Execution_Time']/float(task_details[y]['Period'])
			
	if u<=maxUtilzation:
		print "Start_time  Task_Name End_time  Frequency_used  Energy_Consumed"
		
		for z in range(0,1000):
			EDF_Scheduler (z)
		
		Total_Energy=0
		Idle_Time=0
		
		for t in range(0,len(queue)):
			z=t+1
			if t==0:
				start=0
			if z!=len(queue):   
				if queue[t]['Task_Name']!=queue[z]['Task_Name']:
					end=t+1
					if queue[t]['Task_Name']!='IDLE':
						Total_Energy=Total_Energy+(end-start)*Exec_Power
						print " ",start,"        ",queue[t]['Task_Name'],"       ",end,"        ",Exec_Frequency,"        ",(end-start)*Exec_Power," J"
					else: 
						Total_Energy=Total_Energy+(end-start)*Idle_Power
						Idle_Time=Idle_Time+(end-start)
						print " ",start,"        ",queue[t]['Task_Name'],"      ",end,"       ","IDLE","        ",(end-start)*Idle_Power," J"
						TotalIdlePower.append((end-start)*Idle_Power)
					start=t+1
			if z==len(queue):
				if queue[t]['Task_Name']!='IDLE':
					print " ",start,"        ",queue[t]['Task_Name'],"       ",len(queue),"        ",Exec_Frequency,"        ",(len(queue)-start)*Exec_Power," J"
					Total_Energy=Total_Energy+(end-start)*Exec_Power
				else:
					print " ",start,"        ",queue[t]['Task_Name'],"      ",len(queue),"       ","IDLE","        ",(len(queue)-start)*Idle_Power," J"
					Idle_Time=Idle_Time+end-start
					Total_Energy=Total_Energy+(end-start)*Idle_Power
					TotalIdlePower.append((len(queue)-start)*Idle_Power)
		print "Total Energy Consumed : ",Total_Energy,"J"
		print "Total Idle Time :",Idle_Time
		print "Idle Time Percentage :",Idle_Time/float(10), "%"
		IdleSum=0
		#print TotalIdlePower
		for i in TotalIdlePower:
			IdleSum=IdleSum+i
		print("Total Energy Consumed by IDLE state:" ,IdleSum)
		print("% of  otal Energy Consumed by IDLE state:",IdleSum/round(Total_Energy,3)*100,"%")


	else:
		print "EDF_scheduling can't be acheived"