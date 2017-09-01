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
def HistoJet ( label, Process, MissingET, SaveHistROOT ):
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
	h1.Write()
	f.Close()
#============End HistoJet ===============================#

#=========== HistogramsRegion ===========================#
def HistoGramsRegion ( Region, Process, Jets, SaveHistROOT ):
	f = ROOT.TFile(SaveHistROOT,"UPDATE")
	StringOfName = "h" + Process +"_" + Region + "_obs_njets"
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
#===========End HistogramRegion ==========================#

############Program Start##########################

#============Future Input agruments===============#
#directory = str(sys.argv[1]) 
#Process = str(sys.argv[1])
#Cuty = int(sys.argv[2])

directory= str("~/Programs/MadGraph/bin/ttpp/Events/run_01/tag_1_delphes_events.root")
directory2 = str("~/MadShell/Data/histo14.root")
SaveHistROOT = str("~/MadShell/Results/Results.root")
TreeNames = "Delphes"
BranchName = "MissingET"
LeafNamey = "Jet_size"
LeafNamex = "MissingET.MET"

#===========End Future Input arguments============#



#____________Performing Cuts in the array__________#
histograms = []
histfile = ROOT.TFile(directory2)
NewFile = ROOT.TFile(SaveHistROOT, "RECREATE")
histnames = histfile.GetListOfKeys()
for i in histnames:
	kname = i.GetName()
	if ( kname == "httbarNom_jets_obs_met" ):
		continue
	if ( kname == "httbarNom_jets0_obs_met" ):
		continue
	if ( kname == "hWWNom_jets_obs_met" ):
		continue
	if ( kname == "hWWNom_jets0_obs_met" ):
		continue
	if ( kname == "hWZNom_jets_obs_met" ):
		continue
	if ( kname == "hWZNom_jets0_obs_met" ):
		continue
	if ( kname == "hWjetsNom_jets_obs_met" ):
		continue
	if ( kname == "hWjetsNom_jets0_obs_met" ):
		continue
	if ( kname == "hZZNom_jets_obs_met" ):
		continue
	if ( kname == "hZZNom_jets0_obs_met" ):
		continue
	if ( kname == "hZjetsNom_jets_obs_met" ):
		continue
	if ( kname == "hZjetsNom_jets0_obs_met" ):
		continue
	if (kname == "hWWJETEffectiveNPLow_jets_obs_met" ):
		continue
	if (kname == "hWWJETEffectiveNPLow_jets0_obs_met" ):
		continue
	if (kname == "hWZJETEffectiveNPLow_jets_obs_met" ):
		continue
	if (kname == "hWZJETEffectiveNPLow_jets0_obs_met" ):
		continue
	if (kname == "hWjetsJETEffectiveNPLow_jets_obs_met" ):
		continue
	if (kname == "hWjetsETEffectiveNPLow_jets0_obs_met" ):
		continue
	if (kname == "hWtJETEffectiveNPLow_jets_obs_met" ):
		continue
	if (kname == "hWtJETEffectiveNPLow_jets0_obs_met" ):
		continue
	if (kname == "hZZJETEffectiveNPLow_jets_obs_met" ):
		continue
	if (kname == "hZZJETEffectiveNPLow_jets0_obs_met" ):
		continue
	if (kname == "hWjetsJETEffectiveNPLow_jets_obs_met" ):
		continue
	if (kname == "hWjetsJETEffectiveNPLow_jets0_obs_met" ):
		continue
	if (kname == "httbarJETEffectiveNPLow_jets_obs_met" ):
		continue
	if (kname == "httbarETEffectiveNPLow_jets0_obs_met" ):
		continue
	if (kname == "hZjetsJETEffectiveNPLow_jets_obs_met" ):
		continue
	if (kname == "hZjetsETEffectiveNPLow_jets0_obs_met" ):
		continue
	if (kname == "hWWJETEffectiveNPHigh_jets_obs_met" ):
		continue
	if (kname == "hWWJETEffectiveNPHigh_jets0_obs_met" ):
		continue
	if (kname == "hWZJETEffectiveNPHigh_jets_obs_met" ):
		continue
	if (kname == "hWZJETEffectiveNPHigh_jets0_obs_met" ):
		continue
	if (kname == "hWjetsJETEffectiveNPHigh_jets_obs_met" ):
		continue
	if (kname == "hWjetsETEffectiveNPHigh_jets0_obs_met" ):
		continue
	if (kname == "hWtJETEffectiveNPHigh_jets_obs_met" ):
		continue
	if (kname == "hWtJETEffectiveNPHigh_jets0_obs_met" ):
		continue
	if (kname == "hZZJETEffectiveNPHigh_jets_obs_met" ):
		continue
	if (kname == "hZZJETEffectiveNPHigh_jets0_obs_met" ):
		continue
	if (kname == "hWjetsJETEffectiveNPHigh_jets_obs_met" ):
		continue
	if (kname == "hWjetsJETEffectiveNPHigh_jets0_obs_met" ):
		continue
	if (kname == "httbarJETEffectiveNPHigh_jets_obs_met" ):
		continue
	if (kname == "httbarJETEffectiveNPHigh_jets0_obs_met" ):
		continue
	if (kname == "httbarJETEffectiveNPLow_jets0_obs_met" ):
		continue
	if (kname == "hZjetsJETEffectiveNPHigh_jets_obs_met" ):
		continue
	if (kname == "hZjetsJETEffectiveNPHigh_jets0_obs_met" ):
		continue
	if (kname == "hZjetsJETEffectiveNPLow_jets_obs_met" ):
		continue
	if (kname == "hZjetsJETEffectiveNPLow_jets0_obs_met" ):
		continue

	if (kname == "hRatioNom_jets_obs_met" ):
		continue
	if (kname == "hRatioNom_jets0_obs_met" ):
		continue
	else:
		hist = i.ReadObj()
		h = histfile.Get(kname)
		h.Write()

NewFile.Close()
#=====Adjust these to fit isabelles data =====
names = ["pptt","ppWj","ppWW","ppWZ","ppZj","ppZZ"]
length = len(names)
processes = ["ttbar","Wjets","WW","WZ","Zjets", "ZZ"]
for i in range(length):
	name = names[i]
	process = processes[i]
	directory= str("~/Programs/MadGraph/bin/"+ name +"/Events/run_01/tag_1_delphes_events.root")
	x = RootReading(directory, TreeNames, BranchName, LeafNamex) #Defined function at the beginning of script 
	y = TreeLeaves(directory, TreeNames, LeafNamey)	      #Defined function at the beginning of script
	Jet1 = JetFilter(x,y,0) #<----
	ETJ0 = Jet1.JetCut
	ETRemain = Jet1.JetRemain
	HistoJet ( "jets", process,ETRemain, SaveHistROOT )
	HistoJet ( "jets0", process, ETJ0, SaveHistROOT )
