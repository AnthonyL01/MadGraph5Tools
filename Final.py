from ROOT import TCanvas, TPad, TFormula, TF1, TPaveLabel, TH1F, TH2F, TFile
from ROOT import gROOT, gBenchmark

wilson = "0.000001"
RootName = str("SM"+wilson+".root")
Output = str("WithoutEFT"+wilson+".root")

#============scales

f = TFile(str("~/MadGraphShell/PostAnalysis/FinalStep/"+RootName))
New = TFile(str("~/MadGraphShell/PostAnalysis/FinalStep/"+Output),"RECREATE")


vain0 = TH1F("hData_jets0_obs_met","hData_jets0_obs_met",20,0,200)
vain = TH1F("hData_jets_obs_met","hData_jets_obs_met",20,0,200)

jet = str("jets")
jet0 = str("jets0")

t=0
t0=0
z = 0
x = 0
y = 0
Process = ("ttbar","WW","WZ","Wjets","Wt","ZZ","Zjets")
Scale = [0.212957274, 0.033380255, 0.012201975, 15.9059762, 0.012661892, 0.004723519, 5.063108637]
for i in Process:
	ttbarScale=Scale[z]
	process = i
	ttbar = f.Get(str("h"+process+"Nom_"+jet+"_obs_met"))
	ttbar0 = f.Get(str("h"+process+"Nom_"+jet0+"_obs_met"))
	ttbar.Scale(ttbarScale)
	ttbar0.Scale(ttbarScale)
	addtt = TH1F(str("h"+process+"Nom_"+jet+"_obs_met"),str("h"+process+"Nom_"+jet+"_obs_met"),20,0,200)
	addtt0 = TH1F(str("h"+process+"Nom_"+jet0+"_obs_met"),str("h"+process+"Nom_"+jet0+"_obs_met"),20,0,200)
	vain.Add(ttbar)
	vain0.Add(ttbar0)
	ttbar.Sumw2()
	ttbar0.Sumw2()
	t = ttbar.Integral()
	t0 = ttbar0.Integral()
	addtt.Add(ttbar)
	addtt0.Add(ttbar0)
	ttbar.Write()
	ttbar0.Write()
	x = x + t
	y = y + t0
	z = z+1
	print(x)
	print(y)

ttbarScale=0.00002273755556
process = "tamu"
ttbar = f.Get(str("h"+process+"Nom_"+jet+"_obs_met"))
ttbar0 = f.Get(str("h"+process+"Nom_"+jet0+"_obs_met"))
ttbar.Scale(ttbarScale)
ttbar0.Scale(ttbarScale)
addtt = TH1F(str("h"+process+"Nom_"+jet+"_obs_met"),str("h"+process+"Nom_"+jet+"_obs_met"),20,0,200)
addtt0 = TH1F(str("h"+process+"Nom_"+jet0+"_obs_met"),str("h"+process+"Nom_"+jet0+"_obs_met"),20,0,200)
ttbar.Sumw2()
ttbar0.Sumw2()
addtt.Add(ttbar)
addtt0.Add(ttbar0)
ttbar.Write()
ttbar0.Write()







ttbar = 0
ttbar0 = 0
addtt = 0
addtt0 =0
ttbar0 = TH1F("hData_jets0_obs_met","hData_jets0_obs_met",20,0,200)
ttbar = TH1F("hData_jets_obs_met","hData_jets_obs_met",20,0,200)
ttbar0.FillRandom(vain0, int(y) )
ttbar.FillRandom(vain, int(x) )
ttbar0.Sumw2()
ttbar.Sumw2()

New.Write()
New.Close()



