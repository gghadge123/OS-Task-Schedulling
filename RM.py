import operator
import sys
def RM(filename):
	temp_list=[] 
	values=[] 
	queue=[] 
	firstline_details={} 
	task_details={} 

	
	File_Length=len((open(str(filename),"r")).readlines()) 

	
	with open(str(filename)) as file:
		for i in range(1,File_Length):
				task_details[i]={}   
		for j in range(0,File_Length):
			values = file.readline()  
			line=values.split(' ')
			  
			if j==0:
				firstline_details["Num_of_tasks"]=int(line[0]) 
				firstline_details["Total_exe_time"]=int(line[1]) 
				firstline_details["ActivePower@1188Mhz"]=int(line[2]) 
				firstline_details["ActivePower@918Mhz"]=int(line[3]) 
				firstline_details["ActivePower@648Mhz"]=int(line[4]) 
				firstline_details["ActivePower@384Mhz"]=int(line[5]) 
				firstline_details["IdlePower@LowestFreq"]=str(line[6])
				firstline_details["IdlePower@LowestFreq"]=int(firstline_details["IdlePower@LowestFreq"].replace('\n',''))
			        
			for z in range(1,File_Length):
				if z==j:
					task_details[j]['Task_Name']=line[0] 
					task_details[j]['Period']=int(line[1])
					task_details[j]['Deadline']=task_details[j]['Period']
					task_details[j]['WCET@1188Mhz']=int(line[2]) 
					task_details[j]['Execution_Time']=task_details[j]['WCET@1188Mhz'] 
					task_details[j]['Remain_Execution_Time']=task_details[j]['WCET@1188Mhz']              
					task_details[j]['WCET@918Mhz']=int(line[3]) 
					task_details[j]['WCET@648Mhz']=int(line[4]) 
					line[5]=str(line[5])
					task_details[j]['WCET@384Mhz']=line[5].replace('\n','') 
					task_details[j]['WCET@384Mhz']=int(task_details[j]['WCET@384Mhz'])
	Idle_State={'Task_Name':'IDLE', 'IdlePower@LowestFreq':'IDLE'} 

	def RM_Scheduler(x): 
		if x==0:
			for j in range(1,File_Length):
				temp_list.append(task_details[j])
		for j in range(1,File_Length):
			task_details[j]['Deadline']=task_details[j]['Deadline']-1
			if (x % task_details[j]['Period']==0 and x!=0):
				task_details[j]['Deadline']=task_details[j]['Deadline']+task_details[j]['Period']
				task_details[j]['Remain_Execution_Time']=task_details[j]['Execution_Time']
				temp_list.append(task_details[j])  
		if len(temp_list)!=0:
			temp_list.sort(key=operator.itemgetter('Period'))
			queue.append(temp_list[0])
			if temp_list[0]['Remain_Execution_Time']>0:
				temp_list[0]['Remain_Execution_Time']=temp_list[0]['Remain_Execution_Time']-1                    
				if temp_list[0]['Remain_Execution_Time']==0:               
					temp_list.remove(temp_list[0])        
		else:
			queue.append(Idle_State)
	taskFreq=1188 
	idleFreq= "IDLE"
	TotalIdlePower=[]  
	Exec_Power=firstline_details["ActivePower@1188Mhz"]/float( firstline_details["Total_exe_time"]) 
	#Exec_Power=round(Exec_Power,3)
	Idle_Power=firstline_details["IdlePower@LowestFreq"]/float( firstline_details["Total_exe_time"])  
	Idle_Power=round(Idle_Power,3)

	maxUtilization=0.74349 
	u=0.0
	for num in task_details:    
		u=u+task_details[num]['Execution_Time']/float(task_details[num]['Period'])

	def printer(queue,taskFreq,idleFreq,Exec_Power,Idle_Power):
		ln = len(queue)
		Idle_Time = 0
		Total_Energy = 0
		for t in range(0,ln):
			z=t+1
			if t==0:
				start=0
			if z!=ln:   
				if queue[t]['Task_Name']!=queue[z]['Task_Name']:
					end=t+1
					if queue[t]['Task_Name']!='IDLE':
						print "       ",start,"        ",queue[t]['Task_Name'],"      ",end,"       ",taskFreq,     "       ",(end-start)*Exec_Power
						Total_Energy = Total_Energy + (end-start)*Exec_Power

					else:
						print "       ",start,"        ",queue[t]['Task_Name'],"    ",end,"       ",idleFreq,"      ",round(((end-start)*Idle_Power),3)
						Idle_Time = Idle_Time + (end-start)
						Total_Energy = Total_Energy + (end-start)*Idle_Power
						TotalIdlePower.append((end-start)*Idle_Power)
					start=t+1
			if z==ln:
				if queue[t]['Task_Name']!='IDLE':  
					print    "       ",start, "        ",queue[t]['Task_Name'],"     ",len(queue),"       ",taskFreq,  "        ",round(((len(queue)-start)*Exec_Power),3)
					Total_Energy = Total_Energy + (len(queue)-start)*Exec_Power
				else:
					print  "    ",start,  "      ",queue[t]['Task_Name'],"     ",len(queue),"     ",idleFreq,"     ",round(((len(queue)-start)*Idle_Power),3)
					Idle_Time = Idle_Time + (end-start)
					Total_Energy = Total_Energy + (len(queue)-start)*Idle_Power
					TotalIdlePower.append((len(queue)-startt)*Idle_Power)
		print "Total Energy Consumed  = ", round(Total_Energy,3),"Jules"
		print "Total IDLE Time = ",Idle_Time
		print "Total IDLE Time % :", (Idle_Time/float(firstline_details["Total_exe_time"])*100),"%"
		IdleSum=0
		for i in TotalIdlePower:
			IdleSum=IdleSum+i

		print "Total Energy Consumed by IDLE state:" ,IdleSum
		print "% of  otal Energy Consumed by IDLE state:",IdleSum/round(Total_Energy,3)*100,"%"
		
			
	if u<=maxUtilization:
		print "Utilization :",u,"<",maxUtilization,"Utilization Limit "
		print "The eqution is satisfied ------> Rate Monotonic Scheduling can be achieved as below\n"
		print "Start_Time  Task_Name    End-Time   Frequency_Used    Energy(Jules)"            
		count = 0
		while(count<1000): 
			 RM_Scheduler(count)
			 count += 1    
		printer(queue,taskFreq,idleFreq,Exec_Power,Idle_Power)
	else:
		print "Utilization :",u,">",maxUtilization,"Utilization Limit"
		print " The equation is not satisfied-------> Tasks Cannot be Scheduled via Rate Monotonic Scheduling!!!!!"