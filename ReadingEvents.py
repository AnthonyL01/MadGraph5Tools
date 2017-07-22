#==================MadReading====BY THOMAS NOMMENSEN==================================
from decimal import *
import numpy as np
import time
import ROOT
import sys

#**********************PDG Renaming scheme************************#
def PDGRename(code):
	#=====Quarks======#
	name = "Not There, PDG:" +str(code)
	if code == 1:
		name = "d"
	if code == -1:
		name = "[d]" #Antiparticle
	if code == 2:
		name = "u"
	if code == -2:
		name = "[u]" #Antiparticle
	if code ==  3:
		name = "s"
	if code == -3:
		name = "[s]" #Antiparticle
	if code == 4:
		name = "c"
	if code == -4:
		name = "[c]" #Antiparticle
	if code == 5:
		name = "b"
	if code == -5:
		name = "[b]" #Antiparticle
	if code ==  6:
		name = "t"
	if code == -6:
		name = "[t]" #Antiparticle
	if code ==  7:
		name = "b'"
	if code == -7:
		name = "[b']" #Antiparticle
	if code == 8:
		name = "t'"
	if code == -8:
		name = "[t']" #Antiparticle
	
	#======Leptons========#
	if code == 11:
		name = "e-"
	if code == -11:
		name = "e+" #Antiparticle
	if code ==  12:
		name = "ve"
	if code == -12:
		name = "[ve]" #Antiparticle
	if code ==  13:
		name = "mu-"
	if code == -13:
		name = "mu+" #Antiparticle
	if code ==  14:
		name = "vmu"
	if code == -14:
		name = "[vmu]" #Antiparticle
	if code ==  15:
		name = "tau-"
	if code == -15:
		name = "tau+" #Antiparticle
	if code ==  16:
		name = "vtau"
	if code == -16:
		name = "[vtau]" #Antiparticle
	
	#======Gauge and Bosons======#
	if code == 21:
		name = "g"
	if code == 22:
		name = "photon"
	if code == 23:
		name = "Z0"
	if code == 24:
		name = "W+" 
	return name;

#********************End of Function****************************************************

# This script is to extract the event data from the MadGraph file LHE 

#Create arrays which are to be filled with the Data
#Column_Data represents the 4X13 array data
#Above_Column_Data represents the entries above the 4X13 array data (expected size 1X6)

#===================Data arrays=====================================================
AllData = []
Column_Data = []
Above_Column_Data = []
Output=[]

#===================Reading=========================================================
# In this section we are reading the data LHE file and converting it to actual numbers
i = 0
IndexE = 0
IndexM = 0
directory = str(sys.argv[1]) 
with open(directory) as File:
	for line in File:			
		i = i + 1
		if "<event>" in line:
			IndexE = i
			
		if "</event>" in line:
			IndexM = i
		a = IndexE - IndexM
		if a > 0:			
			removing = line.replace("<event>","")	
			data = removing.split()
			Numbers = [float(x) for x in data]
			AllData.append(Numbers)
print("Finished Reading")
#==================Organise in appropriate arrays======================================
for i in range(len(AllData)):
	t = AllData[i]
	#=== creating a dynamic table if there is a change in size ===#
	if t == []:
		temp = i
		Above_Column_Data.append(AllData[temp+1])
	temp2 = i
	tem = temp -temp2
	if abs(tem) >= 2:
		Column_Data.append(AllData[i])

#__________________For Column_Data_________________________________
f = 0	#intermediate variable
run = 1	#Event Number 
for i in range(len(Column_Data)):		
	Batch = Column_Data[i]
	PDGCode = float(str(Batch[0:1]).strip("[]"))	# From this coding we can deduce the particles 
	states = float(str(Batch[1:2]).strip("[]")) 	# This will be used to identify initial or final 
	mass = float(str(Batch[10:11]).strip("[]")) 	# Mass
	spin = float(str(Batch[12:13]).strip("[]")) 	# Spin of the states
	pz = float(str(Batch[8:9]).strip("[]"))		# 
	px = float(str(Batch[6:7]).strip("[]"))		# momentum (GeV)
	py = float(str(Batch[7:8]).strip("[]"))		#
	lifetime = float(str(Batch[11:12]).strip("[]"))	#Decay
	condition = abs(tem)-1	
	if f == condition:
		f = 0 
		run = run +1	
	if f < condition:
		f = f+1
		if states == -1:
			states = "Initial"
		if states == 1:
			states = "Final"
		if states == 2:
			states = "Intermediate"	
		if spin == 1:
			spin = "up"
		if spin == -1:
			spin = "down"
		if spin == 0:
			spin = "no spin"
	#============PDG Numbering for some particles=============#
		name = PDGRename(PDGCode) #See at the start of file... its a function 
		ReFormatedData = [run,states,name,spin,px,py,pz] 
		Output.append(ReFormatedData) #Saving the output 
#print(Output)
print("Finished Organizing")
#=================Extracting User Readable Information==================================
# Above_Column_Data 
NumberOfParticles=[]
CrossSection = []
Energy = []
Alpha = []
for i in range(len(Above_Column_Data)):
	Global = Above_Column_Data[i]
	NumberOfParticles.append(Global[0:1])
	CrossSection.append(Global[2:3])
	Energy.append(Global[3:4])
	Alpha.append(Global[4:6])
print(NumberOfParticles)