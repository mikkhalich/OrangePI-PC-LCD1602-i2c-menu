#!/bin/bash
# Nombre: main.sh
# Description: Main Script
#############################

# Global Parameters
set -e # No errors allowed

#############################

## Usage: FexChange <fexfile> <section> <key> <value> 
## Description: Changes the value of a given key (or adds key=value) to a specific section of FEX file
FexChange()
{
	# Search in file ($1) in section ($2) for key ($3)
	found=$(sed -n -e "/^\[$2\]/,/^\[/{/^$3\s*=/p}" "$1")
  
	if [ -n "$found" ]; then
		# Replace in file ($1) in section ($2) key ($3) with value ($4)
		sed -i -e "/^\[$2\]/,/^\[/{s/^\($3\s*=\s*\).*/\1$4/}" "$1"
	else
		# Append in file ($1) in section ($2) key ($3) with value ($4)
		sed -i -e "/^\[$2\]/,/^\[/{/^\[/i$3 = $4\n" -e "}" "$1"
	fi
}

## Usage: RetrocfgChange <file_path> <key> <value> 
## Description: Changes the value of a given key (or adds key=value) of retroarch.cfg file
RetrocfgChange()
{
	# Search in file ($1) for key ($2)
	found=$(sed -n -e "/^$2\s*=/p" "$1")
  
	if [ -n "$found" ]; then
		# Replace in file ($1) key ($2) with value ($3)
		sed -i -e "s/^\($2\s*=\s*\).*/\1$3/" "$1"
	else
		# Append in file ($1) key ($2) with value ($3)
		sed -i -e "\$a$2 = $3" "$1"
	fi
}

#############################

# Set: Switch to USB Audio

	# Audio setup
	RetrocfgChange '/opt/retropie/configs/all/retroarch.cfg' 'audio_device' '"hw:2,0"'
        RetrocfgChange '/opt/retropie/configs/all/retroarch.cfg' 'audio_driver' '"sdl2"'
	cp -a files/usb/asound.conf /etc/asound.conf
	cp -a files/usb/asoundrc /home/pi/.asoundrc
	amixer -c 0 set "Audio lineout" unmute
