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



directory1= str("MadGraph5/bin/pp/Events/run_01/tag_1_delphes_events.root")
x = RootReading(directory1, "Delphes" , "Jet", "Jet.Eta")
y = RootReading(directory1, "Delphes", "Jet", "Jet.PT")
#===== Finding the max and min=======#
max_x = int(max(x))
max_y = int(max(y))
min_x = int(min(x))
min_y = int(min(y))
#====================================#

h2 = ROOT.TH2F("h2", "hello", 100, min_x , max_x, 100, min_y, max_y)
length = len(y)
for i in range(length):
	valuey = y[i]
	valuex = x[i]	
	h2.Fill(valuex, valuey)
h2.Draw("lego1")