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
read -p "Enter the processes to be generated (ending with ';'): " input
generate=()
for i in ${input[@]};
do 
	if [[ "$i" == ";"* ]]; #Note p p > t t~ ; p p > u u~; this combination creates trouble need to fix this....
	then	
		generate+=("${t//;}") 
		t=""
	else	
		t="$t $i"
	fi
done 
echo "${generate[@]}"
#_____________Giving names to each run___________________________
read -p "Enter the name of output (ending with ';'): " names
Names=()
for i in ${names[@]};
do 
	if [[ "$i" == ";"* ]]; #Note p p > t t~ ; p p > u u~; this combination creates trouble need to fix this....
	then	
		Names+=("${t//;}")
		t=""
	else	
		t="$t $i"
	fi
done 
echo "${Names[@]}"


#echo "generate p p > t t~" >> mycmd



#echo "generate p p > u u~" >> mycmd
#echo "exit" >> mycmd

#ipython "mg5_aMC" $directory/mycmd
#Cleaning up!
#rm mycmd