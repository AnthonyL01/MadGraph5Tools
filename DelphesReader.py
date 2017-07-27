import ROOT
import sys
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

############Program Start##########################

#============Future Input agruments===============#
directory1 = str(sys.argv[1]) 
#directory1= str("MadGraph5/bin/pp/Events/run_01/tag_1_delphes_events.root")
TreeNames = "Delphes"
BranchName = "MissingET"
LeafNamey = "Jet_size"
LeafNamex = "MissingET.MET"
PlotName = "Hello"
Cutx = 0
Cuty = 0
#===========End Future Input arguments============#

x = RootReading(directory1, TreeNames, BranchName, LeafNamex)
y = TreeLeaves(directory1, TreeNames, LeafNamey)

#===== Finding the max and min=======#
max_x = int(max(x))
max_y = int(max(y))
min_x = int(min(x))
min_y = int(min(y))
#====================================#

#========== ROOT Figures ============#
binsy = int(max_y-min_y)
binsx = int(max_x-min_x)

h2 = ROOT.TH2F("Figure", PlotName, binsx, min_x , max_x, binsy, min_y, max_y)
length = len(y)
for i in range(length):
	valuey = y[i]
	valuex = x[i]
	if (Cuty <= valuey) and (Cutx <=valuex):
		Collecty = valuey 
		Collectx = valuex
		h2.Fill(Collectx, Collecty)
h2.GetXaxis().SetTitle(LeafNamex)
h2.GetYaxis().SetTitle(LeafNamey)
h2.GetZaxis().SetTitle("Frequency")
h2.SetStats(1)
h2.Draw("lego20")