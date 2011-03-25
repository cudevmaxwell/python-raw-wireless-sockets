#!/bin/bash

scp -r /home/student/Desktop/YOBATMAN student@192.168.0.182:/home/student/Desktop
echo 182 is finished

scp -r /home/student/Desktop/YOBATMAN student@192.168.0.183:/home/student/Desktop
echo 183 is finished

scp -r /home/student/Desktop/YOBATMAN student@192.168.0.174:/home/student/Desktop
echo 174 is finished

scp -r /home/student/Desktop/YOBATMAN student@192.168.0.198:/home/student/Desktop
echo 198 is finished

scp -r /home/student/Desktop/YOBATMAN student@192.168.0.197:/home/student/Desktop
echo 197 is finished

scp -r /home/student/Desktop/YOBATMAN student@192.168.0.196:/home/student/Desktop
echo 196 is finished

scp -r /home/student/Desktop/YOBATMAN student@192.168.0.184:/home/student/Desktop
echo 184 is finished


ssh -Y -f student@192.168.0.182 gksu /usr/bin/x-terminal-emulator
read -p "182 Started? (Press any key to confirm)"
ssh -Y -f student@192.168.0.174 gksu /usr/bin/x-terminal-emulator
read -p "174 Started? (Press any key to confirm)"
ssh -Y -f student@192.168.0.183 gksu /usr/bin/x-terminal-emulator
read -p "183 Started? (Press any key to confirm)"
ssh -Y -f student@192.168.0.198 gksu /usr/bin/x-terminal-emulator
read -p "198 Started? (Press any key to confirm)"
ssh -Y -f student@192.168.0.197 gksu /usr/bin/x-terminal-emulator
read -p "197 Started? (Press any key to confirm)"
ssh -Y -f student@192.168.0.196 gksu /usr/bin/x-terminal-emulator
read -p "196 Started? (Press any key to confirm)"
ssh -Y -f student@192.168.0.184 gksu /usr/bin/x-terminal-emulator
read -p "184 Started? (Press any key to confirm)"
