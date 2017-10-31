import ROOT
import sys
import collections
import array 

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
def HistoJet ( label, Process, MissingET, SaveHistROOT):
	f = ROOT.TFile(SaveHistROOT,"UPDATE")
	StringOfName = label+"_"+Process
	Tree = ROOT.TTree(str(StringOfName),"")
	collect = array.array('d',xrange(1))
	Data = Tree.Branch(str(StringOfName), collect, 'collect/D')
	x = 0
	for i in MissingET:
		collect[0] = i
		Tree.Fill()
		x = x +1
	f.Write()
	f.Close()
#=============End HistoJet ===============================#

############Program Start##########################

#============Future Input agruments===============#
directory= sys.argv[1]
DelphFile = sys.argv[4]
name = sys.argv[2]
process = sys.argv[3]
output = sys.argv[5]
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
		passE = [EvID,MissingET,EPT,ECh,EEta]
		Electron.append(passE)
		el = el +1 
	#===========Muon=================#
	passM = [] # This ensures that the loop does throw an error 
	for m in range(MuonS):
		MPT = MuonPT[mu]
		MCh = MuonCharge[mu]
		MEta = abs(MuonEta[mu])
		passM = [EvID,MissingET,MPT,MCh,MEta]
		Muon.append(passM)
		mu = mu +1

	#============Jets================#
	iteration = 0  #reset counter
	passJ = []
	for j in range(JetS):
		JPT = JetPT[je]
		JEta = abs(JetEta[je])
		passJ = [EvID,MissingET,JPT,JEta]
		Jet.append(passJ)
		je = je +1

	tempJ0 = [EvID,MissingET,0,0]			
	Jet0.append(tempJ0)

	EvID = EvID + 1


#Comparing the lepton arrays and enforcing opposite charge 
#this then leads to opposite charge and opposite flavor
seen = set()
OpFlOpCh = []
for e in range(len(Electron)):
	ECharge = Electron[e][3]
	EEvent = Electron[e][0]
	ET = Electron[e][1]
	EPT = Electron[e][2]
	EEta = Electron[e][4]
	for m in range(len(Muon)):
		MCharge = Muon[m][3]
		MEvent = Muon[m][0]
		MPT = Muon[m][2]
		MEta = Muon[m][4]
		if (ECharge != MCharge  and EEvent == MEvent):
			temp = [EEvent,ET,EPT,EEta,MPT,MEta]
			OpFlOpCh.append(temp)


#We now find the jets corresponding to the DiLepton Events
IDJ = []
ETJ = []
EPTJ = []
EEtaJ = []
MPTJ = []
MEtaJ = []
JPTJ = []
JEtaJ = []

IDJ0 = []
ETJ0 = []
EPTJ0 = []
EEtaJ0 = []
MPTJ0 = []
MEtaJ0 = []
JPTJ0 = []
JEtaJ0 = []
for i in OpFlOpCh:
	EventID = i[0]
	ET = i[1]
	EPT = i[2]
	EEta = i[3]
	MPT = i[4]
	MEta = i[5]
	for j in Jet:
		EventIDJet = j[0]
		JPT = j[2]
		JEta = j[3]
		if (EventID == EventIDJet):
			IDJ.append(EventID)
			ETJ.append(ET)
			EPTJ.append(EPT) #
			EEtaJ.append(EEta)
			MPTJ.append(MPT)
			MEtaJ.append(MEta)
			JPTJ.append(JPT)
			JEtaJ.append(JEta)
	for x in Jet0:
		EventIDJet0 = x[0]
		JPT0 = x[2]
		JEta0 = x[3]
		if (EventID == EventIDJet0):
			IDJ0.append(EventID)
			ETJ0.append(ET)
			EPTJ0.append(EPT)
			EEtaJ0.append(EEta)
			MPTJ0.append(MPT)
			MEtaJ0.append(MEta)
			JPTJ0.append(JPT0)
			JEtaJ0.append(JEta0)

#========== ROOT Figures ============#
HistoJet ( "jet", "EventID",IDJ, SaveHistROOT)
HistoJet ( "jet", "MissingET",ETJ, SaveHistROOT)
HistoJet ( "jet", "ElectronPT",EPTJ, SaveHistROOT)
HistoJet ( "jet", "ElectronEta",EEtaJ, SaveHistROOT)
HistoJet ( "jet", "MuonPT",MPTJ, SaveHistROOT)
HistoJet ( "jet", "MuonEta",MEtaJ, SaveHistROOT)
HistoJet ( "jet", "JetPT",JPTJ, SaveHistROOT)
HistoJet ( "jet", "JetEta",JEtaJ, SaveHistROOT)

HistoJet ( "jet0", "EventID",IDJ0, SaveHistROOT)
HistoJet ( "jet0", "MissingET",ETJ0, SaveHistROOT)
HistoJet ( "jet0", "ElectronPT",EPTJ0, SaveHistROOT)
HistoJet ( "jet0", "ElectronEta",EEtaJ0, SaveHistROOT)
HistoJet ( "jet0", "MuonPT",MPTJ0, SaveHistROOT)
HistoJet ( "jet0", "MuonEta",MEtaJ0, SaveHistROOT)
HistoJet ( "jet0", "JetPT",JPTJ0, SaveHistROOT)
HistoJet ( "jet0", "JetEta",JEtaJ0, SaveHistROOT)

