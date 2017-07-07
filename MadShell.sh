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
	#read -p "Enter the processes to be generated (ending with ';'): " input
	input="p p > t t~; p p > u u~ ;" #<-----Remove later!!!!!!!!!!!!!!!!!!!!!!!!
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

	#_____________Giving names to each run___________________________
	#read -p "Enter the name of output (ending with ';'): " names
	names="Test1; Test2;" #< ----------------- Remove later!!!
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

#Menu for adding in subprocesses 
read -p "Would you like to add a sub process? (y/n)" answer
if [[ "$answer" == "y" ]]; 
then 
echo "Please select one of the following:"
	select add in "${generate[@]}";
	do
		[ -n "${add}" ] && break
	done
	echo "You have selected $add"
	read -p "Enter the subprocess to be added (ending with ';'): " Subinput
	input="p p > t t~; p p > u u~ ;" #<-----Remove later!!!!!!!!!!!!!!!!!!!!!!!!
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









	
fi


#============= Actually creating Directories ===================#
echo "Starting MadGraph 5 and generating the directories"
#This will use a coding process to maintain white space for the input to MG5
delimit=($(echo $generate | sed -e "s/;/#/g" | sed -e "s/ /!/g" | fold -w1))
for del in "${delimit[@]}";
do 	
	if [[ "$del" == "#" ]];
	then 
		code+=("$name")
		name=""
	else 
		name="$name$del"
	fi
done
#echo "${code[@]}"




#removing variables 
unset name
unset del
unset delimit




























#================Entering the options menu for tweaking============================#
#==================================================================================#
#Declaring variables
process=()
Additional_Process=()
Evnts=()
BeamEV1=()
BeamEV2=()
Import_model=()
NumberOfRuns=()

#Adding a finish option to menu
generate+=("finished")
selections=("Add Processes" "Edit Number of Events" "Edit Beam Energy" "Model to Import" "Number of Runs" "Finished")

#User interaction point
read -p "Would you like to edit these processes? (y/n): " options
if [ "$options" == "y" ];
then 

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
		if [ "$process" == "finished" ]; 
		then 
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
	
		#Creating a backup file from the run_card.dat	
		echo "Creating a back up of run_data.dat"
		mv run_card.dat run_card_original.dat	
		cp run_card_original.dat run_card.dat

		echo "Chose one of the options below"
		while [ "$suboptions" == "incomplete" ];
		do
			echo -e "You have chosen; Process: \e[1;32m"$process"\e[0m, Additional Processes: \e[1;32m"${Additional_Process[@]}"\e[0m, Number of Events: \e[1;32m"$Evnts"\e[0m, Beam Energy, 1: \e[1;32m"$BeamEV1"\e[0m 2: \e[1;32m"$BeamEV2"\e[0m, Model: \e[1;32m"$Import_model"\e[0m, Number of Runs: \e[1;32m"$NumberOfRuns"\e[0m"  
			select category in "${selections[@]}";
			do
				[ -n "${category}" ] && break
			
			done 
			#Exits the submenu
			if [ "$category" == "Finished" ];
			then
				suboptions="complete"
			
			#Enters Add Process 
			elif [ "$category" == "Add Processes" ];
			then 
				read -p "Enter additional decays etc. (ending each with ';'): " decay
				delimit=($(echo $decay | fold -w1))
				Additional_Process=()
				for x in ${delimit[@]};
				do 	
					if [[ "$x" = ";" ]];
					then				
						Additional_Process+=("$v") 
						v=""
					else	
						v="$v$x"
					fi
				done 
				echo "Added: ${Additional_Process[@]} to the simulation"
			
			#Enters Number of Events 
			elif [ "$category" == "Edit Number of Events" ];
			then 		
				unset i
				unset Card
				unset Name
				unset Wanted	

				#Changing the settings in the .dat file using the sed -i (interactive command)				
				Card=run_card.dat
				read -p "Enter the number of events which are to be generated: " Evnts
				sed -i "s/ 10000	= nevents !/ "$Evnts"	= nevents !/g" $Card

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
						unset Name
						unset Wanted
	
						#Changing the settings in the .dat file using the sed -i (interactive command)				
						Card=run_card.dat
						read -p "Enter the energy of Beam 1 (GeV): " BeamEV1
						sed -i "s/6500.0	= ebeam1/"$BeamEV1"	= ebeam1/g" $Card
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
						sed -i "s/6500.0	= ebeam2/"$BeamEV2"	= ebeam2/g" $Card
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
fi 







#echo "generate p p > t t~" >> mycmd



#echo "generate p p > u u~" >> mycmd
#echo "exit" >> mycmd

#ipython "mg5_aMC" $directory/mycmd
#Cleaning up!
#rm mycmd






