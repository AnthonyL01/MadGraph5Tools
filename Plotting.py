import ROOT
import sys
import collections
import array 

#============Functions================#
		
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

#============Plotting=============================#
def Plotting (directory, JCutPT,JCutEta):
	Data = collections.namedtuple("Data", ["ET","Njets"])
	#Cuts applied to the particles
	ECutPT = 0
	ECutEta = 1000000000000000
	MCutPT = 0
	MCutEta = 1000000000000000

	#Arrays for temporary storing of the entries:	

	EventJ = TreeLeaves (directory, "jet_EventID" ,"jet_EventID")
	ETJ = TreeLeaves (directory, "jet_MissingET" ,"jet_MissingET")
	ElecPTJ = TreeLeaves (directory, "jet_ElectronPT" ,"jet_ElectronPT")
	ElecEtaJ = TreeLeaves (directory, "jet_ElectronEta" ,"jet_ElectronEta")
	MuonPTJ = TreeLeaves (directory, "jet_MuonPT" ,"jet_MuonPT")
	MuonEtaJ = TreeLeaves (directory, "jet_MuonEta" ,"jet_MuonEta")
	JetPTJ = TreeLeaves (directory, "jet_JetPT" ,"jet_JetPT")
	JetEtaJ = TreeLeaves (directory, "jet_JetEta" ,"jet_JetEta")
	print("Finished Reading Jet entries")


	EventJ0 = TreeLeaves (directory, "jet0_EventID" ,"jet0_EventID")
	ETJ0 = TreeLeaves (directory, "jet0_MissingET" ,"jet0_MissingET")
	ElecPTJ0 = TreeLeaves (directory, "jet0_ElectronPT" ,"jet0_ElectronPT")
	ElecEtaJ0 = TreeLeaves (directory, "jet0_ElectronEta" ,"jet0_ElectronEta")
	MuonPTJ0 = TreeLeaves (directory, "jet0_MuonPT" ,"jet0_MuonPT")
	MuonEtaJ0 = TreeLeaves (directory, "jet0_MuonEta" ,"jet0_MuonEta")
	JetPTJ0 = TreeLeaves (directory, "jet0_JetPT" ,"jet0_JetPT")
	JetEtaJ0 = TreeLeaves (directory, "jet0_JetEta" ,"jet0_JetEta")
	print("Finished Reading Jet0 entries")

	NumberOfJets=[]
	Jet=[]
	Jets=[]
	ETs=[]
	Evnt = []
	failed = []
	seen = set()
	print("Jet Cuts")
	for i in range(len(EventJ)):
		EvID = EventJ[i]
		ET = ETJ[i]
		EPT = ElecPTJ[i]
		EEta = ElecEtaJ[i]
		MPT = MuonPTJ[i]
		MEta = MuonEtaJ[i]
		JPT = JetPTJ[i]
		JEta = JetEtaJ[i]
		iterator = 0
		if ( EPT > ECutPT and EEta < ECutEta and MPT > MCutPT and MEta < MCutEta and JPT > JCutPT and JEta < JCutEta ):
			NumberOfJets.append(EvID)
			if ( EvID not in seen):
				Jets.append(ET)
				seen.add(EvID)
				Evnt.append(EvID)
				iterator = 1
		if (iterator == 0):
			failE = [EvID,ET]
			failed.append(failE)

	Jet0 = []
	for i in range(len(failed)):
		EvID = failed[i][0]
		ET = failed[i][1]
		if (EvID not in seen):
			Jet0.append(ET)
			Evnt.append(EvID)
			seen.add(EvID)
	
	seen0 = set()
	for i in range(len(EventJ0)):
		EvID = EventJ0[i]
		ET = ETJ0[i]
		EPT = ElecPTJ0[i]
		EEta = ElecEtaJ0[i]
		MPT = MuonPTJ0[i]
		MEta = MuonEtaJ0[i]
		if ( EPT > ECutPT and EEta < ECutEta and MPT > MCutPT and MEta < MCutEta and EvID not in seen0 and EvID not in seen):
			seen0.add(EvID)
			Jet0.append(ET)
			Evnt.append(EvID)

	z = 0
	j = 0
	for i in range(len(Evnt)):
			Event = Evnt[i]
			JetNumber = NumberOfJets.count(Event)
			if (JetNumber > 0):
				ET = Jets[z]
				z = z+1
			if (JetNumber == 0):
				ET = Jet0[j]
				j = j+1
			if (ET >= 192):
				ET = 192
			Jet.append(JetNumber)
			ETs.append(ET)
		
	return Data(ETs,Jet)
#==============End===========================#

#============HistoJet ==============================#
def HistoJet ( label, MissingET, SaveHistROOT):
	f = ROOT.TFile(SaveHistROOT,"UPDATE")
	StringOfName = label
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

JCutPT = float(sys.argv[6])
JCutEta = float(sys.argv[7])/10

#===========End Future Input arguments============#
Data = Plotting(directory, JCutPT,JCutEta)
ETs = Data.ET
Jets = Data.Njets


StringOfNameET = str("ET")
StringOfNameNJ = str("NJets")
HistoJet(StringOfNameET,ETs,SaveHistROOT)
HistoJet(StringOfNameNJ,Jets,SaveHistROOT)