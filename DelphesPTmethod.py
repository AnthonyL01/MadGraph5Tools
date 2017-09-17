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

#=============Jet Filter ==========================#
def JetFilter ( MissingET, NumberOfJets, limit ):
	Output = collections.namedtuple("Output", ["JetCut","JetRemain"])
	ETCut = []
	ETRemain = []
	length = len(NumberOfJets)
	for i in range(length):
		cut = NumberOfJets[i]
		ET = MissingET[i]
		if (cut <= limit): # <----- Collects Jets for cut
			ETCut.append(ET)
		if (cut > limit): # <----- Collects Residue
			ETRemain.append(ET)
	return Output(ETCut,ETRemain)
#==============End Jet Filter ======================#

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
place=sys.argv[1]
DelphFile = sys.argv[4]
directory= str(place)
output = sys.argv[5]
SaveHistROOT = str(output+"/"+DelphFile)
TreeNames = "Delphes"
BranchName = "MissingET"
LeafNamex = "MissingET.MET"
scaling = 1
MissingMuonPTVar = sys.argv[6]
MissingElectronPTVar = sys.argv[5]
MissingJetPTVar = sys.argv[5]
#===========End Future Input arguments============#

NewFile = ROOT.TFile(SaveHistROOT, "RECREATE")
NewFile.Close()

