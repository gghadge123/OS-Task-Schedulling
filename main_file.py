import sys
import RM
import RM_EE
import EDF
import EDF_EE

length=len(sys.argv)
filename=sys.argv[1]

if (length ==3):
	method=sys.argv[-1].upper()
	if method=='RM':
		RM.RM(filename)
	elif method=='EDF':
		EDF.EDF(filename)
	else:
		print "Enter a valid scheduling method"
elif (length==4):
	scheme=sys.argv[-1].upper()
	method=sys.argv[-2].upper()
	
	if scheme=='EE' and method=='RM':
		RM_EE.RM_EE(filename)
	elif scheme=='EE' and method=='EDF':
		EDF_EE.EDF_EE(filename)
	else:
		print "Enter a valid scheduling method"
	