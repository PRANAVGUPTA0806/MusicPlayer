import tkinter as tk
import fnmatch
import os
from pygame import mixer
from PIL import Image, ImageTk

# Initialize the Tkinter window
canvas = tk.Tk()
canvas.title("Music Player")
canvas.geometry("800x900")  # Adjusted to match the original size
canvas.config(bg='black')

# Path to music files and images
rootpath = "D:\\my-projects\MusicPlayer\\songs"
pattern = "*.mp3"
images_path = "images"

# Initialize the mixer
mixer.init()

# Function to load and resize images
def load_image(filename, size=(50, 50)):
    filepath = os.path.join(images_path, filename)
    if os.path.isfile(filepath):
        image = Image.open(filepath)
        image = image.resize(size, Image.Resampling.LANCZOS)
        return ImageTk.PhotoImage(image)
    else:
        print(f"File not found: {filepath}")
        return None

# Load and resize images for buttons
prev1 = load_image('prev_img.png')
next1 = load_image('next_img.png')
play1 = load_image('play_img.png')
pause1 = load_image('pause_img.png')
stop1 = load_image('stop_img.png')
shuffle1 = load_image('shuffle_img.png')
repeat1 = load_image('repeat_img.png')

# If any image is missing, exit the program
if not all([prev1, next1, play1, pause1, stop1, shuffle1, repeat1]):
    canvas.destroy()
    raise SystemExit("One or more image files are missing. Exiting...")

# Function to update track time
def update_time():
    if mixer.music.get_pos() != -1:
        current_time = mixer.music.get_pos() // 1000
        minutes, seconds = divmod(current_time, 60)
        time_label.config(text=f"{minutes:02}:{seconds:02}")
        canvas.after(1000, update_time)

def play():
    try:
        song = listBox.get("anchor")
        if song:
            lable.config(text=song)
            mixer.music.load(os.path.join(rootpath, song))
            mixer.music.play()
            update_time()
    except Exception as e:
        print(f"Error: {e}")

def stop():
    mixer.music.stop()
    listBox.select_clear('active')
    time_label.config(text="00:00")

def next_song():
    try:
        selection = listBox.curselection()
        if selection:
            next_song_index = selection[0] + 1
            if next_song_index < listBox.size():
                next_song_name = listBox.get(next_song_index)
                lable.config(text=next_song_name)
                mixer.music.load(os.path.join(rootpath, next_song_name))
                mixer.music.play()
                listBox.select_clear(0, 'end')
                listBox.activate(next_song_index)
                listBox.select_set(next_song_index)
                update_time()
    except Exception as e:
        print(f"Error: {e}")

def prev_song():
    try:
        selection = listBox.curselection()
        if selection:
            prev_song_index = selection[0] - 1
            if prev_song_index >= 0:
                prev_song_name = listBox.get(prev_song_index)
                lable.config(text=prev_song_name)
                mixer.music.load(os.path.join(rootpath, prev_song_name))
                mixer.music.play()
                listBox.select_clear(0, 'end')
                listBox.activate(prev_song_index)
                listBox.select_set(prev_song_index)
                update_time()
    except Exception as e:
        print(f"Error: {e}")

def pause():
    if pauseButton["text"] == "Pause":
        mixer.music.pause()
        pauseButton["text"] = "Play"
    else:
        mixer.music.unpause()
        pauseButton["text"] = "Pause"

def search():
    query = search_entry.get().lower()
    listBox.delete(0, tk.END)  # Clear current listbox entries

    for root, dirs, files in os.walk(rootpath):
        for filename in fnmatch.filter(files, pattern):
            if query in filename.lower():  # Case-insensitive search
                listBox.insert(tk.END, filename)

def adjust_volume(val):
    volume = int(val) / 100
    mixer.music.set_volume(volume)

def toggle_shuffle():
    global shuffle_mode
    shuffle_mode = not shuffle_mode
    shuffleButton.config(bg='green' if shuffle_mode else 'gray')

def toggle_repeat():
    global repeat_mode
    repeat_mode = not repeat_mode
    repeatButton.config(bg='green' if repeat_mode else 'gray')

def add_to_playlist():
    song = listBox.get("anchor")
    if song and song not in playlistBox.get(0, tk.END):
        playlistBox.insert(tk.END, song)

def remove_from_playlist():
    selected_songs = playlistBox.curselection()
    for index in reversed(selected_songs):
        playlistBox.delete(index)

def play_from_playlist():
    song = playlistBox.get("anchor")
    if song:
        listBox.selection_clear(0, tk.END)
        listBox.selection_set(playlistBox.curselection())
        play()

def show_playlist():
    listBox.pack_forget()
    playlistBox.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
    show_playlist_button.pack_forget()
    add_playlist_button.pack_forget()
    remove_playlist_button.pack(side=tk.RIGHT, padx=10)
    play_playlist_button.pack(side=tk.RIGHT, padx=10)
    hide_playlist_button.pack(side=tk.RIGHT, padx=10)

def hide_playlist():
    playlistBox.pack_forget()
    listBox.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
    hide_playlist_button.pack_forget()
    remove_playlist_button.pack_forget()
    play_playlist_button.pack_forget()
    add_playlist_button.pack(side=tk.RIGHT, padx=10)
    show_playlist_button.pack(side=tk.RIGHT, padx=10)

# Search widgets
search_frame = tk.Frame(canvas, bg="black")
search_frame.pack(pady=10)

