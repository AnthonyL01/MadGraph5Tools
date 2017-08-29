#========================================================================#
# This is developed to extract data from the log files created by HistFitter and 
# 				MadGraph 5 after running MadShell
#=================BY THOMAS NOMMENSEN==================================
from decimal import *
import time
import ROOT
import sys
#===================Data arrays=====================================================
Process = []
Luminosity = []
Xsection = []
Events = []

#===================Reading=========================================================
# In this section we are reading the log text and filtering out useless text to extract the cross section... 
IndexE = 0
IndexM = 0
j = 0
with open("MadShellLog1.txt") as File:
	for i in File:			
		if "launch" in i:
			launch = str(i.strip(" launch"))
			j = 0
			E = 0
			C = 0
			Process.append(launch)
		if "Effective Luminosity" in i and E < 1:
			string = str(i.strip("INFO: ").strip("Effective Luminosity"))
			E = 1
			Luminosity.append(string)
		if "Cross-section :" in i and C < 1:
			C = 1
			Cross = str(i.strip("Cross-section :"))
			Xsection.append(Cross)
		if "Nb of events :  " in i and j < 1:
			events = str(i.strip("Nb of events:"))
			number = float(events)
			j = 1
			Events.append(number)

for x in range(len(Events)):
	P = Process[x]
	L = Luminosity[x]
	X = Xsection[x]
	E1 = Events[x]
	E2 = Events[x-1]
	delta = E2-E1
	if delta > 0 or delta < 0:
	