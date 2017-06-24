Pijuke is a simple jukebox GUI designed for the raspberry pi for cases where input is limited as in the case of an joystick/button setup.
However pijuke will also work with standard keyboard inputs.

To get started simply change the value of 'MUSIC_DIRECTORY' in pijuke.py to point to the location of your mp3 files. 
You then need to run the following commands on the command line:

sudo apt-get install vlc
sudo pip install mutagen 
sudo pip install python-imaging-tk


and finally start pijuke
python pijuke.py
