#!/bin/bash
directory=$1 #~/MadShell/SimulationData/Renamed/*
NewDelphesReader=$2 #~/MadShell/DelphesPTmethod.py
DelphesReader=$3 #~/MadShell/DelphesReader.py
FC=$4
PT=$5
MuonPT=$6
ElectronPT=$7
JetPT=$8
for i in $directory
do
	File=$i
	FileName=${i##*/}
	RemoveDelph=${FileName#*Delphes_Event}
	if [[ "$RemoveDelph" == "pptt"* ]];
	then
		Name="pptt"
		Process="ttbar"
	fi
	if [[ "$RemoveDelph" == "ppWW"* ]];
	then
		Name="ppWW"
		Process="WW"
	fi
	if [[ "$RemoveDelph" == "ppWj"* ]];
	then
		Name="ppWj"
		Process="Wjets"
	fi
	if [[ "$RemoveDelph" == "ppWZ"* ]];
	then
		Name="ppWZ"
		Process="WZ"
	fi
	if [[ "$RemoveDelph" == "ppZj"* ]];
	then
		Name="ppZj"
		Process="Zjets"
	fi
	if [[ "$RemoveDelph" == "ppZZ"* ]];
	then
		Name="ppZZ"
		Process="ZZ"
	fi
	#Delphes Reader which finds the dilepton events with opposite flavor and charge 
	python $DelphesReader "$File" "$Name" "$Process" "$RemoveDelph" "$FC" &

	sleep 10
	NewRemoveDelph="CUTS$RemoveDelph"
	#Delphes Reader which performs cuts according to PT of electrons muons and jets (see python file)
	python $NewDelphesReader "$File" "$Name" "$Process" "$NewRemoveDelph" "$PT" "$MuonPT" "$ElectronPT" "$JetPT" &
done