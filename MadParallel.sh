#!/bin/bash
#This software was developed to make the computation faster and more efficient
read -p "How many workers do you want to run? (enter number) " workers
read -p "Enter the energy scale you want to run at (GeV): " Energy
read -p "Enter the number of iterations of interest (enter number) " Iterations

#Directory Names
MeV=MeV
OutputDir=$HOME/MadGraphShell/SimulationData/$Energy$MeV

#Creating directories
mkdir $HOME/MadGraphShell/Logs 2>&1
mkdir $OutputDir > /dev/null 2>&1
mkdir $OutputDir/processed > /dev/null 2>&1
mkdir $OutputDir/Results 2>&1
OutputFCPT=$OutputDir/processed

rm -rf $HOME/MadGraphShell/Workers/MadGraph* > /dev/null 2>&1
echo "Creating $workers Workers"

for ((x=1; x<= $workers; x++));
do
	mkdir $HOME/MadGraphShell/Workers/MadGraph$x
	cp -rf $HOME/MadGraphShell/Workers/x/* $HOME/MadGraphShell/Workers/MadGraph$x
	cp -rf $HOME/MadGraphShell/Scripts/ComandoGen.sh $HOME/MadGraphShell/Workers/MadGraph$x/ComandoGen.sh
	echo "Created $x/$workers !"
done

#Input arguments for ComandoGen.sh
DelphesFCPT=$HOME/MadGraphShell/Scripts/DelphesFCPTMethod.py
Collection=$HOME/MadGraphShell/Scripts/Collection.sh
MadShellDir=$HOME/MadGraphShell/Scripts/MadShell.sh
MergeMe=$HOME/MadGraphShell/Scripts/MergeMe.sh
MergeROOT=$HOME/MadGraphShell/Scripts/MergeROOT.py

#Some variable change for the next loop
work=$workers
beams=$((Energy/2))
Beam1=$beams
Beam2=$beams
steps=$((Iterations/work))

for ((i=1; i<= $workers; i++));
do
	echo "Worker: $i Time: $(date)"
	Logs=$HOME/MadGraphShell/Logs/MadShellLog$i.txt
	Directory=$HOME/MadGraphShell/Workers/MadGraph$i
	bash $Directory/ComandoGen.sh "$i" "$Beam1" "$Beam2" "$steps" "$Directory" "$OutputDir" "$Collection" "$OutputFCPT" "$DelphesFCPT"  "$MadShellDir" & >> $Logs
	
done
echo "Completed all runs!"
wait
for ((i=1; i<= $workers; i++));
do
	dir=$HOME/MadGraphShell/SimulationData/$Energy$MeV/$i
	bash $Collection "$dir" "$DelphesFCPT" "$OutputFCPT" 
done
wait
echo "Completed Cuts!"
output2=$OutputFCPT/*
dest=$OutputDir/Results
bash $MergeMe "$output2" "$MergeROOT" "$dest"
exit