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

# Set: HDMI Video & Audio
	
	######## Video setup
	
	# Script.bin modification
	bin2fex /boot/script.bin /boot/script.fex
	FexChange "/boot/script.fex" "disp_init" "disp_mode" "0" # Use Screen0 configs
	FexChange "/boot/script.fex" "disp_init" "screen0_output_type" "3" # HDMI
	FexChange "/boot/script.fex" "disp_init" "screen0_output_mode" "5" # 720p
        FexChange "/boot/script.fex" "disp_init" "fb0_width" "0" # default setting
        FexChange "/boot/script.fex" "disp_init" "fb0_height" "0" # default setting
        FexChange "/boot/script.fex" "disp_init" "fb1_width" "0" # default setting
        FexChange "/boot/script.fex" "disp_init" "fb1_height" "0" # default setting
	FexChange "/boot/script.fex" "hdmi_para" "hdmi_used" "1" # Turn on HDMI
	FexChange "/boot/script.fex" "tv_para" "tv_used" "0" # Turn off RCA
	FexChange "/boot/script.fex" "audiohub" "hub_used" "0" # Disable Audio HUB
	FexChange "/boot/script.fex" "audiohub" "spdif_used" "0" # Disable SPDIF
	fex2bin /boot/script.fex /boot/script.bin
	
	# TV module load
	sed -i '/tv/d' /etc/modules # Delete "tv" line
	sed -i '/^ *$/d' /etc/modules # Delete empty lines
	
	######## Audio setup
	RetrocfgChange '/opt/retropie/configs/all/retroarch.cfg' 'audio_device' '""'
	cp -a files/hdmi/asound.conf /etc/asound.conf
	cp -a files/hdmi/asoundrc /home/pi/.asoundrc
