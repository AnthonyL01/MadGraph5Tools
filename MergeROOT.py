import ROOT
import sys

#This function merges root files with Histograms
def CombinedROOT(Files, NameJet, NameJet0):
	Combined = ROOT.TFile.Open("~/Merged.root","UPDATE")
	j = str(NameJet)
	j0 = str(NameJet0)
	jet = ROOT.TH1F(j,"",0,0,0)
	jet0 = ROOT.TH1F(j0,"",0,0,0) 
	for i in range(len(Files)):
		names = str(Files[i]).strip("[").strip("]")
		string = str(names)
		name = str("ROOT.TFile.Open("+string+","+"'Read'"+")")
		execute = eval(name)
		proJets = str(NameJet)
		proJets0 = str(NameJet0)
		jets = execute.Get(proJets)
		jets0 = execute.Get(proJets0)
		jet.Add(jets)
		jet0.Add(jets0)
		del jets
		del jets0
	Combined.Write()
	Combined.Close()
	return

#Files = ["CUTSpptt1.root","CUTSpptt10.root","CUTSpptt11.root"]
#

#for i in Files:
Files = sys.argv[1]
Names = Files.split("#*#")
RemoveWhite= Names.pop(0) #This removes the empty entry in the list

#Opening sorting histnames and root file names 
HistNames = []
for i in Names:
	rootFile = ROOT.TFile.Open(i,"Read")
	Hist = rootFile.GetListOfKeys()
	temp = []
	for entry in Hist:
		HistoName = entry.GetName()
		temp.append(HistoName)
	Collect = [i,temp[0],temp[1]]
	HistNames.append(Collect)

HistNames.sort(reverse = True)

unique = []
unique0 = []
for i in range(len(HistNames)):
	process = HistNames[i][1]
	process0 = HistNames[i][2]
	if process not in unique:
		unique.append(process)
		unique0.append(process0)

Target = []
for i in range(len(HistNames)):
	process = HistNames[i][1]
	Directory = HistNames[i][0]
	process0 = HistNames[i][2]
	for x in range(len(unique)):
		if (process == unique[x]):
			Collect = [Directory, process, process0,x,i]
			Target.append(Collect)

for i in range(len(unique)):
	run = []
	for x in range(len(Target)):
		cutting = Target[x][3]
		directory = Target[x][0]
		processes = Target[x][1]
		processes0 = Target[x][2]
		if ( i == cutting ):
			temp = [directory]
			run.append(temp)
	string = str(unique[i])
	string0 = str(unique0[i])
	CombinedROOT(run,string,string0)