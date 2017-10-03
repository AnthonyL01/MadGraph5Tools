import ROOT
import sys
import collections 

#============Functions================#

#================ Extracting Data from Delphes root =====================#
def RootReading ( directory, TreeName , Branch, LeafName ):
	LeafValues = []
	File = ROOT.TChain(str(TreeName))
	File.Add(directory)
	Number = File.GetEntries()
	for i in range(Number):
		Entry = File.GetEntry(i)
		string = str("File."+Branch+".GetEntries()")
		EntryFromBranch = eval(string)
		for j in range(EntryFromBranch):
			LeafValue = File.GetLeaf(str(LeafName)).GetValue(j)
			LeafValues.append(LeafValue)
	return LeafValues
#===============End RootReading===================#

#================ Extracting Data from Delphes root =====================#
def LeptonReading ( directory, TreeName , Branch, LeafName1, LeafName2, LeafName3):
	Lepton= collections.namedtuple("Lepton", ["PT", "Charge", "Eta"])
	LeafValues1 = []
	LeafValues2 = []
	LeafValues3 = []
	File = ROOT.TChain(str(TreeName))
	File.Add(directory)
	Number = File.GetEntries()
	for i in range(Number):
		Entry = File.GetEntry(i)
		string = str("File."+Branch+".GetEntries()")
		EntryFromBranch = eval(string)
		for j in range(EntryFromBranch):
			LeafValue1 = File.GetLeaf(str(LeafName1)).GetValue(j)
			LeafValue2 = File.GetLeaf(str(LeafName2)).GetValue(j)
			LeafValue3 = File.GetLeaf(str(LeafName3)).GetValue(j)
			LeafValues1.append(LeafValue1)
			LeafValues2.append(LeafValue2)
			LeafValues3.append(LeafValue3)
	return Lepton(LeafValues1, LeafValues2, LeafValues3)
#===============End Lepton===================#

#================ Extracting Data from Delphes root =====================#
def JetReading ( directory, TreeName , Branch, LeafName1, LeafName2 ):
	Jet= collections.namedtuple("Jet", ["PT", "Eta"])
	LeafValues1 = []
	LeafValues2 = []
	File = ROOT.TChain(str(TreeName))
	File.Add(directory)
	Number = File.GetEntries()
	for i in range(Number):
		Entry = File.GetEntry(i)
		string = str("File."+Branch+".GetEntries()")
		EntryFromBranch = eval(string)
		for j in range(EntryFromBranch):
			LeafValue1 = File.GetLeaf(str(LeafName1)).GetValue(j)
			LeafValue2 = File.GetLeaf(str(LeafName2)).GetValue(j)
			LeafValues1.append(LeafValue1)
			LeafValues2.append(LeafValue2)
	return Jet(LeafValues1, LeafValues2)
#===============End JetReading===================#
		
#======Extracting Data from Delphes Tree==========#
def TreeLeaves ( directory, TreeName, LeafName):
	LeafValues = []
	File = ROOT.TFile(directory)
	string = str("File."+TreeName)
	TreeEvents = eval(string)
	for i in TreeEvents:
		LeafString = str("i."+LeafName)
		Leaf = eval(LeafString)
		LeafValues.append(Leaf)
	return LeafValues
#===========End Delphes Tree =====================#

#============HistoJet ==============================#
def HistoJet ( label, Process, MissingET, SaveHistROOT,scaling ):
	f = ROOT.TFile.Open(SaveHistROOT,"UPDATE")
	StringOfName = "h" + Process +"Nom_" + label + "_obs_met"
	max_size = 200
	min_size = 0
	delta = 20
	lengthy = len(MissingET)
	h1 = ROOT.TH1F(StringOfName,StringOfName,delta,min_size,max_size)
	for i in range(lengthy):
		temp = MissingET[i]
		h1.Fill(temp)
	h1.Scale(scaling)
	h1.Write()
	f.Close()
#=============End HistoJet ===============================#

############Program Start##########################

#============Future Input agruments===============#
directory= "~/Testing/pptt1.root"
DelphFile = "ppttNoCUTOpFlOpCh.root"
name = "pptt"
process = "pptt"
output = "~/Testing"
SaveHistROOT = str(output+"/"+DelphFile)

#===========End Future Input arguments============#

NewFile = ROOT.TFile(SaveHistROOT, "RECREATE")
NewFile.Close()
TreeNames="Delphes"


#preparing all the data arrays from Delphes
ET = RootReading(directory, TreeNames, "MissingET", "MissingET.MET")
print("Finished ET")

