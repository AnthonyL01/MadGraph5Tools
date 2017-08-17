#!/bin/sh
#!/bin/bash
#!/bin/ipython
#============Generator text===================#
initial=("1" "p p > t t~; p p > W- j; p p > W+ W-; p p > W- Z; p p > Z j; p p > Z Z;" "pptt; ppWj; ppWW; ppWZ; ppZj; ppZZ;" "y" "2" "p p > W+ j;" "4" "p p > W+ Z;" "7" "y")
NumberOfProcess=6
inside=("1" "2" "2" "6" "2")

cd ~/Programs/HistFitter/
source setup.sh
cd ~/MadShell/

i=0
steps=1000
iterations=50
for ((x=1; x<= $iterations; x++));
do
	rm ~/Commands.txt
	i=$((i+ $steps)) #<---- number of events
	for command in "${initial[@]}"; #<----- writing the initial script for MadShell
	do
		echo "$command" >> Commands.txt
	done
	for ((t=1; t<= $NumberOfProcess; t++));
	do
		echo "$t" >> Commands.txt
		for z in "${inside[@]}";
		do
			echo "$z" >> Commands.txt
		done
		echo "$i" >> Commands.txt
		echo "8" >> Commands.txt
	done
	echo "7" >> Commands.txt
	bash MadShell.sh < Commands.txt
	sleep 5
	python DelphesReader.py 
	HistFitter.py -w -f -D "before,after" /home/tnom6927/MadShell/Data/MyOneBinExample_6Tom.py >> logFile.txt
	mkdir Plots
	cd ~/MadShell/results/Results
	mv can_jets0_met_afterFit.pdf ~/MadShell/Plots/can_jets0_met_afterFit$i.pdf
	mv can_jets0_met_beforeFit.pdf ~/MadShell/Plots/can_jets0_met_beforeFit$i.pdf
	mv can_jets_met_afterFit.pdf ~/MadShell/Plots/can_jets_met_afterFit$i.pdf
	mv can_jets_met_beforeFit.pdf ~/MadShell/Plots/can_jets_met_beforeFit$i.pdf
	cd ~/MadShell
	rm -rf results data config Commands.txt
done
