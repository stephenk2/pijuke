#!/usr/bin/env python

import sys
import glob
from Tkinter import *
import tkFont
import vlc
from PIL import Image, ImageTk
from mutagen.id3 import ID3
from mutagen.mp3 import MP3
import pygame
import os
import subprocess

#sudo apt-get install vlc, sudo pip install mutagen, sudo pip install python-imaging-tk
pygame.init()
my_joystick = pygame.joystick.Joystick(0)
my_joystick.init()

root = Tk()
#sw sh 1366 768
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

MUSIC_DIRECTORY = "/media/usb/music/"

LABEL_WIDTH=int(screen_width*0.168)
LABEL_HEIGHT=int(screen_height*0.081)
LABEL_X = int(screen_width*0.212)
LABEL_Y =int(screen_height*0.242)

NOW_PLAYING_HEIGHT=int(screen_height*0.005)
NOW_PLAYING_WIDTH=int(screen_width*0.024)
QUEUE_HEIGHT=int(screen_height*0.005)
QUEUE_WIDTH=int(screen_width*0.025)

NOW_PLAYING_X = int(screen_width*0.510)
NOW_PLAYING_Y = int(screen_height*0.816)
QUEUE_X = int(screen_width*0.277)
QUEUE_Y = int(screen_height*0.816)

LETTER_X = int(screen_width*0.113)
LETTER_Y = int(screen_height*0.842)
ROW_LETTER_X = int(screen_width*0.140)

VOL_X=int(screen_width*0.835)
VOL_Y=int(screen_height*0.848)


queue = []
p = vlc.MediaPlayer()

curvol = 50
vlc.MediaPlayer.audio_set_volume(p, curvol)

im = Image.open('/home/pi/pijuke-master/pijuke_frontend_2.png')




fixedim = im.resize((screen_width,screen_height))
tkimage = ImageTk.PhotoImage(fixedim)
myvar=Label(root,image = tkimage)
myvar.place(x=0, y=0, relwidth=1, relheight=1)

root.attributes('-fullscreen', True)
font = 'comic 22 bold'
song_dictionary = {0:{0:{"ARTIST":"","SONGNAME":""},1:{"ARTIST":"","SONGNAME":""},2:{"ARTIST":"","SONGNAME":""},3:{"ARTIST":"","SONGNAME":""},
                      4:{"ARTIST":"","SONGNAME":""},5:{"ARTIST":"","SONGNAME":""},6:{"ARTIST":"","SONGNAME":""},7:{"ARTIST":"","SONGNAME":""}
                     ,8:{"ARTIST":"","SONGNAME":""},9:{"ARTIST":"","SONGNAME":""},10:{"ARTIST":"","SONGNAME":""},11:{"ARTIST":"","SONGNAME":""},
                     12:{"ARTIST":"","SONGNAME":""},13:{"ARTIST":"","SONGNAME":""},14:{"ARTIST":"","SONGNAME":""}}}
my_music =  glob.glob("{}*.mp3".format(MUSIC_DIRECTORY))

skipvar= False
paused = False
pagenum = 0
songs_on_page = 0 


