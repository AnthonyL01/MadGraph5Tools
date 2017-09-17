#!/bin/bash
#This software was developed to make the computation faster and more efficient
read -p "How many workers do you want to run? (enter number) " workers
read -p "Enter the energy scale you want to run at (GeV): " Energy
read -p "Enter the number of iterations of interest (enter number) " Iterations

MuonPT=25
ElectronPT=20
JetPT=25

#Directory Names
MeV=MeV
OutputDir=$PWD/SimulationData/$Energy$MeV
FLC=$PWD/FCMethod
PT=$PWD/PTMethod

#Creating directories
mkdir $FLC > /dev/null 2>&1
mkdir $PT > /dev/null 2>&1
mkdir $PWD/Logs
mkdir $OutputDir > /dev/null 2>&1
mkdir $OutputDir/processed > /dev/null 2>&1


rm -rf $PWD/Workers/MadGraph* > /dev/null 2>&1
echo "Creating $workers Workers"

for ((x=1; x<= $workers; x++));
do
	mkdir $PWD/Workers/MadGraph$x
	cp -rf $PWD/Workers/x/* $PWD/Workers/MadGraph$x
	cp -rf $PWD/Scripts/ComandoGen.sh $PWD/Workers/MadGraph$x/ComandoGen.sh
	echo "Created $x/$workers !"
done

#Input arguments for ComandoGen.sh
DelphesFC=$PWD/Scripts/DelphesFCmethod.py
DelphesPT=$PWD/Scripts/DelphesPTmethod.py
Collection=$PWD/Scripts/Collection.sh
MadShellDir=$PWD/Scripts/MadShell.sh

#Some variable change for the next loop
work=$workers
beams=$((Energy/2))
Beam1=$beams
Beam2=$beams
steps=$((Iterations/work))


for ((i=1; i<= $workers; i++));
do
	echo "Worker: $i Time: $(date)"
	Logs=$PWD/Logs/MadShellLog$i.txt
	Directory=$PWD/Workers/MadGraph$i
	bash $Directory/ComandoGen.sh "$i" "$Beam1" "$Beam2" "$steps" "$Directory" "$OutputDir" "$Collection" "$DelphesPT" "$DelphesFC" "$FLC" "$PT" "$MadShellDir" "$MuonPT" "$ElectronPT" "$JetPT" >> $Logs &
done
wait

echo "Completed all runs!"