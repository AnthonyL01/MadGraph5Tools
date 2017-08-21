#!/bin/sh
#!/bin/bash

directory=~/Plots/*
cd ~/Plots/
jets0after=()
jetsafter=()
jets0before=()
jetsbefore=()
for file in $directory
do
	echo "$file"
	name=${file##*/}
	actual=${name%.*}
	convert -density 500 $file $name.jpg
	newfile="$name.jpg"
	output="trimmed$actual.jpg"
	convert -trim $newfile $output
	real="$actual.jpg"
	label="$(cut -d "_" -f2 <<< $actual)"
	label2="$(cut -d "_" -f4 <<< $actual)"
	label3="$(sed "s/[^0-9]//g" <<< $label2)"
	if [[ "$label" == "jets0" ]];
	then
		if [[ "$label2" == "before"* ]];
		then 
			name="can_""$label""_met_""beforeFit$label3"".jpg"
			jets0before+=("$name")
		elif [[ "$label2" == "after"* ]];
		then
			name="can_""$label""_met_""afterFit$label3"".jpg"
			jets0after+=("$name")
		fi
	fi
	if [[ "$label" == "jets" ]];
	then 
		if [[ "$label2" == "before"* ]];
		then 
			name="can_""$label""_met_""$label2"".jpg"
			jetsbefore+=("$name")
		elif [[ "$label2" == "after"* ]];
		then		
			name="can_""$label""_met_""$label2"".jpg"
			jetsafter+=("$name")
		fi
	fi
	comment="$label$label2"
	rm $file
	rm $newfile
	convert -pointsize 150 -fill black -draw "text 500,100 "$comment" " $output $real
	rm $output
done

for i in "${!jets0after[@]}";
do
	
	nameJet0a="${jets0after[$i]}"
	label2a="$(cut -d "_" -f4 <<< $nameJet0a)"
	label3a="$(sed "s/[^0-9]//g" <<< $label2a)"
	for z in "${!jets0after[@]}";
	do 
		nameJet0b="${jets0before[$z]}"
		label2b="$(cut -d "_" -f4 <<< $nameJet0b)"
		label3b="$(sed "s/[^0-9]//g" <<< $label2b)"
		if [[ "$label3b" == "$label3a" ]];
		then 
			inputa="can_jets0_met_afterFit$label3a.jpg"
			inputb="can_jets0_met_beforeFit$label3b.jpg"
			output="can_jets0_met_$label3a.jpg"
			convert +append $inputa $inputb $output
		fi
	done
done

for i in "${!jetsafter[@]}";
do
	
	nameJeta="${jetsafter[$i]}"
	label2a="$(cut -d "_" -f4 <<< $nameJeta)"
	label3a="$(sed "s/[^0-9]//g" <<< $label2a)"
	for z in "${!jetsafter[@]}";
	do 
		nameJetb="${jetsbefore[$z]}"
		label2b="$(cut -d "_" -f4 <<< $nameJetb)"
		label3b="$(sed "s/[^0-9]//g" <<< $label2b)"
		if [[ "$label3b" == "$label3a" ]];
		then 
			inputa="can_jets_met_afterFit$label3a.jpg"
			inputb="can_jets_met_beforeFit$label3b.jpg"
			output="can_jets_met_$label3a.jpg"
			rm $inputa $inputb
			convert +append $inputa $inputb $output
		fi
	done
done