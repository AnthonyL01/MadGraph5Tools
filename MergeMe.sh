#!/bin/bash
directoryFiles=$1 #~/MadShell/Results/FCMethod/*
MergeROOT=$2
dest=$3
for i in $directoryFiles;
do
	string="$string#*#$i"	
done
python $MergeROOT "$string" "$dest"