search_label = tk.Label(search_frame, text="Search:", bg="black", fg="white", font=('Mandala Romantic', 14))
search_label.pack(side=tk.LEFT, padx=5)

search_entry = tk.Entry(search_frame, width=40, font=('Mandala Romantic', 14))
search_entry.pack(side=tk.LEFT, padx=5)

search_button = tk.Button(search_frame, text="Search", command=search, bg='grey', fg='white', font=('Mandala Romantic', 14))
search_button.pack(side=tk.LEFT, padx=5)

# Create and pack the widgets
frame = tk.Frame(canvas)
frame.pack(padx=15, pady=15, fill=tk.BOTH, expand=True)

listBox = tk.Listbox(frame, fg="cyan", bg="black", width=100, font=('Mandala Romantic', 16))
listBox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

playlist_frame = tk.Frame(frame)
playlist_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

scrollbar = tk.Scrollbar(frame, orient=tk.VERTICAL, command=listBox.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

listBox.config(yscrollcommand=scrollbar.set)

lable = tk.Label(canvas, text='', bg='black', fg='yellow', font=('Mandala Romantic', 18))
lable.pack(pady=15)

# Playlist listbox
playlistBox = tk.Listbox(playlist_frame, fg="cyan", bg="black", width=100, font=('Mandala Romantic', 16))

playlist_scrollbar = tk.Scrollbar(playlist_frame, orient=tk.VERTICAL, command=playlistBox.yview)
playlist_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

playlistBox.config(yscrollcommand=playlist_scrollbar.set)

# Playback controls

# Track time display
time_label = tk.Label(canvas, text="00:00", bg="black", fg="white", font=('Mandala Romantic', 14))
time_label.pack(pady=5)

top = tk.Frame(canvas, bg="black")

top.pack(padx=10, pady=5, anchor='center')


prevButton = tk.Button(top, text="Prev", image=prev1, bg='white', borderwidth=10, command=prev_song)
prevButton.pack(pady=15, in_=top, side='left')

playButton = tk.Button(top, text="Play", image=play1, bg='blue', borderwidth=10, command=play)
playButton.pack(pady=15, in_=top, side='left')

stopButton = tk.Button(top, text="Stop", image=stop1, bg='red', borderwidth=10, command=stop)
stopButton.pack(pady=15, in_=top, side='left')

pauseButton = tk.Button(top, text="Pause", image=pause1, bg='yellow', borderwidth=10, command=pause)
pauseButton.pack(pady=15, in_=top, side='left')

nextButton = tk.Button(top, text="Next", image=next1, bg='black', borderwidth=10, command=next_song)
nextButton.pack(pady=15, in_=top, side='left')

shuffleButton = tk.Button(top, text="Shuffle", image=shuffle1, bg='gray', borderwidth=10, command=toggle_shuffle)
shuffleButton.pack(pady=15, in_=top, side='left')

repeatButton = tk.Button(top, text="Repeat", image=repeat1, bg='gray', borderwidth=10, command=toggle_repeat)
repeatButton.pack(pady=15, in_=top, side='left')

b_frame = tk.Frame(canvas, bg="black")
b_frame.pack(padx=10, pady=5, anchor='center')

# Volume control
volume_frame = tk.Frame(canvas, bg="black")
volume_frame.pack(pady=5)

volume_label = tk.Label(volume_frame, text="Volume", bg="black", fg="white", font=('Mandala Romantic', 14))
volume_label.pack(side=tk.LEFT, padx=5)

volume_slider = tk.Scale(volume_frame, from_=0, to=100, orient=tk.HORIZONTAL, command=adjust_volume, bg="black", fg="white")
volume_slider.set(50)  # Set initial volume to 50%
volume_slider.pack(side=tk.LEFT)

# Button to show playlist
show_playlist_button = tk.Button(b_frame, text="Show Playlist", command=show_playlist, bg='grey', fg='white', font=('Mandala Romantic', 14))
show_playlist_button.pack(pady=5, side='left')

# Button to hide playlist (hidden initially)
hide_playlist_button = tk.Button(b_frame, text="Hide Playlist", command=hide_playlist, bg='grey', fg='white', font=('Mandala Romantic', 14))
hide_playlist_button.pack_forget()

add_playlist_button = tk.Button(b_frame, text="Add to Playlist", command=add_to_playlist, bg='grey', fg='white', font=('Mandala Romantic', 14))
add_playlist_button.pack(pady=5,in_=b_frame,  side='left')

remove_playlist_button = tk.Button(b_frame, text="Remove from Playlist", command=remove_from_playlist, bg='grey', fg='white', font=('Mandala Romantic', 14))
remove_playlist_button.pack(pady=5,in_=b_frame,  side='left')
remove_playlist_button.pack_forget()

play_playlist_button = tk.Button(b_frame, text="Play from Playlist", command=play_from_playlist, bg='grey', fg='white', font=('Mandala Romantic', 14))
play_playlist_button.pack(pady=5, in_=b_frame, side='left')
play_playlist_button.pack_forget()

# Initialize global variables for shuffle and repeat modes
shuffle_mode = False
repeat_mode = False

# Load all songs into the listbox
for root, dirs, files in os.walk(rootpath):
    for filename in fnmatch.filter(files, pattern):
        listBox.insert(tk.END, filename)

# Start the Tkinter main loop
canvas.mainloop()

