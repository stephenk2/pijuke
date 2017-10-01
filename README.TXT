Pijuke is a simple jukebox GUI designed for the raspberry pi for cases where input is limited as in the case of an joystick/button setup.
However pijuke will also work with standard keyboard inputs.

To get started simply change the value of 'MUSIC_DIRECTORY' in pijuke.py to point to the location of your mp3 files. 
You then need to run the following commands on the command line:

sudo apt-get install vlc python-pip python-dev python-tk python-pygame xorg xserver-xorg-legacy openbox menu
sudo pip install --upgrade pip
sudo pip install Pillow mutagen


and finally start pijuke
python pijuke.py


to start via openbox create a bash script with the following lines:

#!/bin/sh
openbox --config-file ~/.config/openbox/rc.xml --startup ./pijuke-master/pijuke.py

call that script via xinit ./myscript
