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

#=========== Validation and Signal Regions =======#
def Region ( MissingET, NumberOfJets, GreEqu ):
	Output = collections.namedtuple("Output",["SRET" , "SRJTS", "VRET", "VRJTS"])
	SRMissingET = []
	SRJets = []
	VRMissingET = []
	VRJets = []
	length = len(MissingET)
	for i in range(length):	
		cut = MissingET[i]
		jets = NumberOfJets[i]
		if ( cut < GreEqu ): # <---- Signal Region
			SRMissingET.append(cut)
			SRJets.append(jets)
		if ( cut >= GreEqu ): # <------ Validation Region
			VRMissingET.append(cut)
			VRJets.append(jets)	
	return Output(SRMissingET, SRJets, VRMissingET, VRJets )
#======= End Validation and Signal Regions ========#

#=========== Histograms ===========================#
def HistoGrams ( Region, Process, Jets, SaveHistROOT ):
	f = ROOT.TFile(SaveHistROOT,"UPDATE")
	StringOfName = "h" + Process +"Nom_" + Region + "_obs_njets"
	max_size = int(max(Jets))
	min_size = int(min(Jets))
	delta = max_size - min_size
	lengthy = len(Jets)
	#_______First Historgam__________#
	h1 = ROOT.TH1F(StringOfName,StringOfName,delta,min_size,max_size)
	for i in range(lengthy):
		temp = Jets[i]
		h1.Fill(temp)

	#_____Second Histogram___________#
	h2 = ROOT.TH1F(StringOfName,StringOfName,3,0,3)
	for i in range(lengthy):
		temp = Jets[i]
		h2.Fill(temp)

	#______Third Histogram___________#
	h3 = ROOT.TH1F(StringOfName,StringOfName,2,0,3)
	for i in range(lengthy):
		temp = Jets[i]
		h3.Fill(temp)

	#____ creating Root File for Histograms______________#
	h1.Write()
	h2.Write()
	h3.Write()
	f.Close()
#===========End Histogram ==========================#
############Program Start##########################

#============Future Input agruments===============#
#directory = str(sys.argv[1]) 
directory= str("MadGraph5/bin/pptt/Events/run_01/tag_1_delphes_events.root")
SaveHistROOT = str("~/MadShell/Results/pptt.root")
TreeNames = "Delphes"
BranchName = "MissingET"
LeafNamey = "Jet_size"
LeafNamex = "MissingET.MET"
PlotName = "Hello"
Cutx = 30
Cuty = 0
#===========End Future Input arguments============#

x = RootReading(directory, TreeNames, BranchName, LeafNamex) #Defined function at the beginning of script 
y = TreeLeaves(directory, TreeNames, LeafNamey)	      #Defined function at the beginning of script
#==================================================#
#____________Performing Cuts in the array__________#
R = Region(x , y, Cutx)
SRJet = R.SRJTS
VRJet = R.VRJTS

HistoGrams("SR","ttbar",SRJet, SaveHistROOT)
HistoGrams("VR","ttbar",VRJet, SaveHistROOT)