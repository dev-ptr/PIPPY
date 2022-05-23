#!/usr/bin/python3
# File name   : setup.py for PIPPY
# Date        : 2020/11/24

import os
import time
import re

curpath = os.path.realpath(__file__)
thisPath = os.path.dirname(curpath)

def replace_num(file,initial,new_num):  
    newline=""
    str_num=str(new_num)
    with open(file,"r") as f:
        for line in f.readlines():
            if(line.find(initial) == 0):
                line = (str_num+'\n')
            newline += line
    with open(file,"w") as f:
        f.writelines(newline)


def exec_loop(command):
	for x in range(1,4):
		if os.system(command) == 0:
			break

def catch_replace_exception(file, string, replacement):
	try:
		replace_num(file, string, replacement)
	except:
		print("try again")

# Rather than repeat code 100* we'll actually use a function for it
exec_loop("sudo apt update")
exec_loop("sudo apt -y dist-upgrade")
exec_loop("sudo apt clean")
exec_loop("sudo pip3 install -U pip")
exec_loop("sudo apt-get install -y python-dev python3-pip libfreetype6-dev libjpeg-dev build-essential")
exec_loop("sudo -H pip3 install --upgrade luma.oled")
exec_loop("sudo apt-get install -y i2c-tools")
exec_loop("sudo apt-get install -y python3-smbus")

# Now we install all the things that were left out... (In the event we aren't using a bloated GUI image)
exec_loop("sudo apt-get install -y libharfbuzz0 libavcodec58 libavformat58 libswscale5 libgtk-3-0 libilmbase-dev libopenexr-dev")
exec_loop("sudo pip3 install icm20948")
exec_loop("sudo pip3 install flask")
exec_loop("sudo pip3 install flask_cors")
exec_loop("sudo pip3 install websockets")

# like our consolidation of exec loops, we'll do the same for exception
catch_replace_exception("/boot/config.txt",'#dtparam=i2c_arm=on','dtparam=i2c_arm=on')
catch_replace_exception("/boot/config.txt",'[all]','[all]\ngpu_mem=128')
catch_replace_exception("/boot/config.txt",'camera_auto_detect=1','#camera_auto_detect=1\nstart_x=1')
catch_replace_exception("/boot/config.txt",'camera_auto_detect=1','#camera_auto_detect=1')


exec_loop("sudo pip3 install opencv-contrib-python==3.4.11.45")


# Removed the fallback because it potentially either doesn't hit or if it does can potentially break
exec_loop("sudo pip3 uninstall -y numpy")
exec_loop("sudo pip3 install numpy==1.21")
exec_loop("sudo apt-get -y install libhdf5-dev libhdf5-serial-dev libatlas-base-dev libjasper-dev")
exec_loop("sudo pip3 install imutils zmq pybase64 psutil")
exec_loop("sudo apt-get install -y util-linux procps hostapd iproute2 iw haveged dnsmasq")
exec_loop("sudo pip3 install pi-ina219")
exec_loop("cd " + thisPath + " && cd .. && sudo git clone https://github.com/oblique/create_ap")

try:
	os.system("cd " + thisPath + " && cd .. && cd create_ap && sudo make install")
except:
	pass

# Here we actually check if it's in /etc/rc.local before putting it in there
run_string = 'cd '+thisPath+' && sudo python3 webServer.py &\nexit 0'
file = open("/etc/rc.local")
if run_string not in file.read():
	replace_num('/etc/rc.local','exit 0', run_string)
else:
	print("Start up already in /etc/rc.local, skipping...")

print('Completed!')

os.system("sudo reboot")
