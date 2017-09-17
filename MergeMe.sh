#!/bin/bash
directoryFiles=~/MadShell/Results/FCMethod/*
for i in $directoryFiles;
do
	string="$string#*#$i"	
done
python MergeROOT.py $string