# Parse the my_music list, extracting metadata and storing songs in a dictionary
for song in my_music:
    mediafile = MP3(song)
    metadata = mediafile.pprint() # gets all metadata
    try:
        title = (metadata.split("TIT2=")[1]).split("\n")[0]
    except:
        title = (song.split("/")[-1]).replace(".mp3","")
        if len(title) > 28:
            title = title[:28]+"..."
    try:
        author = (metadata.split("TPE1=")[1]).split("\n")[0]
        if len(author) > 28:
            author = author[:28]+"..."    
    except:
        author = ""
    try:
        time = int(float((metadata.split(" seconds")[0]).split(", ")[-1]))
    except:
        time = 0

    if songs_on_page == 15:
        pagenum += 1
        song_dictionary[pagenum] = {0:{"ARTIST":"","SONGNAME":""},1:{"ARTIST":"","SONGNAME":""},2:{"ARTIST":"","SONGNAME":""},3:{"ARTIST":"","SONGNAME":""},
                      4:{"ARTIST":"","SONGNAME":""},5:{"ARTIST":"","SONGNAME":""},6:{"ARTIST":"","SONGNAME":""},7:{"ARTIST":"","SONGNAME":""}
                     ,8:{"ARTIST":"","SONGNAME":""},9:{"ARTIST":"","SONGNAME":""},10:{"ARTIST":"","SONGNAME":""},11:{"ARTIST":"","SONGNAME":""},
                     12:{"ARTIST":"","SONGNAME":""},13:{"ARTIST":"","SONGNAME":""},14:{"ARTIST":"","SONGNAME":""}}
        songs_on_page = 0
    songs_on_page += 1
    song_dictionary[pagenum][songs_on_page-1] = {"SONGPATH":song, "SONGNAME":title,"ARTIST": author, "LENGTH": time}

def fakefunction():
    pass

#Called each time a song is added or a song is skipped, will either play a song or add it to queue
def comp_s(index, songname):
    global queue
    global p
    state = str(p.get_state())
  
    if state != "State.Playing":
        p = vlc.MediaPlayer('/home/pi/pijuke-master/record_play.wav')
        p.play()
        root.after(3500, fakefunction())
        p = vlc.MediaPlayer(song_dictionary[index][songname]["SONGPATH"])
        p.play()
        nowplayinglistbox.insert(END, song_dictionary[index][songname]["SONGNAME"])
    else:
        listbox.insert(END, song_dictionary[index][songname]["SONGNAME"])
        queue.append((index, songname))

        
current_page = 0

# Changes the list of songs being displayed depending on direction
def change_page(direction):
    global current_page
    global pagenum #this is the max page
    state = str(p.get_state())
    if direction == "right":
        if state != "State.Playing":
            x = vlc.MediaPlayer('/home/pi/pijuke-master/fast_change_page.wav')
            x.play()
            root.after(1050, fakefunction())
        else:
            root.after(500, fakefunction())
        if current_page == pagenum: # if we can't go right anymore then go to first page
            current_page = 0
        else:
            current_page += 1
    elif direction == "left":
        if state != "State.Playing":
            x = vlc.MediaPlayer('/home/pi/pijuke-master/fast_change_page.wav')
            x.play()
            root.after(1050, fakefunction())
        else:
            root.after(500, fakefunction())
        if current_page == 0: # if we cant go left anymore then go to max page
            current_page = pagenum
        else:
            current_page -= 1
    update_buttons()


photoimage1 = Image.open("/home/pi/pijuke-master/black_white_label.png").resize((LABEL_WIDTH, LABEL_HEIGHT)) 
photoimage = ImageTk.PhotoImage(photoimage1)  

listbox = Listbox(root, height=QUEUE_HEIGHT, width=QUEUE_WIDTH,borderwidth=0, highlightthickness=0, bg='black', fg='white')
listbox.place(x=QUEUE_X, y=QUEUE_Y)

nowplayinglistbox = Listbox(root, height=NOW_PLAYING_HEIGHT, width=NOW_PLAYING_WIDTH,borderwidth=0, highlightthickness=0, bg='black', fg='white')
nowplayinglistbox.place(x=NOW_PLAYING_X, y=NOW_PLAYING_Y)

vol_font = tkFont.Font(size=25)
volbox = Listbox(root, height=1, width=3,borderwidth=0, highlightthickness=0, bg='black', fg='white', font=vol_font)
volbox.place(x=VOL_X, y=VOL_Y)
volbox.insert(END,curvol)


