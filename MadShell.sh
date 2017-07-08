#!/bin/sh
#!/bin/bash
#!/bin/ipython
#This shell script is used to run MadGraph 5 commands and events:
#==========================Setting the directory of MadGraph 5=========================#

#Finding the directories which have MadGraph 5
MadGraph=($(find ~/ -name "mg5_aMC" ))

#Waiting for user input which directory is correct
echo "Please select MadGraph 5 directory:"
select dir in "${MadGraph[@]}";
do
	[ -n "${dir}" ] && break
done

#Extract the directory and change to it!
directory="$(dirname $dir)/"
cd $directory

#============We now generate the config file for MadGraph 5:======================#
echo "Entering Configuration Mode:"

#_____________Generating arrays containing processes_____________
# the variables "i" and "t" are temp variables and will be cleared after each section
continue="no"
while [ "no" == $continue ];
do
	#_____________Process to run__________________________________#
	read -p "Enter the processes to be generated (ending with ';'): " input
	splitter=($(echo $input | fold -w1))
	generate=()
	for i in ${splitter[@]};
	do 	
		if [[ "$i" = ";" ]];
		then				
			generate+=("$t") 
			t=""
		else	
			t="$t$i"
		fi
	done 
	echo "${generate[@]}"
	
	unset i #Clearing variable
	unset t	#Clearing variable 
	unset splitter
	
	#__________This is to get the names in code of the entered process___________#
	splitter=($(echo $input | sed -e "s/;/#/g" | sed -e "s/ /!/g" | fold -w1))
	coding=()
	for i in ${splitter[@]};
	do 	
		if [[ "$i" = "#" ]];
		then				
			coding+=("$t") 
			t=""
		else	
			t="$t$i"
		fi
	done 	
	unset i #Clearing variable
	unset t	#Clearing variable 
	unset splitter
	
	#_____________Giving names to each run___________________________
	read -p "Enter the name of output (ending with ';'): " names
	splitter=($(echo $names | fold -w1))
	Names=()
	for i in ${splitter[@]};
	do 	
		if [[ "$i" = ";" ]];
		then				
			Names+=("$t") 
			t=""
		else	
			t="$t$i"
		fi
	done 
	echo "${Names[@]}"
	
	unset i #Clearing variable
	unset t	#Clearing variable 
	unset splitter

	#This will ensure that for each process there is a name present
	if [[ ${#Names[@]} == ${#generate[@]} ]]; then
		echo -e "\e[1;32m You are ready to continue! \e[0m"
		continue="yes"
	else 
		echo -e "\e[1;31m Please give for each process a name! \e[0m"
	fi	
done

#==========Menu for adding in subprocesses=============# 
read -p "Would you like to add a sub process? (y/n) " answer
if [[ "$answer" == "y" ]]; 
then 
	echo "Please select one of the following:"
	generate+=("finished")
	continue="false"
	while [[ "$continue" == "false" ]]; do
		select add in "${generate[@]}";
		do
				[ -n ${add} ] && break
		done
		#_______________Finding index of add in generate____________________#
		for i in "${!generate[@]}";
		do
			if [[ "${generate[$i]}" == "${add}" ]];
			then
				front=${coding[$i]}
				NameOfOutput=${Names[$i]}
			fi
		done
		#__________________Exiting___________________________________________#
		if [[ "$add" == "finished" ]];
		then
			break
		fi		
		echo "You have selected $add"
		read -p "Enter the subprocess to be added (ending with ';'): " Subinput
		#______________Storing and Confirming________________________#
		subcode=($(echo $Subinput | sed -e "s/;/#/g" | sed -e "s/ /!/g" | fold -w1))
		subprocess=()
		for decode in ${subcode[@]};
		do 	
			if [[ "$decode" = "#" ]];
			then				
				subprocess+=("$temp") 
				temp=""
			else	
				temp="$temp$decode"
			fi
		done 
		Message="You have added: \e[1;32m${subprocess[@]}\e[0m to $add"
		echo -e ${Message[@]} | tr "!" " " 
		unset decode 	#Clearing variable
		unset Subinput	#Clearing variable 
		unset subcode	#Clearing variable
		unset temp	#Clearing variable
		unset Message	#Clearing variable
	
		#=======Generating the MadShell config===================#
		MG5Gen="generate $front" #This is the instruction to generate process.
		echo $MG5Gen | tr "!" " " >> MadShell #Creates the file
		for subcode in "${subprocess[@]}";
		do
			Message="add process $subcode"
			echo $Message | tr "!" " " >> MadShell	#Creates the file
		done
		echo "output $NameOfOutput" >> MadShell #Creates the file
	done
elif [[ "$answer" == "n" ]];
then
	for i in "${!generate[@]}";
	do
		front="generate ${coding[$i]}"
		echo  $front | tr "!" " ">>MadShell
		NameOfOutput=${Names[$i]}
		echo "output $NameOfOutput">>MadShell
	done
fi
echo "exit">>MadShell
#============= Actually creating Directories ===================#
echo "Generating the Files and directories by conducting a test run!"
python mg5_aMC MadShell
rm MadShell

#=======================removing variables=======================# 
unset name
unset del
unset delimit
unset answer 
unset MG5Gen
unset subcode
unset NameOfOutput
unset front
unset Message
unset i 

########################################################################################
########################################################################################
#############				################################################
#############	 Useful variables	################################################
#############				################################################
#======================================================================================#
# $directory = MadGraph5 bin directory   					       #
# ${generate[@]} = The entered Processes in string form with no whitespace!            #
# ${Names[@]} = This gives the process names    				       #
# ${coding[@]} = The generate string parsed using a code # = new element != Space      #
# ${subprocess[@]} = Added extra processes in code 				       #
#======================================================================================#
########################################################################################
########################################################################################

#================Entering the options menu for tweaking============================#
#==================================================================================#
#Declaring variables
Pythia=()
Evnts=()
BeamEV1=()
BeamEV2=()
Import_model=()
NumberOfRuns=1
BackedDir=()
#Standard Settings for MadGraph5 
Import_model="!" 
Pythia="no"
SimDetector="Off"
Weight="no"
MadSpin="no"

#Adding a finish option to menu
selections=("Pythia/Detector" "Edit Number of Events" "Edit Beam Energy" "Model to Import" "Number of Runs" "Finished")

#User interaction point
read -p "Would you like to edit these processes? (y/n): " options
if [ "$options" == "y" ];
then 
generate+=("Finished")
	#This level enables user to chose the process to edit 
	running="false" #Keeping the loop running for the options menu
	while [ "$running" == "false" ]; 
	do 
		#Submenu with selections options 
		suboptions="incomplete"
		echo "Chose the process which you would like to edit:"
		select process in "${generate[@]}";
		do
			[ -n "${process}" ] && break
		done
		if [ "$process" == "Finished" ]; 
		then 	
			for name in "${Names[@]}";
			do			
				place=$directory$name/Cards/MadShell	
				if [[ -f "$place" ]];			
				then			
					continue
				else	
					cd $directory$name/Cards/				
					second="launch $name"	      #Launches the output name generated from the start
					echo "$second" >> MadShell
					echo "done" >> MadShell
					echo "done" >> MadShell
					cd $directory
				fi
				
			done	
			unset Evnts
			unset BeamEV1
			unset BeamEV2
			unset NumberOfRuns
			running="true" && break	
		fi

		#Searching the generate array for index of process selected 
		for i in "${!generate[@]}";
		do 
			if [[ "${generate[$i]}" = "${process}" ]]; 	
			then
				Name=${Names[$i]}
			fi
		done	

		#Changing to the run_card.dat file directory				
		Wanted="$directory$Name"
		cd "$Wanted"
		File=$(find . -name "run_card.dat" )
		cd "$(dirname $File)/"

		echo "Chose one of the options below"
		while [ "$suboptions" == "incomplete" ];
		do
			echo -e "You have chosen; Process: \e[1;32m"$process"\e[0m""\e[0m, Number of Events: \e[1;32m"$Evnts"\e[0m, Beam Energy, 1: \e[1;32m"$BeamEV1"\e[0m 2: \e[1;32m"$BeamEV2"\e[0m, Model: \e[1;32m"$Import_model"\e[0m, Number of Runs: \e[1;32m"$NumberOfRuns"\e[0m"  
			select category in "${selections[@]}";
			do
				[ -n "${category}" ] && break
			
			done 
			#====================Exits the submenu====================#
			if [ "$category" == "Finished" ];
			then
				#Writing a config file for MadGraph5 for these particular settings
				#Used Variables: Pythia, SimDetector, MadSpin, Weight, Import_model , NumberOfRuns, Name
				
				for (( i=1; i <= $NumberOfRuns; i++))
				do 	
					rm MadShell #This removes any existing MadShell settings file.
					if [[ "$Import_model" == "!" ]]; then
						Nothing=""
					else
						first="import $Import_model" #Imports models
						echo "$first" >> MadShell     
					fi
					
					second="launch $Name"	      #Launches the output name generated from the start
					echo "$second" >> MadShell
					if [[ "$Pythia" == "yes" ]]; then
						if [[ "$SimDetector" == "PGS" ]]; then 
							echo "2" >> MadShell
						elif [[ "$SimDetector" == "Delphes" ]]; then
							echo "2" >> MadShell
							echo "2" >> MadShell
						elif [[ "$SimDetector" == "Off" ]]; then
							echo "1" >> MadShell
						fi
					
					elif [[ "$Pythia" == "no" ]]; then 
						continue 
					fi
				
					if [[ "$MadSpin" == "yes" ]]; then
						echo "4" >> MadShell
					elif [[ "$MadSpin" == "no" ]]; then 
						continue
					fi
	
					if [[ "$Weight" == "yes" ]]; then
						echo "5" >> MadShell
					elif [[ "$Weight" == "no" ]]; then 
						continue					
					fi
					echo "done" >> MadShell
					echo "done" >> MadShell
				done
				echo "exit" >> MadShell
				suboptions="complete"
			
			#Enters Pythia/Detector settings
			elif [ "$category" == "Pythia/Detector" ];
			then 	
				Launching=("Shower/Hadronization" "Detector Simulation" "Decay with MadSpin" "Add weights to events for different model hypothesis" "Back")
				PythiaDetector="True"
				while [[ "$PythiaDetector" == "True" ]]; 
				do
					select Sim in "${Launching[@]}";
					do
						[ -n "${Sim}" ] && break
					done 		
					if [[ "$Sim" == "Shower/Hadronization" ]];
					then 
						read -p "Enable Showering/Hadronization using Pythia6? (y/n) " SimPy
						if [[ "$SimPy" == "y" ]]; then
							Pythia="yes"
						elif [[ "$SimPy" == "n" ]]; then
							Pythia="no"
						fi
					elif [[ "$Sim" == "Detector Simulation" ]];
					then 
						echo "By enabling detector simulations you also activate Pythia!"
						Detec=("PGS" "Delphes" "Off")
						select DetecSim in "${Detec[@]}";
						do
							[ -n "${DetecSim}" ] && break
						done 		
						if [[ "$DetecSim" == "PGS" ]]; then
							Pythia="yes"
							SimDetector="PGS"
						elif [[ "$DetecSim" == "Off" ]]; then
							Pythia="no"
						elif [[ "$DetecSim" == "Delphes" ]]; then
							Pythia="yes"
							SimDetector="Delphes"
						fi
					elif [[ "$Sim" == "Decay with MadSpin" ]];
					then 
						read -p "Decay with MadSpin? (y/n) " MadAns
						if [[ "$MadAns" == "y" ]]; then
							MadSpin="yes"
						elif [[ "$MadAns" == "n" ]]; then
							MadSpin="no"
						fi
	
					elif [[ "$Sim" == "Add weights to events for different model hypothesis" ]];
					then 
						read -p "Add Weights? (y/n) " WeighANS
						if [[ "$WeighANS" == "y" ]]; then
							Weight="yes"
						elif [[ "$WeighANS" == "n" ]]; then
							Weight="no"
						fi
					elif [[ "$Sim" == "Back" ]];
					then
						echo "Weight: $Weight MadSpin: $MadSpin Detector: $SimDetector Pythia: $Pythia"
						sleep 3
						PythiaDetector="false"
					fi
				done




			#Enters Number of Events 
			elif [ "$category" == "Edit Number of Events" ];
			then 		
				unset i
				unset Card	

				#Changing the settings in the .dat file using the sed -i (interactive command)				
				Card=run_card.dat
				read -p "Enter the number of events which are to be generated: " Evnts
				sed -i "/nevents/c\ "$Evnts" = nevents ! Number of unweighted events requested" $Card

			#Enters Edit Beam Energy
			elif [ "$category" == "Edit Beam Energy" ];
			then 
				unset i		#Cleaning Variables 
				unset Card
				unset Name
				unset Wanted

				BeamLOOP="true"
				Beams=("Beam1" "Beam2" "Finished")
				
				#=============Adding Beam menu====================#
				while [[ "$BeamLOOP" == "true" ]]; 
				do
					select object in "${Beams[@]}";
					do
						[ -n "${object}" ] && break
					done

					if [[ "$object" == "Finished" ]];
					then
						BeamLOOP="false" 	#Breaking the loop conditions return to previous 
					#============Beam 1==============
					elif [[ "$object" == "Beam1" ]];
					then
						unset i
						unset Card
	
						#Changing the settings in the .dat file using the sed -i (interactive command)				
						Card=run_card.dat
						read -p "Enter the energy of Beam 1 (GeV): " BeamEV1
						sed -i "/ebeam1/c\     "$BeamEV1"     = ebeam1  ! beam 1 total energy in GeV" $Card
					#===========Beam 2===============
					elif [[ "$object" == "Beam2" ]];
					then 

						unset i
						unset Card
						unset Name
						unset Wanted	
	
						#Changing the settings in the .dat file using the sed -i (interactive command)				
						Card=run_card.dat
						read -p "Enter the energy of Beam 2 (GeV): " BeamEV2
						sed -i "/ebeam2/c\     "$BeamEV2"     = ebeam2  ! beam 2 total energy in GeV" $Card
					fi
				done
			#Enters Model to Import
			elif [ "$category" == "Model to Import" ];
			then 
				echo "!!!!!!!!!!!Make sure you READ MadGraph5 instructions!!!!!!!!!!!!!!!!!!"
				read -p "Please write the model you would like to import (e.g. MSSM...): " Import_model

			#Enters Number of Runs 
			elif [ "$category" == "Number of Runs" ];
			then 
				read -p "How many runs would you like to conduct? " NumberOfRuns
			fi
		done

	done
elif [[ "$options" == "n" ]]; then 
	cd $directory
	for name in "${Names[@]}";
	do			
		second="launch $name"	      #Launches the output name generated from the start
		echo "$second" >> MadShell
		echo "done" >> MadShell
		echo "done" >> MadShell
	done	
	python mg5_aMC MadShell	
fi 

#This will be the method used to execute the saved MadShell file for each directory in names 
if [[ "$options" == "y" ]];
then 
	cd $directory
	File=$(find $directory -name "MadShell" )
	for path in "${File[@]}";
	do 
		#python mg5_aMC "$path"
		echo "$path"
		echo "Time: $(date)"
		wait
	done
fi