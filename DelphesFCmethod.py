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

#================Lepton Size=======================#
def LeptonSize (ET, jets, Electron_size, Muon_size):
	Lepton = collections.namedtuple("Lepton",["Muon","Electron"])
	Muon = []
	Electron = []
	eq = 0
	muq = 0
	for j in range(len(ET)):
		Jet = jets[j]
		ElectronSize = Electron_size[j]
		MuonSize = Muon_size[j]
		MissingET = ET[j]
		if (ElectronSize == 1):
			ElecCharge = ElectronCharge[eq] 
			collectEl = [MissingET, ElecCharge, Jet, j]
			Electron.append(collectEl)
			eq = eq + 1
		if (MuonSize == 1):
			MuCharge = MuonCharge[muq]
			collectMu = [MissingET, MuCharge, Jet, j]
			Muon.append(collectMu)
			muq = muq + 1
	return Lepton(Muon,Electron)
#=============End Lepton Size======================#

#============Lepton Charge Filter===================#
def LeptonChargeFilter(LeptonArray):
	LeptonCharge = collections.namedtuple("Charge",["Minus","Plus"])
	LeptonPlus = []
	LeptonMinus = []
	for i in range(len(LeptonArray)):
		ET = LeptonArray[i][0]
		Charge = LeptonArray[i][1]
		Jets = LeptonArray[i][2]
		index = LeptonArray[i][3]
		if (Charge == -1):
			TempE = [ET,Jets,index]
			LeptonMinus.append(TempE)
		if (Charge == 1):
			TempP = [ET,Jets,index]
			LeptonPlus.append(TempP) 
	return LeptonCharge(LeptonMinus,LeptonPlus)
#==============End Lepton Charge Filter============#

#======================Merger=====================#
def Merger(LeptonArray1,LeptonArray2):
	Merger = []
	for j in range(len(LeptonArray1)):
		IndexMM = LeptonArray1[j][2]
		ETMM = LeptonArray1[j][0]
		JetMM = LeptonArray1[j][1]
		for i in range(len(LeptonArray2)):
			IndexP = LeptonArray2[i][2]
			ETP = LeptonArray2[i][0]
			JetP = LeptonArray2[i][1]
			if (IndexP == IndexMM):
				TempArrayMP = [ETMM,JetMM]
				Merger.append(TempArrayMP)
	return Merger
#====================End Merger====================# 
			
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

#===========End Future Input arguments============#

NewFile = ROOT.TFile(SaveHistROOT, "RECREATE")
NewFile.Close()

#=======Performing cuts==============#
names = sys.argv[2]
Scales = 1
processes = sys.argv[3]
print(names)
print(place)
print(processes)
for i in range(1):
	name = names
	directory= str(place)
	ET = RootReading(directory, TreeNames, BranchName, LeafNamex) 	#Defined function at the beginning of script 
	Electron_size = TreeLeaves(directory, TreeNames, "Electron_size")
	Muon_size = TreeLeaves(directory, TreeNames, "Muon_size")
	jets = TreeLeaves(directory, TreeNames, "Jet_size")
	ElectronCharge = RootReading(directory, TreeNames, "Electron","Electron.Charge")
	MuonCharge = RootReading(directory, TreeNames, "Muon","Muon.Charge")
	
	#Arrays
	MuonArray = []
	ElectronArray = []
	MuPlusElectron = []
	MuMinusPositron = []
	x = []
	y = []
	
	#Filters the Electrons and Muons from the ROOT file with their missing ET
	Leptons = LeptonSize(ET,jets,Electron_size,Muon_size)
	MuonArray=Leptons.Muon
	ElectronArray=Leptons.Electron

	#Categorizing leptons according to charge 
	ElectronCharge = LeptonChargeFilter(ElectronArray)
	Electron = ElectronCharge.Minus
	Positron = ElectronCharge.Plus
	MuonCharge = LeptonChargeFilter(MuonArray)
	MuonMinus = MuonCharge.Minus
	MuonPlus = MuonCharge.Plus

	#This uses index matching to determine the nature of the individual events
	MuMinusPositron = Merger(MuonMinus,Positron)
	MuPlusElectron = Merger(MuonPlus,Electron)
	Total = MuMinusPositron + MuPlusElectron 
	
	#Creates the Histograms for all the processes after the filtering 
      	#Defined function at the beginning of script
      	for j in range(len(Total)):
		ET = Total[j][0]
		Jets = Total[j][1]
		x.append(ET)
		y.append(Jets)
	scaling = 1
	process = processes
	Jet1 = JetFilter(x,y,0) #<----
	ETJ0 = Jet1.JetCut
	ETRemain = Jet1.JetRemain
	HistoJet ( "jets", process,ETRemain, SaveHistROOT,scaling )
	HistoJet ( "jets0", process, ETJ0, SaveHistROOT,scaling )