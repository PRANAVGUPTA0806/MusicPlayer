import tkinter as tk
import fnmatch
import os
from pygame import mixer

canvas = tk.Tk()
canvas.title("Music Player")
canvas.geometry("600x800")
canvas.config(bg = 'black')

rootpath = "C:\\4\\Music"
pattern = "*.mp3"

mixer.init()

prev1 = tk.PhotoImage('prev_img.png')
next1 = tk.PhotoImage('next_img.png')
play1 = tk.PhotoImage('play_img.png')
pause1 = tk.PhotoImage('pause_img.png')
stop1 = tk.PhotoImage('stop_img.png')

def play():
    lable.config(text=listBox.get("anchor"))
    mixer.music.load(rootpath + "\\" + listBox.get("anchor"))
    mixer.music.play()
    
def stop():
    mixer.music.stop()
    listBox.select_clear('active')
    
def next():
    next_song = listBox.curselection()
    next_song = next_song[0] + 1
    next_song_name = listBox.get(next_song)
    lable.config(text = next_song_name) 
    
    mixer.music.load(rootpath + "\\" + next_song_name)
    mixer.music.play()
    
    listBox.select_clear(0, 'end')
    listBox.activate(next_song)
    listBox.select_set(next_song)
    
def prev():
    next_song = listBox.curselection()
    next_song = next_song[0] - 1
    next_song_name = listBox.get(next_song)
    lable.config(text = next_song_name) 
    
    mixer.music.load(rootpath + "\\" + next_song_name)
    mixer.music.play()
    
    listBox.select_clear(0, 'end')
    listBox.activate(next_song)
    listBox.select_set(next_song)
    
def pause():
    if pauseButton["text"]=="Pause":
        mixer.music.pause()
        pauseButton["text"]="Play"
    else:
        mixer.music.unpause()
        pauseButton["text"]="Pause"

listBox = tk.Listbox(canvas, fg ="cyan", bg="black", width=100, font=('Mandala Romantic', 16))
listBox.pack(padx = 15, pady = 15)
lable = tk.Label(canvas, text = '', bg = 'black', fg = 'yellow', font=('Mandala Romantic', 18))
lable.pack(pady = 15)

top = tk.Frame(canvas, bg = "black")
top.pack(padx = 10, pady = 5, anchor = 'center')

prevButton = tk.Button(canvas, text = "Prev", image = prev1, bg = 'white', borderwidth = 10, command = prev)
prevButton.pack(pady = 15, in_ = top, side = 'left')

playButton = tk.Button(canvas, text = "Play", image = play1, bg = 'blue', borderwidth = 10, command = play)
playButton.pack(pady = 15, in_ = top, side = 'left')

stopButton = tk.Button(canvas, text = "Stop", image = stop1, bg = 'red', borderwidth = 10, command = stop)
stopButton.pack(pady = 15, in_ = top, side = 'left')


pauseButton = tk.Button(canvas, text = "Pause", image = pause1, bg = 'yellow', borderwidth = 10, command = pause)
pauseButton.pack(pady = 15, in_ = top, side = 'left')

nextButton = tk.Button(canvas, text = "Next", image = next1, bg = 'black', borderwidth = 10, command = next)
nextButton.pack(pady = 15, in_ = top, side = 'left')

for root, dirs, files in os.walk(rootpath):
    for filename in fnmatch.filter(files, pattern):
        listBox.insert('end', filename)

canvas.mainloop()