print song_dictionary
button1 = Label(root, text=song_dictionary[current_page][0]["ARTIST"]+"\n\n"+song_dictionary[current_page][0]["SONGNAME"],anchor = N, image = photoimage,font = 'comic 8 bold',  height=LABEL_HEIGHT, width=LABEL_WIDTH,borderwidth=0, highlightthickness=0, compound=CENTER)
button1.place(x=LABEL_X, y=LABEL_Y)
button2 = Label(root, text=song_dictionary[current_page][1]["ARTIST"]+"\n\n"+song_dictionary[current_page][1]["SONGNAME"], image = photoimage,font = 'comic 8 bold', relief='flat', height=LABEL_HEIGHT, width=LABEL_WIDTH,borderwidth=0, highlightthickness=0, compound=CENTER)
button2.place(x=LABEL_X+int(screen_width*0.204), y=LABEL_Y)
button3 = Label(root, text=song_dictionary[current_page][2]["ARTIST"]+"\n\n"+song_dictionary[current_page][2]["SONGNAME"], image = photoimage,font = 'comic 8 bold', relief='groove', height=LABEL_HEIGHT, width=LABEL_WIDTH,borderwidth=0, highlightthickness=0, compound=CENTER)
button3.place(x=LABEL_X+int(screen_width*0.406), y=LABEL_Y)

button4 = Label(root, text=song_dictionary[current_page][3]["ARTIST"]+"\n\n"+song_dictionary[current_page][3]["SONGNAME"], image = photoimage,font = 'comic 8 bold', relief='groove', height=LABEL_HEIGHT, width=LABEL_WIDTH,borderwidth=0, highlightthickness=0, compound=CENTER)
button4.place(x=LABEL_X, y=LABEL_Y+LABEL_HEIGHT)
button5 = Label(root, text=song_dictionary[current_page][4]["ARTIST"]+"\n\n"+song_dictionary[current_page][4]["SONGNAME"], image = photoimage,font = 'comic 8 bold',  relief='groove', height=LABEL_HEIGHT, width=LABEL_WIDTH,borderwidth=0, highlightthickness=0, compound=CENTER)
button5.place(x=LABEL_X+int(screen_width*0.204), y=LABEL_Y+LABEL_HEIGHT)
button6 = Label(root, text=song_dictionary[current_page][5]["ARTIST"]+"\n\n"+song_dictionary[current_page][5]["SONGNAME"], image = photoimage,font = 'comic 8 bold', relief='groove', height=LABEL_HEIGHT, width=LABEL_WIDTH,borderwidth=0, highlightthickness=0, compound=CENTER)
button6.place(x=LABEL_X+int(screen_width*0.406), y=LABEL_Y+LABEL_HEIGHT)

button7 = Label(root, text=song_dictionary[current_page][6]["ARTIST"]+"\n\n"+song_dictionary[current_page][6]["SONGNAME"], image = photoimage,font = 'comic 8 bold',  relief='groove', height=LABEL_HEIGHT, width=LABEL_WIDTH,borderwidth=0, highlightthickness=0, compound=CENTER)
button7.place(x=LABEL_X, y=LABEL_Y+(LABEL_HEIGHT*2))
button8 = Label(root, text=song_dictionary[current_page][7]["ARTIST"]+"\n\n"+song_dictionary[current_page][7]["SONGNAME"], image = photoimage,font = 'comic 8 bold',  relief='groove', height=LABEL_HEIGHT, width=LABEL_WIDTH,borderwidth=0, highlightthickness=0, compound=CENTER)
button8.place(x=LABEL_X+int(screen_width*0.204), y=LABEL_Y+(LABEL_HEIGHT*2))
button9 = Label(root, text=song_dictionary[current_page][8]["ARTIST"]+"\n\n"+song_dictionary[current_page][8]["SONGNAME"], image = photoimage,font = 'comic 8 bold',  relief='groove', height=LABEL_HEIGHT, width=LABEL_WIDTH,borderwidth=0, highlightthickness=0, compound=CENTER)
button9.place(x=LABEL_X+int(screen_width*0.406), y=LABEL_Y+(LABEL_HEIGHT*2))

