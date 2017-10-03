#!/bin/sh
#!/bin/bash
#!/bin/ipython
#============Generator text===================#

#======== Input arguments ============#
worker=$1
Beam1=$2
Beam2=$3
EndIteration=$4
CommandsDir=$5
SimulationName=$6
Collection=$7
Output=$8
DelphesFCPTReader=$9
MadShellDir=${10}
#======================================#

initial=("$worker" "p p > t t~; p p > W- j; p p > W+ W-; p p > W- Z; p p > Z j; p p > Z Z;" "pptt; ppWj; ppWW; ppWZ; ppZj; ppZZ;" "y" "2" "p p > W+ j;" "4" "p p > W+ Z;" "7" "y")
EventsInProcess=("" "50000" "50000" "50000" "50000" "50000" "50000")
NumberOfProcess=6
inside=("3" "1" "$Beam1" "2" "$Beam2" "3" "1" "2" "2" "4" "y" "6" "5" "y" "13000" "2")
ProcessNames=("pptt" "ppWj" "ppWW" "ppWZ" "ppZj" "ppZZ")
for ((x=1; x<= $EndIteration; x++));
do
	ComandGen=$CommandsDir/Commands$worker.txt
	sleep 5
	rm $ComandGen > /dev/null 2>&1
	for command in "${initial[@]}"; #<----- writing the initial script for MadShell
	do
		echo "$command" >> $ComandGen
	done
	for ((t=1; t<= $NumberOfProcess; t++));
	do
		echo "$t" >> $ComandGen
		for z in "${inside[@]}";
		do
			echo "$z" >> $ComandGen
		done
		processevent="${EventsInProcess[$t]}"
		echo "$processevent" >> $ComandGen 
		echo "6" >> $ComandGen
	done
	echo "7" >> $ComandGen
	echo "w:$worker number:$x , dir:$ComandGen Time: $(date)"
	bash $MadShellDir < $ComandGen 
	
	#====Copying the data to a different location====#
	for copy in "${ProcessNames[@]}";
	do 
		mkdir $SimulationName/$worker > /dev/null 2>&1
		echo "Copying $copy"
		DelphesROOT=$CommandsDir/bin/$copy/Events/run_01_decayed_1/tag_1_delphes_events.root
		destination=$SimulationName/$worker/Delphes_Event$copy$worker$x.root
		mv $DelphesROOT $destination
	done
	
	#=====Initiating the Filtering process==========#
	#FileDir=$SimulationName/$worker/*
	#bash $Collection "$FileDir" "$DelphesFCPTReader" "$Output"  
	wait
done
