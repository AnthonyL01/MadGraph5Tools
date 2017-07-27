import ROOT
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
directory1= str("MadGraph5/bin/pp/Events/run_01/tag_1_delphes_events.root")
x = RootReading(directory1, "Delphes", "MissingET", "MissingET.MET")
y = TreeLeaves(directory1, "Delphes", "Jet_size")
#===== Finding the max and min=======#
max_x = int(max(x))
max_y = int(max(y))
min_x = int(min(x))
min_y = int(min(y))
#====================================#
binsy = int(max_y-min_y)
binsx = int(max_x-min_x)
h2 = ROOT.TH2F("h2", "hello", binsx, min_x , max_x, binsy, min_y, max_y)
length = len(y)
for i in range(length):
	valuey = y[i]
	valuex = x[i]	
	h2.Fill(valuex, valuey)
h2.Draw("lego")