button10 = Label(root, text=song_dictionary[current_page][9]["ARTIST"]+"\n\n"+song_dictionary[current_page][9]["SONGNAME"],image = photoimage,font = 'comic 8 bold',  relief='groove', height=LABEL_HEIGHT, width=LABEL_WIDTH,borderwidth=0, highlightthickness=0, compound=CENTER)
button10.place(x=LABEL_X, y=LABEL_Y+(LABEL_HEIGHT*3))
button11 = Label(root, text=song_dictionary[current_page][10]["ARTIST"]+"\n\n"+song_dictionary[current_page][10]["SONGNAME"],image = photoimage,font = 'comic 8 bold',  relief='groove', height=LABEL_HEIGHT, width=LABEL_WIDTH,borderwidth=0, highlightthickness=0, compound=CENTER)
button11.place(x=LABEL_X+int(screen_width*0.204), y=LABEL_Y+(LABEL_HEIGHT*3))
button12 = Label(root, text=song_dictionary[current_page][11]["ARTIST"]+"\n\n"+song_dictionary[current_page][11]["SONGNAME"], image = photoimage,font = 'comic 8 bold',  relief='groove', height=LABEL_HEIGHT, width=LABEL_WIDTH,borderwidth=0, highlightthickness=0, compound=CENTER)
button12.place(x=LABEL_X+int(screen_width*0.406), y=LABEL_Y+(LABEL_HEIGHT*3))

button13 = Label(root, text=song_dictionary[current_page][12]["ARTIST"]+"\n\n"+song_dictionary[current_page][12]["SONGNAME"],image = photoimage,font = 'comic 8 bold', relief='groove', height=LABEL_HEIGHT, width=LABEL_WIDTH,borderwidth=0, highlightthickness=0, compound=CENTER)
button13.place(x=LABEL_X, y=LABEL_Y+(LABEL_HEIGHT*4))
button14 = Label(root, text=song_dictionary[current_page][13]["ARTIST"]+"\n\n"+song_dictionary[current_page][13]["SONGNAME"],image = photoimage,font = 'comic 8 bold',  relief='groove', height=LABEL_HEIGHT, width=LABEL_WIDTH,borderwidth=0, highlightthickness=0, compound=CENTER)
button14.place(x=LABEL_X+int(screen_width*0.204), y=LABEL_Y+(LABEL_HEIGHT*4))
button15 = Label(root, text=song_dictionary[current_page][14]["ARTIST"]+"\n\n"+song_dictionary[current_page][14]["SONGNAME"], image = photoimage,font = 'comic 8 bold', relief='groove', height=LABEL_HEIGHT, width=LABEL_WIDTH,borderwidth=0, highlightthickness=0, compound=CENTER)
button15.place(x=LABEL_X+int(screen_width*0.406), y=LABEL_Y+(LABEL_HEIGHT*4))


