#!/bin/bash

	# Creating the directory for our pcaps
	[ -d ./pcaps/$1 ] || mkdir -pv ./pcaps/$1
	

	# Creating the file name.
	fname="$1-$(date +'%m-%d-%y_%T')"
	

	if [ ! -z "$2" ]; then
	    fname="$fname-$2"
	    echo "PCAPs in ./pcaps/$1: " $(ls -ltr ./pcaps/$1/ | grep "$2.pcap$" | wc -l)
	else
	    echo "PCAPs in ./pcaps/$1: " $(ls -ltr ./pcaps/$1/ | grep ".pcap$" | wc -l)
	fi
	

	sudo tcpdump -vv -x -X -i eth0 -A tcp and port not 22 -w ./pcaps/$1/$fname.pcap
