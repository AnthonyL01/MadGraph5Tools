"""
 **********************************************************************************
 * Project: HistFitter - A ROOT-based package for statistical data analysis       *
 * Package: HistFitter                                                            *
 *                                                                                *
 * Description:                                                                   *
 *      Simple example configuration with input trees                             *
 *                                                                                *
 * Authors:                                                                       *
 *      HistFitter grojets0, CERN, Geneva                                         *
 *                                                                                *
 * Redistribution and use in source and binary forms, with or without             *
 * modification, are permitted according to the terms listed in the file          *
 * LICENSE.                                                                       *
 **********************************************************************************
"""

################################################################
## In principle all you have to setjets0 is defined in this file ##
################################################################

## This configuration performs a simplified version of the "soft lepton" fits documented in ATLAS-CONF-2012-041.
## Only two systematics are considered:
##   -JES (Tree-based) conservatively treated like an MC stat error
##   -Alpgen Kt scale (weight-based)
##
## For the real complete implementation, see: HistFitterUser/MET_jets_leptons/python/MyOneLeptonKtScaleFit_mergerSoftLep.py

from configManager import configMgr
import logger
from ROOT import kBlack,kWhite,kGray,kRed,kPink,kMagenta,kViolet,kBlue,kAzure,kCyan,kTeal,kGreen,kSpring,kYellow,kOrange,kDashed,kSolid,kDotted
from configWriter import fitConfig,Measurement,Channel,Sample
from systematic import Systematic
from math import sqrt

from ROOT import gROOT, TLegend, TLegendEntry, TCanvas
#gROOT.LoadMacro("./macros/AtlasStyle.C")
import ROOT
#ROOT.SetAtlasStyle()

#---------------------------------------------------------------------------------------------
# Some flags for overridding normal execution and telling ROOT to shut jets0... use with caution!
#---------------------------------------------------------------------------------------------
#gROOT.ProcessLine("gErrorIgnoreLevel=10001;")
#configMgr.plotHistos = True

#---------------------------------------
# Flags to control which fit is executed
#---------------------------------------
useStat=True
doValidation=False #use or use not validation regions to check exptrapolation to signal regions

#-------------------------------
# Parameters for hypothesis test
#-------------------------------

#configMgr.doHypoTest=False
configMgr.nTOYs = 5000
configMgr.calculatorType = 0
configMgr.testStatType = 3
configMgr.nPoints = 20

log = logger.Logger("AIDAlog")
log.setLevel(logger.VERBOSE)

#--------------------------------
# Now we start to build the model
#--------------------------------

# Set uncorrelated systematics for bkg and signal (1 +- relative uncertainties)
#ucettbar = Systematic("ucettbar", configMgr.weights, 1.032,0.968, "user","userOverallSys")
#uceww = Systematic("uceww", configMgr.weights, 1.032,0.968, "user","userOverallSys")
#ucezjets = Systematic("ucezjets", configMgr.weights, 1.033,0.967, "user","userOverallSys")

### HISTO SYS ###
#jeteffttbar = Systematic("JETEffectiveNP", None, "JETEffectiveNP","JETEffectiveNP", "weight","histoSys")
#jeteffww = Systematic("JETEffectiveNP", None, "JETEffectiveNP","JETEffectiveNP", "weight","histoSys")
#jeteffzjets = Systematic("JETEffectiveNP", None, "JETEffectiveNP","JETEffectiveNP", "weight","histoSys")

### NORMALISATION SYS ###
normttbar = Systematic("norm", None, 1.5,0.5, "user","userOverallSys")
normww = Systematic("norm", None, 1.5,0.5, "user","userOverallSys")
normzjets = Systematic("norm", None, 1.5,0.5, "user","userOverallSys")
normwz = Systematic("norm", None, 1.5,0.5, "user","userOverallSys")
normzz = Systematic("norm", None, 1.5,0.5, "user","userOverallSys")
normwjets = Systematic("norm", None, 1.5,0.5, "user","userOverallSys")
normwt = Systematic("norm", None, 1.1,0.9, "user","userOverallSys")