# Changes the songs/artists being displayed
def update_buttons():
    button1.configure(text=song_dictionary[current_page][0]["ARTIST"]+"\n\n"+song_dictionary[current_page][0]["SONGNAME"])
    button2.configure(text=song_dictionary[current_page][1]["ARTIST"]+"\n\n"+song_dictionary[current_page][1]["SONGNAME"])
    button3.configure(text=song_dictionary[current_page][2]["ARTIST"]+"\n\n"+song_dictionary[current_page][2]["SONGNAME"])
    button4.configure(text=song_dictionary[current_page][3]["ARTIST"]+"\n\n"+song_dictionary[current_page][3]["SONGNAME"])
    button5.configure(text=song_dictionary[current_page][4]["ARTIST"]+"\n\n"+song_dictionary[current_page][4]["SONGNAME"])
    button6.configure(text=song_dictionary[current_page][5]["ARTIST"]+"\n\n"+song_dictionary[current_page][5]["SONGNAME"])
    button7.configure(text=song_dictionary[current_page][6]["ARTIST"]+"\n\n"+song_dictionary[current_page][6]["SONGNAME"])
    button8.configure(text=song_dictionary[current_page][7]["ARTIST"]+"\n\n"+song_dictionary[current_page][7]["SONGNAME"])
    button9.configure(text=song_dictionary[current_page][8]["ARTIST"]+"\n\n"+song_dictionary[current_page][8]["SONGNAME"])
    button10.configure(text=song_dictionary[current_page][9]["ARTIST"]+"\n\n"+song_dictionary[current_page][9]["SONGNAME"])
    button11.configure(text=song_dictionary[current_page][10]["ARTIST"]+"\n\n"+song_dictionary[current_page][10]["SONGNAME"])
    button12.configure(text=song_dictionary[current_page][11]["ARTIST"]+"\n\n"+song_dictionary[current_page][11]["SONGNAME"])
    button13.configure(text=song_dictionary[current_page][12]["ARTIST"]+"\n\n"+song_dictionary[current_page][12]["SONGNAME"])
    button14.configure(text=song_dictionary[current_page][13]["ARTIST"]+"\n\n"+song_dictionary[current_page][13]["SONGNAME"])
    button15.configure(text=song_dictionary[current_page][14]["ARTIST"]+"\n\n"+song_dictionary[current_page][14]["SONGNAME"])

root.update()


# Increases or decreases the volume, 
def vol_changer(direction, event=None):
    global curvol
    global p
    if direction == 'up':
        curvol = curvol + 5
        if curvol > 100:
            curvol = 100
        vlc.MediaPlayer.audio_set_volume(p, curvol)
        volbox.delete(0)
        volbox.insert(END, curvol)
    else:
        curvol = curvol - 5
        if curvol <0:
            curvol = 0
        vlc.MediaPlayer.audio_set_volume(p, curvol)
        volbox.delete(0)
        volbox.insert(END, curvol)

# Sets the skipvar variable to True, next time manage queue is called it will skip the currently playing song        
def skip():
    global skipvar
    skipvar = True
   
   
# Sets the paused variable to the opposite of its current setting       
def pause(event=None):
    global paused
    global p    
    if paused == True:
        paused= False
        p.play()
    else:
        paused = True
        p.pause()

# Create 'buttons' for each of the controls        
rightbutton = Button(root, text='right', command=lambda: change_page('right'), relief='groove')
rightbutton.place(x=859, y=1000)
leftbutton = Button(root, text='left', command=lambda: change_page('left'), relief='groove')
leftbutton.place(x=859, y=1000)
volupbutton = Button(root, text='Vol up', command=lambda: vol_changer('up'), relief='groove')
volupbutton.place(x=859, y=1000)
volupbutton = Button(root, text='Vol down', command=lambda: vol_changer('down'), relief='groove')
volupbutton.place(x=859, y=1000)
skipbutton = Button(root, text='Skip', command=lambda: skip(), relief='groove')
skipbutton.place(x=859, y=1000)
pausebutton = Button(root, text='Pause', command=lambda: pause(), relief='groove')
pausebutton.place(x=859, y=1000)

letterpick = ""
letter_dict = {"A":0, "B":1, "C":2,"D":3,"E":4,"F":5}
column_dict = {"A":[0,3,6,9,12], "B":[1,4,7,10,13],"C":[2,5,8,11,14]}

col_lab = ""
row_lab = ""


