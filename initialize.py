# Main GUI initialiation

import tkinter as tk
from tkinter import ttk
import action_windows
import fetch

def initialize(db, root, username):

    # Function to load albums into the albums panel
    def load_albums():
        for album in fetch.albums(db):
            album_id, album_name = album if len(album) > 1 else (album[0], album[0])
            albums_listbox.insert(tk.END, album_name)
            albums_listbox.album_ids.append(album_id)

    # Function to load songs into the songs table view
    def load_songs(album_id=None):
        # Clear current table view content
        for row in treeview.get_children():
            treeview.delete(row)
        # Fetch and populate songs
        songs = fetch.songs_by_album(db, album_id)
        for title, artist, album, genre, duration in songs:
            treeview.insert("", tk.END, values=(title, artist, album, genre, duration))

    # Event handler for album selection
    def on_album_select(event):
        selected_index = albums_listbox.curselection()
        if not selected_index:
            return
        album_id = albums_listbox.album_ids[selected_index[0]]
        load_songs(album_id)

    # Create main frames
    left_frame = tk.Frame(root, bg="#1c1c1c", width=200)
    left_frame.pack(side=tk.LEFT, fill=tk.Y)

    middle_frame = tk.Frame(root, bg="#1c1c1c")
    middle_frame.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

    right_frame = tk.Frame(root, bg="#1c1c1c", width=200)
    right_frame.pack(side=tk.RIGHT, fill=tk.Y)

    # Left panel - Albums
    albums_label = tk.Label(left_frame, text="Albums", font=("Helvetica", 14), bg="#1c1c1c", fg="white")
    albums_label.pack(pady=10)

    # Album listbox with custom attribute for IDs
    albums_listbox = tk.Listbox(left_frame, bg="#333333", fg="white", font=("Helvetica", 12))
    albums_listbox.pack(pady=5, padx=5, fill=tk.BOTH, expand=True)
    albums_listbox.album_ids = []  # Store album IDs for reference
    albums_listbox.bind("<<ListboxSelect>>", on_album_select)

    # Left panel - Playlists
    playlists_label = tk.Label(left_frame, text="Playlists", font=("Helvetica", 14), bg="#1c1c1c", fg="white")
    playlists_label.pack(pady=10)

    playlists_listbox = tk.Listbox(left_frame, bg="#333333", fg="white", font=("Helvetica", 12))
    playlists_listbox.pack(pady=5, padx=5, fill=tk.BOTH, expand=True)

    # Middle panel - Songs
    songs_label = tk.Label(middle_frame, text="Songs", font=("Helvetica", 14), bg="#1c1c1c", fg="white")
    songs_label.pack(pady=5)

    # Create a frame for the middle panel (songs)
    middle_frame = tk.Frame(middle_frame, bg="#1c1c1c")
    middle_frame.pack(side=tk.LEFT, fill=tk.Y, expand=True)

    # Create a Treeview for the songs
    columns = ("Song Title", "Artist", "Album", "Genre", "Duration")
    treeview = ttk.Treeview(middle_frame, columns=columns, show='headings', height=25)
    treeview.pack(pady=10, padx=10)

    # Configure the Treeview style
    style = ttk.Style()
    style.configure("Treeview",
                    background="#333333",
                    foreground="white",
                    fieldbackground="#333333")

    # Define the column headings
    for col in columns:
        treeview.heading(col, text=col)
        treeview.column(col, anchor=tk.CENTER)

    # Set the widths and alignments of each column
    treeview.column("Song Title", width=200, anchor="w")
    treeview.column("Artist", width=150, anchor="center")
    treeview.column("Album", width=150, anchor="center")
    treeview.column("Genre", width=100, anchor="center")
    treeview.column("Duration", width=70, anchor="center") 

    # Initialize GUI content
    load_albums()  # Load albums list
    load_songs()   # Load all songs initially

    # Right panel - Buttons
    right_label = tk.Label(right_frame, text=f"Welcome, {username}", font=("Helvetica", 12), bg="#1c1c1c", fg="white")
    right_label.pack(pady=10)

    right_label = tk.Label(right_frame, text="Admin", font=("Helvetica", 9), bg="#1c1c1c", fg="white")
    right_label.pack(pady=10)


    # Add Song button in the main window
    add_song_button = tk.Button(right_frame, text="Add Song", command=lambda: action_windows.open_add_song_window(db, root), bg="#555555", fg="white", font=("Helvetica", 12))
    add_song_button.pack(padx=10, pady=10)

    remove_song_button = tk.Button(right_frame, text="Remove Song", command=lambda: action_windows.open_remove_song_window(db, root), bg="#555555", fg="white", font=("Helvetica", 12))
    remove_song_button.pack(pady=10, padx=10)

    add_album_button = tk.Button(right_frame, text="Add Album", command=lambda: action_windows.open_add_album_window(db, root), bg="#555555", fg="white", font=("Helvetica", 12))
    add_album_button.pack(padx=10, pady=10)

    right_label = tk.Label(right_frame, text="User", font=("Helvetica", 9), bg="#1c1c1c", fg="white")
    right_label.pack(pady=10)

    upload_album_button = tk.Button(right_frame, text="Upload Album", command=lambda: action_windows.open_upload_album_window(db, root, username), bg="#555555", fg="white", font=("Helvetica", 12))
    upload_album_button.pack(padx=10, pady=10)