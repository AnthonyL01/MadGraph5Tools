#!/bin/bash
directory1=$HOME/MadGraphShell/PostAnalysis/InsertSamples/*

NewDelphesReader=$HOME/MadGraphShell/PostAnalysis/Parameters.py
output=$HOME/MadGraphShell/PostAnalysis/OutputCuts/
Output=$HOME/MadGraphShell/PostAnalysis/OutputCuts/*
combine=$HOME/MadGraphShell/PostAnalysis/3.sh
z=0
ET=30
ETA=25   #(the format is 25 for 2.5 cuts)

for i in $directory1;
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
	if [[ "$RemoveDelph" == "ppWt"* ]];
	then
		Name="ppWt"
		Process="Wt"
	fi
	if [[ "$RemoveDelph" == "pptamu"* ]];
	then 
		Name="pptamu"
		Process="tamu"
	fi
	z=$((z+1))
	#Delphes Reader which performs cuts according to PT of electrons muons and jets (see python file)
	python $NewDelphesReader "$File" "$Name" "$Process" "$RemoveDelph" "$output" "$ET" "$ETA" &
	if [[ z -eq 14 ]];
	then 
		echo "wait"
		z=0
		wait
	fi
	echo "$File"	
done
wait
bash $combine

for i in $directory1;
do
	rm $i
done

for i in $Output;
do
	rm $i
done