# Called every time one the 'lettered' buttons are pushed. If first time being called stores the column in 'letterpick', else the letter is used to choose the row
def pick_song(index):
    global col_lab
    global row_lab
    global p
    state = str(p.get_state)
    if state != "State.Playing":
        x = vlc.MediaPlayer('/home/pi/pijuke-master/button_press.wav')
        x.play()

    if index == "delete":
        col_lab.destroy()
        row_lab.destroy()
    else:
        global current_page
        global letterpick    
        if letterpick == "":
            acceptable_columns = ["A","B","C"]
            if index in acceptable_columns:
                letterpick = index
                lab = Label(root, text=index, width = 2, height=1,borderwidth=0, highlightthickness=0, bg='black', fg='white', font=("Helvetica", 20))
                lab.place(x=LETTER_X, y=LETTER_Y)
                col_lab = lab
        else:
            x = True
            row = Label(root, text=index, width = 2, height=1,borderwidth=0, highlightthickness=0, bg='black', fg='white', font=("Helvetica", 20))
            row.place(x=ROW_LETTER_X, y=LETTER_Y)
            row_lab = row
            total = column_dict[letterpick][letter_dict[index]]
            comp_s(current_page, total)
            letterpick = ""
            root.after(1000, pick_song, "delete")

# Used to exit the frontend
def quit_gui():
    subprocess.call("killall xinit",shell=True)
    sys.exit()  


# Binds keyboard inputs to actions, all lowercase
root.bind("<a>", (lambda event: pick_song("A")))
root.bind("<b>", (lambda event: pick_song("B")))
root.bind("<c>", (lambda event: pick_song("C")))
root.bind("<d>", (lambda event: pick_song("D")))
root.bind("<e>", (lambda event: pick_song("E")))
root.bind("<p>", (lambda event: pause()))
root.bind("<s>", (lambda event: skip()))
root.bind("<q>", (lambda event: quit_gui()))
root.bind("<Up>", (lambda event: vol_changer('up')))
root.bind("<Down>", (lambda event: vol_changer('down')))
root.bind("<Left>", (lambda event: change_page('left')))
root.bind("<Right>", (lambda event: change_page('right')))


#This is called continuously, if it detects a song has ended and the queue is not empty it will start playing the next song
def manage_queue():
    print "manage queue called"
    global queue
    global skipvar
    global p
    #print "event queue", pygame.event.get()
    event_list = pygame.event.get()
    print "event list", event_list
    for event_name in event_list:
        print "EVENt", event_name.type

        # if event_name.type is 10, a button has been pressed
        if event_name.type == 10:
            print event_name.button
            if event_name.button == 0:
                change_page('left')
            if event_name.button == 1:
                vol_changer("up", event=None)
            if event_name.button == 2:
                vol_changer("down", event=None)
            if event_name.button == 3:
                change_page('right')
            if event_name.button == 5:
                pick_song("B")
            if event_name.button == 6:
                pick_song("C")
            if event_name.button == 4:
                pick_song("E")
            if event_name.button == 7:
                pick_song("F")
            if event_name.button == 8:
                skip()
            if event_name.button == 9:
                pause()
        if event_name.type == 7:
            print "JOYSTICK PUSHED ", event_name.value
            if event_name.value == 1.0:
                print "calling son"
                pick_song("A")
            elif event_name.value <= -0.5:
                pick_song("D")
            else:
                print "Failure", event_name.value

    
        #if event_name.type == pygame.JOYBUTTONUP:
        #    print "up pressed"
        #    vol_changer("up", event=None)
        #elif event_name.type == pygame.JOYBUTTONDOWN:
        #    print "down pressed"
        #    vol_changer("down", event=None)
    
    if skipvar == False:
        state = str(p.get_state())
        if state == "State.Ended" or state == "State.Stopped":
            nowplayinglistbox.delete(0)
            if queue != []:
                index = queue[0][0]
                songname = queue[0][1]
                queue.remove(queue[0])
                listbox.delete(0)
                comp_s(index, songname)
    else:
        nowplayinglistbox.delete(0)
        p.stop()
        skipvar = False
        if queue != []:
            index = queue[0][0]
            songname = queue[0][1]
            queue.remove(queue[0])
            listbox.delete(0)
            comp_s(index, songname)     
    root.after(1000,manage_queue)
 
 
root.after(0, manage_queue())
root.mainloop()
