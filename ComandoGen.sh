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
DelphesFCPT=$9
MadShellDir=${10}
#======================================#
E=50000
NumberOfProcess=8
run=$((NumberOfProcess+1))
initial=("$worker" "EFT" "p = g u u~ c c~ d d~ s s~ b b~" "p p > t t~ QED=2 @4; p p > W- j QED=2 @4; p p > W+ W- QED=2 @4; p p > W- Z QED=2 @4; p p > Z j QED=2 @4; p p > Z Z QED=2 @4; p p > W- t QED=2 @4; p p > ta+ mu- QED=2 @4;" "pptt; ppWj; ppWW; ppWZ; ppZj; ppZZ; ppWt; pptamu;" "y" "2" "p p > W+ j;" "4" "p p > W+ Z;" "$run" "y")
EventsInProcess=("" "$E" "$E" "$E" "$E" "$E" "$E" "$E" "$E")
inside=("3" "1" "$Beam1" "2" "$Beam2" "3" "1" "2" "2" "6" "4" "y" "90900" "2")
ProcessNames=("pptt" "ppWj" "ppWW" "ppWZ" "ppZj" "ppZZ" "ppWt" "pptamu")
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
		echo "5" >> $ComandGen
	done
	echo "$run" >> $ComandGen
	echo "w:$worker number:$x , dir:$ComandGen Time: $(date)"
	bash $MadShellDir < $ComandGen 
	#====Copying the data to a different location====#
	for copy in "${ProcessNames[@]}";
	do 
		mkdir $SimulationName/$worker > /dev/null 2>&1
		echo "Copying $copy"
		DelphesROOT=$CommandsDir/bin/$copy/Events/run_01/tag_1_delphes_events.root
		destination=$SimulationName/$worker/Delphes_Event$copy$worker$x.root
		mv $DelphesROOT $destination
	done
	dir=$HOME/MadGraphShell/SimulationData/13000MeV/$worker/*
	bash $Collection "$dir" "$DelphesFCPT" "$Output" 
done