#=====Adjust these to fit isabelles data =====
names = sys.argv[2]
processes = sys.argv[3] 
for p in range(1):
	name = names
	directory= str(place)
	ET = RootReading(directory, TreeNames, BranchName, LeafNamex) 	#Defined function at the beginning of script 
	Electron_size = TreeLeaves(directory, TreeNames, "Electron_size")
	Electron_PT = RootReading(directory, TreeNames, "Electron", "Electron.PT")
	ElectronCharge = RootReading(directory, TreeNames, "Electron","Electron.Charge")
	
	Muon_size = TreeLeaves(directory, TreeNames, "Muon_size")
	Muon_PT = RootReading(directory, TreeNames, "Muon", "Muon.PT")
	MuonCharge = RootReading(directory, TreeNames, "Muon","Muon.Charge")
	
	jets = TreeLeaves(directory, TreeNames, "Jet_size")
	JetEta = RootReading(directory,TreeNames,"Jet","Jet.Eta")
	JetPT = RootReading(directory,TreeNames,"Jet","Jet.PT")

	ElectronData = []
	MuonData = []
	JetData = []
	
	#Collecting the Data from the root file
	q = 0 #Used for JetPT index
	a = 0
	h = 0
	for y in range(len(jets)):
		Mu = Muon_size[y]
		Electron = Electron_size[y]
		Jet = jets[y]
		ETMissing = ET[y]
		for el in range(Electron):
			ElectronPT = Electron_PT[a]
			ECharge = ElectronCharge[a]
			a = a + 1	
			tempEL = [ETMissing,ElectronPT,ECharge,y]
			ElectronData.append(tempEL) 
			
		for mu in range(Mu):
			MuonPT = Muon_PT[h]
			MCharge = MuonCharge[h]
			h = h + 1
			tempMU = [ETMissing,MuonPT,MCharge,y] 
			MuonData.append(tempMU)
			
		for x in range(Jet):
			JetMP = JetPT[q]
			q = q +1
			J = [ETMissing,JetMP,y,Jet]
			JetData.append(J)

	#Filtering through events which meet the criteria of Jets, Electron, Muon PT
	ConditionMetElectron = []
	ConditionMetMuon = []
	ConditionMetJet = []
	
	#==========Electrons=======================#
	EventRemoved = []
	for i in range(len(ElectronData)):
		ConditionEP = ElectronData[i][1]
		EventIndex = ElectronData[i][3]
		if (ConditionEP >= MissingElectronPTVar):
			ConditionMetElectron.append(ElectronData[i])
		else:
			EventRemoved.append(EventIndex)
	
	#This cleans the array from contamination of dileptons with same flavor events for which only 
	#one of the two has passed the above condition 
	for i in range(len(ConditionMetElectron)):
		EventPassed = ConditionMetElectron[i][3]
		for j in range(len(EventRemoved)):
			EventRemove = EventRemoved[j]
			if (EventRemove == EventPassed):
				del ConditionMetElectron[i][:]
				
	CleanElectron= []
	for i in range(len(ConditionMetElectron)):
		Data = ConditionMetElectron[i]
		if (Data == []):
			continue 
		else:
			CleanElectron.append(Data)
	
	#==============Muons========================#
	EventRemoved = []
	for i in range(len(MuonData)):
		ConditionMP = MuonData[i][1]
		EventIndex = MuonData[i][3]
		if (ConditionMP >= MissingMuonPTVar):
			ConditionMetMuon.append(MuonData[i])
		else:
			EventRemoved.append(EventIndex)
			
	#This cleans the array from contamination of dileptons with same flavor events for which only 
	#one of the two has passed the above condition 
	for i in range(len(ConditionMetMuon)):
		EventPassed = ConditionMetMuon[i][3]
		for j in range(len(EventRemoved)):
			EventRemove = EventRemoved[j]
			if (EventRemove == EventPassed):
				del ConditionMetMuon[i][:]
	
	CleanMuon= []
	for i in range(len(ConditionMetMuon)):
		Data = ConditionMetMuon[i]
		if (Data == []):
			continue 
		else:
			CleanMuon.append(Data)
	
	#=============Jets============================#
	EventRemoved = []
	for i in range(len(JetData)):
		ConditionJP = JetData[i][1]
		EventIndex = JetData[i][2]
		if (ConditionJP >= MissingJetPTVar):
			ConditionMetJet.append(JetData[i])
		else:
			EventRemoved.append(EventIndex)
					
	for i in range(len(ConditionMetJet)):
		EventPassed = ConditionMetJet[i][2]
		for j in range(len(EventRemoved)):
			EventRemove = EventRemoved[j]
			if (EventRemove == EventPassed):
				del ConditionMetJet[i][:]

	CleanJet= []
	for i in range(len(ConditionMetJet)):
		Data = ConditionMetJet[i]
		if (Data == []):
			continue 
		else:
			CleanJet.append(Data)
	#=============Enforcing the conditions=============#
	#This section will now enforce the condition that all events satify the above conditions simultaneously
	MissingETandJets = []
	for i in range(len(CleanElectron)):
		IndexElectron = CleanElectron[i][3]
		MET = CleanElectron[i][0]
		for j in range(len(CleanMuon)):
			IndexMuon = CleanMuon[j][3]
			MMET = CleanMuon[j][0]
			if (IndexElectron==IndexMuon):
				for z in range(len(CleanJet)):
					JET = CleanJet[z][0]
					NumberOfJets = CleanJet[z][3]
					IndexJet = CleanJet[z][2]
					if (IndexMuon == IndexJet):
						temp = [MMET,NumberOfJets]
						MissingETandJets.append(temp)
	x = []
	y = []
	#Removing dupicate ET 
	CleanData = []
	for k in MissingETandJets:
		if k not in CleanData:
			CleanData.append(k)
	#Creates the Histograms for all the processes after the filtering 
      	#Defined function at the beginning of script
      	for j in range(len(CleanData)):
		ET = CleanData[j][0]
		Jets = CleanData[j][1]
		x.append(ET)
		y.append(Jets)
	scaling = 1
	process = processes
	Jet1 = JetFilter(x,y,0) #<----
	ETJ0 = Jet1.JetCut
	ETRemain = Jet1.JetRemain
	HistoJet ( "jets", process,ETRemain, SaveHistROOT,scaling )
	HistoJet ( "jets0", process, ETJ0, SaveHistROOT,scaling )
