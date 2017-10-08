#!/bin/bash
directory=$1/* #~/MadShell/SimulationData/Renamed/*
DelphesFCPTMethod=$2 #~/MadShell/DelphesPTmethod.py
Output=$3
z=0
for i in $directory
do
	File=$i
	echo "$File"
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
	if [[ "$RemoveDelph" == "ppWt"* ]];
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
	z=$((z+1))
	echo "$z"
	#Delphes Reader which performs cuts according to PT of electrons muons and jets (see python file)
	python $DelphesFCPTMethod "$File" "$Name" "$Process" "$RemoveDelph" "$Output" &
	if [[ z -eq 8 ]];
	then 
		echo "wait"
		wait
		z=0
	fi
done
exit