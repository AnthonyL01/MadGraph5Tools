#========================================================================#
# This is developed to extract data from the log files created by HistFitter and 
# 				MadGraph 5 after running MadShell
#=================BY THOMAS NOMMENSEN==================================
import os
#===================Data arrays=====================================================
Process = []
Luminosity = []
Xsection = []
Events = []

#===================Reading=========================================================
# In this section we are reading the log text and filtering out useless text to extract the cross section... 
j = 0
FileIn = "MadShellLog1.txt"
FileOut = "Clean.txt"	
with open(FileIn) as File:
	for i in File:			
		if "launch" in i:
			launch = str(i.strip(" launch").rstrip())
			j = 0
			E = 0
			C = 0
			Process.append(launch)
		if "Effective Luminosity" in i and E < 1:
			string = str(i.strip("INFO: ").strip("Effective Luminosity").rstrip())
			E = 1
			Luminosity.append(string)
		if "Cross-section :" in i and C < 1:
			C = 1
			Cross = str(i.strip("Cross-section :").rstrip())
			Xsection.append(Cross)
		if "Nb of events :  " in i and j < 1:
			events = str(i.strip("Nb of events:").rstrip())
			j = 1
			Events.append(events)
#===================Filtering=====================#
for i in Process:
	exec("%s = %s" % (i,[])) #<---- creates dynamic arrays for each of the names in process

for x in range(len(Events)):
	P = Process[x]
	L = Luminosity[x]
	X = Xsection[x]
	E1 = Events[x]
	x = " Events: "+E1+" Luminosity: "+L+" Cross-Section: "+X
	eval(P).append(x)

#========= Writing to File=======
file = open("test.txt","w")
for i in Process:
	file.write("\n")
	lines="==============================="+i+"==================================="
	file.write(lines)
	file.write("\n")
	for x in eval(i):
		file.write(x)
		file.write("\n")
file.close()

file = open(FileOut,"w")
readlines= []
for line in open("test.txt"):
	if line not in readlines:
		readlines.append(line)
		file.write(line)
file.close()
os.remove("test.txt")