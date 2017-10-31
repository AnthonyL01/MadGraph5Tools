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

#============HistoJet ==============================#
def HistoJet ( label, Process, MissingET, SaveHistROOT,scaling ):
	f = ROOT.TFile(SaveHistROOT,"UPDATE")
	StringOfName = "h" + Process +"Nom_" + label + "_obs_met"
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


#____________Performing Cuts in the array__________#


#Cuts applied to the particles
ECutPT = 0
ECutEta = 1000000000000000
MCutPT = 0
MCutEta = 1000000000000000
JCutPT = float(sys.argv[6])
JCutEta = float(sys.argv[7])/10

#Arrays for temporary storing of the entries:
Electron = []
Muon = []
Jet = []
Jet0 = []	


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

seen = set()
Jet = []
failed = []
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
	iteration = 0
	if ( EPT > ECutPT and EEta < ECutEta and MPT > MCutPT and MEta < MCutEta and JPT > JCutPT and JEta < JCutEta ):
		passE = [EvID, ET]
		if ( EvID not in seen):
			Jet.append(ET)
			seen.add(EvID)
			iteration = 1
	if (iteration == 0):
		failE = [EvID,ET]
		failed.append(failE)

# Removing the duplicate instnces where a jet may not have passed initially but others did
Jet0 = []
for i in range(len(failed)):
	EvID = failed[i][0]
	ET = failed[i][1]
	if (EvID not in seen):
		Jet0.append(ET)
		seen.add(EvID)

seen0 = set()
for i in range(len(EventJ0)):
	EvID = EventJ0[i]
	ET = ETJ0[i]
	if (ET > 192):
		ET=192
	EPT = ElecPTJ0[i]
	EEta = ElecEtaJ0[i]
	MPT = MuonPTJ0[i]
	MEta = MuonEtaJ0[i]
	if ( EPT > ECutPT and EEta < ECutEta and MPT > MCutPT and MEta < MCutEta and EvID not in seen0 and EvID not in seen):
		seen0.add(EvID)
		Jet0.append(ET)


HistoJet ( "jets0", process, Jet0, SaveHistROOT,1 )
HistoJet ( "jets", process, Jet, SaveHistROOT,1 )

