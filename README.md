![PXL_20251117_143455765 PORTRAIT](https://github.com/user-attachments/assets/a655760a-35e4-47f3-8b7a-c2231b3e0617)

# Rubik-Pi-AudioClassification
Machine Learning audio classification with Thundercomm Rubik Pi and Edge Impulse

# Hardware Setup

. Plug in the power supply, USB mic, and Ethernet cable to the Rubik Pi.
. Connect the other end of the Ethernet cable to your router.
. Press the power button and wait for the Rubik Pi to boot.
Note: this tutorial assumes a Rubik Pi with Canonical Ubuntu for Qualcomm platforms
. Log in to your router’s admin interface to see the IP assigned to the Rubik Pi.
. SSH into the Rubik Pi
user: ubuntu
pass: ubuntu

# Software setup
Run the following commands to install Edge Impulse on the Rubik PI

$ sudo apt update
$ wget https://cdn.edgeimpulse.com/firmware/linux/setup-edge-impulse-qc-linux.sh
$ sudo apt install selinux-utils
$ source ~/.profile
$ chmod +x setup-edge-impulse-qc-linux.sh
$ ./setup-edge-impulse-qc-linux.sh

Connect the USB Mic and run the following to increase the volume
$ alsamixer

Press F6 to select the USB mic input and press several times arrow up to increase the volume.

Exit and run the following commands to allow Python and Gpio:

$ sudo apt install python3-pip
$ sudo apt install python3-periphery
$ sudo groupadd -f gpio
$ sudo usermod -aG gpio ubuntu
$ sudo nano /etc/udev/rules.d/99-gpio.rules 

Add these lines to the file

SUBSYSTEM=="gpio", KERNEL=="gpiochip*", GROUP="gpio", MODE="0660"

SUBSYSTEM=="gpio", ACTION=="add", PROGRAM="/bin/sh -c 'chown root:gpio /sys/class/gpio/export /sys/class/gpio/unexport; chmod 220 /sys/class/gpio/export /sys/class/gpio/unexport'"

SUBSYSTEM=="gpio", ACTION=="add", PROGRAM="/bin/sh -c 'chown root:gpio /sys%p/direction /sys%p/value; chmod 660 /sys%p/direction /sys%p/value'"

Ctrl-X and Yes to save and exit.

$ sudo udevadm control --reload-rules
$ sudo udevadm trigger
$ sudo reboot

Run 
$ edge-impulse-linux-runner –clean

Select the project, unoptimized, select the USB mic

You should see an output like:

classifyRes 2ms. { street: 0.9999, glass: 0.0001 }
classifyRes 2ms. { street: 0.8629, glass: 0.1371 }

Then you can run glass.py 
