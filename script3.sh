#!/bin/bash

# Jared Marcuccilli
# NSSA-221 Script 3

clear

echo "You are currently in:"
pwd

if [[ $HOME/Desktop != $(pwd) ]]
	then
		echo "Not in desktop."
	else
		echo "In desktop."	
fi

echo ""

while :
do
echo "Please enter the path of the file for which to create a shortcut (type quit to end):"
read path

if [[ -f $path ]]
then
	ln --symbolic $path ~/Desktop/
	echo "Link created in" ~/Desktop/
	break

	elif [[ $path == "quit" ]]
	then
		exit 0
	else
		echo "File does not exist."
fi
done
echo ""

links=$(find . -type l | wc -l)

echo "Links  in current directory:" $links
ls -l | grep "\->" | awk '{ print $9 " " $10 " " $11 }'

echo ""