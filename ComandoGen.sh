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
E=50000
initial=("$worker" "sm-ckm" "p p > t t~ QED=2 @4; p p > W- j QED=2 @4; p p > W+ W- QED=2 @4; p p > W- Z QED=2 @4; p p > Z j QED=2 @4; p p > Z Z QED=2 @4; p p > W- t QED=2 @4;" "pptt; ppWj; ppWW; ppWZ; ppZj; ppZZ; ppWt;" "y" "2" "p p > W+ j;" "4" "p p > W+ Z;" "8" "y")
EventsInProcess=("" "$E" "$E" "$E" "$E" "$E" "$E" "$E")
NumberOfProcess=7
inside=("3" "1" "$Beam1" "2" "$Beam2" "3" "1" "2" "2" "4" "y" "6" "4" "y" "90900" "2")
ProcessNames=("pptt" "ppWj" "ppWW" "ppWZ" "ppZj" "ppZZ" "ppWt")
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
	echo "8" >> $ComandGen
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
done