from ROOT import TCanvas, TPad, TFormula, TF1, TPaveLabel, TH1F, TH2F, TFile
from ROOT import gROOT, gBenchmark

coef = "0.000001"
RootName = str("3Dnormal.root")
Output = str("Wilson"+coef+".root")
f = TFile(str("~/Test/"+RootName))
New = TFile(str("~/Test/"+Output),"UPDATE")


vain = TH2F("hData_jets_obs_met","hData_jets_obs_met",200,0,200,10,0,10)

jet = str("jets")
jet0 = str("jets0")


ttbarScale=0.207034712
process = str("ttbar")
ttbar = f.Get(str("h"+process+"Nom_"+jet+"_obs_met"))
addtt = TH2F(str("h"+process+"Nom_"+jet+"_obs_met"),str("h"+process+"Nom_"+jet+"_obs_met"),200,0,200,10,0,10)
addtt.Add(ttbar,1)
vain.Add(ttbar)

WWScale=0.033652478
process = str("WW")
WW = f.Get(str("h"+process+"Nom_"+jet+"_obs_met"))
addWW = TH2F(str("h"+process+"Nom_"+jet+"_obs_met"),str("h"+process+"Nom_"+jet+"_obs_met"),200,0,200,10,0,10)
addWW.Add(WW)
vain.Add(WW)

WZScale=0.01257439
process = str("WZ")
WZ = f.Get(str("h"+process+"Nom_"+jet+"_obs_met"))
addWZ = TH2F(str("h"+process+"Nom_"+jet+"_obs_met"),str("h"+process+"Nom_"+jet+"_obs_met"),200,0,200,10,0,10)
addWZ.Add(WZ)
vain.Add(WZ)

WjetsScale=15.87025265
process = str("Wjets")
Wjets = f.Get(str("h"+process+"Nom_"+jet+"_obs_met"))
addWjets = TH2F(str("h"+process+"Nom_"+jet+"_obs_met"),str("h"+process+"Nom_"+jet+"_obs_met"),200,0,200,10,0,10)

WtScale = 0.012559445
process = str("Wt")
Wt = f.Get(str("h"+process+"Nom_"+jet+"_obs_met"))
addWt = TH2F(str("h"+process+"Nom_"+jet+"_obs_met"),str("h"+process+"Nom_"+jet+"_obs_met"),200,0,200,10,0,10)
addWt.Add(Wt)
vain.Add(Wt)

ZZScale = 0.004971319
process = str("ZZ")
ZZ = f.Get(str("h"+process+"Nom_"+jet+"_obs_met"))
addZZ = TH2F(str("h"+process+"Nom_"+jet+"_obs_met"),str("h"+process+"Nom_"+jet+"_obs_met"),200,0,200,10,0,10)
addZZ.Add(ZZ)
vain.Add(ZZ)

ZjetsScale = 5.160395977
process = str("Zjets")
Zjets = f.Get(str("h"+process+"Nom_"+jet+"_obs_met"))
addZjets = TH2F(str("h"+process+"Nom_"+jet+"_obs_met"),str("h"+process+"Nom_"+jet+"_obs_met"),200,0,200,10,0,10)


process = str("tamu"+coef)
tamu = f.Get(str("h"+process+"Nom_"+jet+"_obs_met"))
addtamu = TH2F(str("h"+process+"Nom_"+jet+"_obs_met"),str("h"+process+"Nom_"+jet+"_obs_met"),200,0,200,10,0,10)
addtamu.Add(tamu)
vain.Add(tamu)

#h1f0 = TH2F("hData_jets0_obs_met","hData_jets0_obs_met",200,0,200,10,0,10)
#h1f = TH2F("hData_jets_obs_met","hData_jets_obs_met",200,0,200,10,0,10)
#h1f0.FillRandom(vain0, 118621 )
#h1f.FillRandom(vain, 135316 )

New.Write()
New.Close()