#=====Electrons============# 
Electron_size = TreeLeaves(directory, TreeNames, "Electron_size")
ElectronEntries = LeptonReading(directory, TreeNames, "Electron", "Electron.PT","Electron.Charge","Electron.Eta")
ElectronPT = ElectronEntries.PT
ElectronCharge = ElectronEntries.Charge
ElectronEta = ElectronEntries.Eta

print("Finished Electrons")
#=========Muon=============#
Muon_size = TreeLeaves(directory, TreeNames, "Muon_size")
MuonEntries = LeptonReading(directory, TreeNames, "Muon", "Muon.PT","Muon.Charge","Muon.Eta")
MuonPT = MuonEntries.PT
MuonCharge = MuonEntries.Charge
MuonEta = MuonEntries.Eta

print("Finished Muon")
#=========Jets=============#
Jets_size = TreeLeaves(directory, TreeNames, "Jet_size")
JetEntries = JetReading(directory, TreeNames, "Jet", "Jet.PT", "Jet.Eta")
JetPT = JetEntries.PT
JetEta = JetEntries.Eta
	
print("Finished Jets")
#Find Dilepton Events
#temp iteration variables to retrieve root entries
EvID = 1
el = 0
mu = 0
je = 0
	

#Cuts applied to the particles
ECutPT = 0
ECutEta = 1000000 #2.47
MCutPT = 0
MCutEta = 1000000 #2.5
JCutPT = 0
JCutEta = 1000000 #2.5

#Arrays for temporary storing of the entries:
Electron = []
Muon = []
Jet = []
Jet0 = []	

#sorting the data into arrays and indexing them with EvID (EventID) along with cutting
for i in range(len(Jets_size)):
	JetS = Jets_size[i]
	MuonS = Muon_size[i]
	ElectronS = Electron_size[i]
	MissingET = ET[i]
	
	#Getting entries from leaves of root file
	#==========Electrons=============#
	passE = [] # This ensures that the loop does not throw an error 
	for e in range(ElectronS):
		EPT = ElectronPT[el]
		ECh = ElectronCharge[el]
		EEta = abs(ElectronEta[el])
		if (EPT > ECutPT and EEta < ECutEta): #We perform the cuts 
			passE = [EvID,MissingET,ECh]
		el = el +1 
		if (len(passE) > 0):	#If passE is non zero save to list
			Electron.append(passE)	
	#===========Muon=================#
	passM = [] # This ensures that the loop does throw an error 
	for m in range(MuonS):
		MPT = MuonPT[mu]
		MCh = MuonCharge[mu]
		MEta = abs(MuonEta[mu])
		if (MPT > MCutPT and MEta < MCutEta): #We perform the cuts 
			passM = [EvID,MissingET,MCh]
		mu = mu +1
		if (len(passM) > 0):	#If passE is non zero save to list
			Muon.append(passM)
	#============Jets================#
	iteration = 0  #reset counter
	passJ = []
	for j in range(JetS):
		JPT = JetPT[je]
		JEta = abs(JetEta[je])
		if (JPT > JCutPT and JEta < JCutEta):
			iteration = iteration + 1	#counts the number of times a jet is counted and therefore accepted 
			passJ = [EvID,MissingET]
		je = je +1
	if (iteration == 0): #none of the jets have passed therefore it's a 0 jet event
		tempJ0 = [EvID,MissingET]			
		Jet0.append(tempJ0)
	if (iteration > 0):
		Jet.append(passJ)
	EvID = EvID + 1

#Comparing the lepton arrays and enforcing opposite charge 
#this then leads to opposite charge and opposite flavor
OpFlOpCh = []
for e in range(len(Electron)):
	ECharge = Electron[e][2]
	EEvent = Electron[e][0]
	ET = Electron[e][1]
	if (ET > 200):
		ET = 200
	for m in range(len(Muon)):
		MCharge = Muon[m][2]
		MEvent = Muon[m][0]
		if (ECharge != MCharge  and EEvent == MEvent):
			temp = [EEvent,ET]
			OpFlOpCh.append(temp)

#We now find the jets corresponding to the DiLepton Events
DlJ = []
DlJ0 = []
for i in OpFlOpCh:
	EventID = i[0]
	ET = i[1]
	for j in Jet:
		EventIDJet = j[0]
		if (EventID == EventIDJet):
			DlJ.append(ET)	
	for x in Jet0:
		EventIDJet0 = x[0]
		if (EventID == EventIDJet0):
			DlJ0.append(ET)
#========== ROOT Figures ============#
HistoJet ( "jets", process,DlJ, SaveHistROOT,1 )
HistoJet ( "jets0", process, DlJ0, SaveHistROOT,1 )