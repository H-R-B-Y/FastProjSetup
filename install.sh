#!/bin/bash

# Function to uninstall main.py
uninstall() {
	rm ~/bin/psetup
	if [ $? -ne 0 ]; then
		echo "Error: Could not uninstall psetup"
		exit 1
	fi
	echo "Uninstalled psetup"
}

install() {
	if [ ! -d ~/bin ]; then
		mkdir ~/bin
		if [ $? -ne 0 ]; then
			echo "Error: Could not install psetup"
			exit 1
		fi
	fi
	ln -s $(pwd)/main.py ~/bin/psetup
	if [ $? -ne 0 ]; then
		echo "Error: Could not install psetup"
		exit 1
	fi
	chmod +x ~/bin/psetup
	if [ $? -ne 0 ]; then
		echo "Error: Could not install psetup"
		unlink ~/bin/psetup
		exit 1
	fi
	echo "Installed psetup"
}

# Check if the first argument is "uninstall"
if [[ "$1" == "uninstall" ]]; then
	uninstall
	exit 0
elif [[ "$1" == "install" ]]; then
	install
	exit 0
elif [[ "$1" == "-help" ]]; then
	echo "Usage: ./install.sh [install|uninstall]"
	exit 0
else
	install
	exit 0
fi