# First define HistFactory attributes
configMgr.analysisName = "ttpp"
# Scaling calculated by outputLumi / inputLumi
configMgr.inputLumi = 4.713 # Luminosity of input TTree after weighting
configMgr.outputLumi = 4.713 # Luminosity required for output histograms
configMgr.setLumiUnits("fb-1")

configMgr.histCacheFile = "/home/tnom6927/MadShell/Results/"+configMgr.analysisName+".root"
configMgr.outputFileName = "results/"+configMgr.analysisName+"_Output.root"

# Set the files to read from
bgdFiles = [configMgr.histCacheFile]
configMgr.setFileList(bgdFiles)

# Dictionary of cuts for Tree->hist
configMgr.cutsDict["jets"] = ""
configMgr.cutsDict["jets0"] = ""



#-------------------------------------------
# List of samples and their plotting colours
#-------------------------------------------

wwSample = Sample("WW",kGreen-9)
wzSample = Sample("WZ",kAzure+1)
dataSample = Sample("Data",kBlack)
wjetsSample = Sample("Wjets",kBlue)
wtSample = Sample("Wt",kYellow)
zzSample = Sample("ZZ",kRed)
zjetsSample = Sample("Zjets",kOrange)
ttbarSample = Sample("ttbar",kMagenta)
dataSample.setData()

wwSample.setNormByTheory() 
wzSample.setNormByTheory()
dataSample.setNormByTheory()
wjetsSample.setNormByTheory()
wtSample.setNormByTheory()
zzSample.setNormByTheory()
zjetsSample.setNormByTheory()
ttbarSample.setNormByTheory()

#wtSample.setNormFactor("mu_WT",1.,0.,5.)
wwSample.setNormFactor("mu_WW",1.,0.,5.) 
#wzSample.setNormFactor("mu_Wz",1.,0.,5.)
#dataSample.setNormFactor("mu_data",1.,0.,5.)
#wjetsSample.setNormFactor("mu_wjets",1.,0.,5.)
#zzSample.setNormFactor("mu_ZZ",1.,0.,5.)  
zjetsSample.setNormFactor("mu_zjets",1.,0.,5.)
ttbarSample.setNormFactor("mu_ttbar",1.,0.,5.)

#ttbarSample.addSystematic(jeteffttbar)
#zjetsSample.addSystematic(jeteffww)
#wwSample.addSystematic(jeteffzjets)


ttbarSample.addSystematic(normttbar)
zjetsSample.addSystematic(normzjets)
wwSample.addSystematic(normww)
wzSample.addSystematic(normwz)
#wjetsSample.addSystematic(jeteffww)
zzSample.addSystematic(normzz)
wtSample.addSystematic(normwt)

#**************
# Exclusion fit
#**************

# Fit config instance
exclusionFitConfig = configMgr.addFitConfig("Exclusion")
meas=exclusionFitConfig.addMeasurement(name="NormalMeasurement",lumi=1.0,lumiErr=0.039)
meas.addPOI("mu_SIG")
    
# Samples
exclusionFitConfig.addSamples([wzSample, wjetsSample, wtSample, zzSample,wwSample,dataSample,zjetsSample,ttbarSample])

# Systematics
#exclusionFitConfig.getSample("Data").addSystematic(Nom)
#exclusionFitConfig.getSample("WW").addSystematic(Nom)
#exclusionFitConfig.getSample("WZ").addSystematic(Nom)

    
# Channel
jetsBin = exclusionFitConfig.addChannel("met",["jets"],20,0.0,200.0)
jets0Bin = exclusionFitConfig.addChannel("met",["jets0"],20,0.0,200.0)
exclusionFitConfig.setSignalChannels([jetsBin])  
exclusionFitConfig.setSignalChannels([jets0Bin])  
#exclusionFitConfig.setSignalSample(wtSample)
#exclusionFitConfig.setSignalSample(zzSample)
exclusionFitConfig.setSignalSample(wwSample)
#exclusionFitConfig.setSignalSample(wzSample)
exclusionFitConfig.setSignalSample(dataSample)
#exclusionFitConfig.setSignalSample(wjetsSample)
exclusionFitConfig.setSignalSample(zjetsSample)
exclusionFitConfig.setSignalSample(ttbarSample)
