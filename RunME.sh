#!/bin/bash
directoryFiles=("pptt" "ppWj" "ppWt" "ppWW" "ppWZ" "ppZj" "ppZZ" "C0_1" "C0_01" "C0_001" "C0_0001" "C0_00001" "C0_000001")
names=("ttbar" "Wj" "Wt" "WW" "WZ" "Zj" "ZZ" "tamu0.1" "tamu0.01" "tamu0.001" "tamu0.0001" "tamu0.00001" "tamu0.000001")
scale=("0.212957274" "15.9059762" "0.012661892" "0.033380255" "0.012201975" "5.063108637" "0.004723519" "227375.5556" "2273.755556" "22.73755556" "0.2273755556" "0.002273755556" "0.00002273755556")
MergeROOT=~/Test/AIDA.py
Destination=$HOME/Test/3Dnormal.root
sample=$HOME/Test/Sample/
call=$HOME/Test/Sample/*
Cutter=$HOME/Test/2.sh
out=$HOME/Test/Out/*
echo "$Destination"
v=0
for i in "${directoryFiles[@]}";
do
	name="${names[$v]}"
	lumin="${lumi[$v]}"
	place=$HOME/Test/Done/$i/*
	for x in ${place[@]};
	do
		cp "$x" $sample
	done
	bash $Cutter
	sleep 1
	
	for z in ${out[@]};
	do
		string="$string#*#$z"	
	done
	echo "$string"
	echo "$name"
	echo "$lumin"
	python $MergeROOT "$string" "$Destination" "$name" "$scale"
	unset string
	sleep 1
	
	for y in ${call[@]};
	do
		rm $y
	done
	sleep 1

	for y in ${out[@]};
	do
		rm $y
	done
	sleep 1
	v=$((v+1))
done
