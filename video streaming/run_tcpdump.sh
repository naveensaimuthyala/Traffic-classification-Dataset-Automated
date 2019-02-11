#!/bin/bash
#FIXME change with your interface name -n -i option  
sudo tcpdump ip and host not 129.173.213.21 and not ether multicast -i enp0s3 -vvv -s 800 -w capture_$(date +%F-%H).pcap & 
sleep 7300
sudo killall tcpdump
