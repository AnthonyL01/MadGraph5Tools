#!/bin/bash
directory=$1 #~/MadShell/SimulationData/Renamed/*
DelphesFCPTMethod=$2 #~/MadShell/DelphesPTmethod.py
Output=$3


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
	if [[ "$RemoveDelph" == "ppWt" ]];
	then 
		Name="ppWt"
		Process="Wt"
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

	NewRemoveDelph="$RemoveDelph"
	#Delphes Reader which performs cuts according to PT of electrons muons and jets (see python file)
	python $DelphesFCPTMethod "$File" "$Name" "$Process" "$NewRemoveDelph" "$OutputDir" 
done