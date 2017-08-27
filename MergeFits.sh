#!/bin/sh
#!/bin/bash

directory=~/Plots #<------------------- change to desired
first=$directory/*
cd $directory
for file in $first
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
	comment="$label$label2"
	rm $file
	rm $newfile
	convert -pointsize 150 -fill black -draw "text 500,100 "$comment" " $output $real
	rm $output
done

Jets0before=$directory/can_jets0_met_beforeFit*
Jets0after=$directory/can_jets0_met_afterFit*
for i in $Jets0after
do
	string="${i##*/}"
	tempstring="$(cut -d "_" -f4 <<< $string)"
	events="$(sed "s/[^0-9]//g" <<< $tempstring)"
	conditionstring="can_jets0_met_beforeFit$events.jpg"
	for z in $Jets0before
	do
		name="${z##*/}"
		if [[ "$name" == "$conditionstring" ]];
		then
			output="0jets_$events.jpg"
			convert +append $name $string $output
		fi
	done
done

Jetsbefore=$directory/can_jets_met_beforeFit*
Jetsafter=$directory/can_jets_met_afterFit*
for i in $Jetsafter
do
	string="${i##*/}"
	tempstring="$(cut -d "_" -f4 <<< $string)"
	events="$(sed "s/[^0-9]//g" <<< $tempstring)"
	conditionstring="can_jets_met_beforeFit$events.jpg"
	for z in $Jetsbefore
	do
		name="${z##*/}"
		if [[ "$name" == "$conditionstring" ]];
		then
			output="jets_$events.jpg"
			finalout="Hist_$events.jpg"
			final0j="0jets_$events.jpg"
			convert +append $name $string $output
			convert -append $output $final0j $finalout
			rm $output
			rm $final0j
		fi
	done
done