#!/bin/sh
#!/bin/bash
#!/bin/ipython
#============Generator text===================#
initial=("1" "p p > t t~; p p > W- j; p p > W+ W-; p p > W- Z; p p > Z j; p p > Z Z;" "pptt; ppWj; ppWW; ppWZ; ppZj; ppZZ;" "y" "2" "p p > W+ j;" "4" "p p > W+ Z;" "7" "y")
EventsInProcess=("" "10000" "10000" "10000" "10000" "10000" "10000")
NumberOfProcess=6
inside=("3" "1" "6500" "2" "6500" "3" "1" "2" "2" "6" "2")

cd ~/Programs/HistFitter/
source setup.sh
cd ~/MadShell/
mkdir Plots
iterations=1
for ((x=1; x<= $iterations; x++));
do
	rm ~/Commands.txt
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
		processevent="${EventsInProcess[$t]}"
		echo "$processevent" >> Commands.txt  
		echo "8" >> Commands.txt
	done
	echo "7" >> Commands.txt
	bash MadShell.sh < Commands.txt
	sleep 5
	python DelphesReader.py 
	HistFitter.py -w -f -D "before,after" /home/tnom6927/MadShell/Data/MyOneBinExample_6Tom.py >> HistFitterLog.txt
	cd ~/MadShell/results/Results
	mv can_jets0_met_afterFit.pdf ~/MadShell/Plots/can_jets0_met_afterFit.pdf
	mv can_jets0_met_beforeFit.pdf ~/MadShell/Plots/can_jets0_met_beforeFit.pdf
	mv can_jets_met_afterFit.pdf ~/MadShell/Plots/can_jets_met_afterFit.pdf
	mv can_jets_met_beforeFit.pdf ~/MadShell/Plots/can_jets_met_beforeFit.pdf
	cd ~/MadShell
	rm -rf results data config Commands.txt
done
python Extractor.py
