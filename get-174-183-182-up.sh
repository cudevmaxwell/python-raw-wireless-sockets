#!/bin/bash

scp -r /home/student/Desktop/YOBATMAN student@192.168.0.174:/home/student/Desktop
echo 174 is finished


ssh -Y -f student@192.168.0.174 gksu /usr/bin/x-terminal-emulator
read -p "174 Started? (Press any key to confirm)"

scp -r /home/student/Desktop/YOBATMAN student@192.168.0.183:/home/student/Desktop
echo 183 is finished


ssh -Y -f student@192.168.0.183 gksu /usr/bin/x-terminal-emulator
read -p "183 Started? (Press any key to confirm)"

scp -r /home/student/Desktop/YOBATMAN student@192.168.0.182:/home/student/Desktop
echo 182 is finished


ssh -Y -f student@192.168.0.182 gksu /usr/bin/x-terminal-emulator
read -p "182 Started? (Press any key to confirm)"
