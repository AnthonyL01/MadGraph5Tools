import ROOT
import sys

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



#for i in Files:
Files = sys.argv[1]
Save = sys.argv[2]
Names = Files.split("#*#")
RemoveWhite= Names.pop(0) #This removes the empty entry in the list

#Opening sorting histnames and root file names 
En = []
Nj = []
for i in Names:
	directory = str(i)
	print(i)
	NJ = TreeLeaves (directory, "NJets" ,"NJets")
	ET = TreeLeaves (directory, "ET" ,"ET")
	for i in range(len(NJ)):
		Jet = NJ[i]
		Energy = ET[i]
		En.append(Energy)
		Nj.append(Jet)
#____________Performing Cuts in the array__________#


#========== ROOT Figures ============#
File = ROOT.TFile(Save,"Update")
max_y = 10
min_y = 0
max_x = 200
min_x = 0
print(max_x, max_y)
process = str(sys.argv[3])
Scale = float(sys.argv[4])
StringOfName = str("h"+process+"Nom_jets_obs_met")
h2 = ROOT.TH2F(StringOfName, StringOfName, 200, 0 , max_x, max_y, 0, max_y)
length = len(En)
for i in range(length):
	valuex = En[i]
	valuey = Nj[i]
	h2.Fill(valuex, valuey)
h2.GetXaxis().SetTitle("ET(GeV)")
h2.GetYaxis().SetTitle("Njet")
h2.GetZaxis().SetTitle("Frequency")
h2.Scale(Scale)
File.Write()
File.Close()
