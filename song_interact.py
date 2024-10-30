import tkinter as tk
from tkinter import messagebox, ttk
from tkcalendar import DateEntry
from datetime import datetime
import mysql.connector

# Handle adding new artist or album
def get_create_artist(db, artist_name):
    cursor = db.cursor()
    cursor.execute("SELECT artist_id FROM Artists WHERE name = %s", (artist_name,))
    result = cursor.fetchone()
    if result:
        return result[0]  # Return existing artist_id
    else:
        cursor.execute("INSERT INTO Artists (name) VALUES (%s)", (artist_name,))
        db.commit()
        return cursor.lastrowid  # Return new artist_id

def get_create_album(db, album_name, artist_id):
    cursor = db.cursor()
    cursor.execute("SELECT album_id FROM Albums WHERE title = %s AND artist_id = %s", (album_name, artist_id))
    result = cursor.fetchone()
    if result:
        return result[0]  # Return existing album_id
    else:
        cursor.execute("INSERT INTO Albums (title, artist_id) VALUES (%s, %s)", (album_name, artist_id))
        db.commit()
        return cursor.lastrowid  # Return new album_id

# Function to open the Add Song window
def open_add_song_window(db, root):
    add_song_window = tk.Toplevel(root)
    add_song_window.title("Add New Song")
    add_song_window.geometry("400x450")
    add_song_window.config(bg="#1c1c1c")

    fields = {
        "Title": tk.Entry(add_song_window, width=30),
        "Artist Name": tk.Entry(add_song_window, width=30),
        "Album": tk.Entry(add_song_window, width=30),
        "Genre": tk.Entry(add_song_window, width=30),
        "Duration (mins)": tk.Entry(add_song_window, width=30),
    }

    for idx, (label, entry) in enumerate(fields.items()):
        tk.Label(add_song_window, text=label, font=("Helvetica", 12), bg="#1c1c1c", fg="white").grid(row=idx, column=0, padx=10, pady=5, sticky="e")
        entry.grid(row=idx, column=1, padx=10, pady=5)

    tk.Label(add_song_window, text="Created At", font=("Helvetica", 12), bg="#1c1c1c", fg="white").grid(row=len(fields), column=0, padx=10, pady=5, sticky="e")
    created_at_date = DateEntry(add_song_window, width=12, background="darkblue", foreground="white", date_pattern="dd/mm/yyyy")
    created_at_date.grid(row=len(fields), column=1, padx=10, pady=5, sticky="w")

    hour_entry = tk.Entry(add_song_window, width=3)
    hour_entry.insert(0, "00")
    hour_entry.grid(row=len(fields), column=1, sticky="w", padx=(135, 0))  # Aligning beside DateEntry

    minute_entry = tk.Entry(add_song_window, width=3)
    minute_entry.insert(0, "00")
    minute_entry.grid(row=len(fields), column=1, sticky="w", padx=(175, 0))  # Aligning beside Hour Entry

    def add_song():
        title = fields["Title"].get()
        artist_name = fields["Artist Name"].get()
        album_name = fields["Album"].get()
        genre = fields["Genre"].get()
        duration = fields["Duration (mins)"].get()
        created_at_date_value = created_at_date.get()
        
        # Default time if empty
        hour = hour_entry.get() or "00"
        minute = minute_entry.get() or "00"
        
        # Validation checks
        if not title or not duration or not created_at_date_value:
            messagebox.showerror("Input Error", "Please fill out all required fields (Title, Duration, Created At Date).")
            return

        # Combine date and time
        created_at_str = f"{created_at_date_value} {hour}:{minute}"
        try:
            created_at = datetime.strptime(created_at_str, "%d/%m/%Y %H:%M")
        except ValueError:
            messagebox.showerror("Date Format Error", "There was an error in date/time format.")
            return

        # Process artist and album creation if they don't exist
        artist_id = get_create_artist(db, artist_name) if artist_name else None
        album_id = get_create_album(db, album_name, artist_id) if album_name else None

        cursor = db.cursor()
        try:
            cursor.execute(
                """
                INSERT INTO Songs (title, artist_id, album_id, genre, duration, created_at)
                VALUES (%s, %s, %s, %s, %s, %s)
                """,
                (title, artist_id, album_id, genre, duration, created_at)
            )
            db.commit()
            messagebox.showinfo("Success", "Song added successfully!")
            add_song_window.destroy()
        except mysql.connector.Error as err:
            db.rollback()
            messagebox.showerror("Database Error", f"An error occurred: {err}")
        finally:
            cursor.close()

    submit_button = tk.Button(add_song_window, text="Add Song", command=add_song, bg="#555555", fg="white", font=("Helvetica", 12))
    submit_button.grid(row=len(fields) + 2, column=0, columnspan=2, pady=20)

    close_button = tk.Button(add_song_window, text="Back", command=add_song_window.destroy, bg="#555555", fg="white", font=("Helvetica", 12))
    close_button.grid(row=len(fields) + 3, column=0, columnspan=2, pady=5)


def open_remove_song_window(db, root):
    remove_song_window = tk.Toplevel(root)
    remove_song_window.title("Remove Song")
    remove_song_window.geometry("600x400")
    remove_song_window.config(bg="#1c1c1c")

    # Search bar
    tk.Label(remove_song_window, text="Search Songs", bg="#1c1c1c", fg="white", font=("Helvetica", 12)).pack(pady=10)
    search_entry = tk.Entry(remove_song_window, width=40)
    search_entry.pack(pady=5)

    # Table to display songs
    columns = ("Song ID", "Title", "Artist", "Album")
    song_tree = ttk.Treeview(remove_song_window, columns=columns, show="headings", selectmode="extended")
    song_tree.pack(pady=10, padx=10, expand=True, fill=tk.BOTH)

    # Define column headings
    for col in columns:
        song_tree.heading(col, text=col)
    song_tree.column("Song ID", width=80, anchor="center")
    song_tree.column("Title", width=200, anchor="w")
    song_tree.column("Artist", width=150, anchor="center")
    song_tree.column("Album", width=150, anchor="center")

    # Fetch songs from the database
    def fetch_songs(search_term=""):
        cursor = db.cursor()
        query = """
            SELECT s.song_id, s.title, a.name AS artist, al.title AS album
            FROM Songs s
            LEFT JOIN Artists a ON s.artist_id = a.artist_id
            LEFT JOIN Albums al ON s.album_id = al.album_id
            WHERE s.title LIKE %s
            """
        cursor.execute(query, (f"%{search_term}%",))
        songs = cursor.fetchall()
        cursor.close()
        return songs

    # Load songs into Treeview based on search input
    def load_songs():
        search_term = search_entry.get()
        songs = fetch_songs(search_term)

        # Clear current entries in the tree
        for item in song_tree.get_children():
            song_tree.delete(item)

        # Insert new filtered songs into table
        for song in songs:
            song_tree.insert("", "end", values=song)

    # Event listener for search input changes
    search_entry.bind("<KeyRelease>", lambda event: load_songs())

    # Confirm deletion dialog and remove selected songs
    def confirm_and_remove_songs():
        selected_items = song_tree.selection()
        if not selected_items:
            messagebox.showwarning("Selection Error", "Please select at least one song to remove.")
            return

        # Gather IDs of selected songs
        song_ids = [song_tree.item(item)["values"][0] for item in selected_items]

        # Confirm removal
        if messagebox.askyesno("Confirm Removal", "Are you sure you want to remove the selected songs? This action cannot be undone."):
            cursor = db.cursor()
            try:
                cursor.executemany("DELETE FROM Songs WHERE song_id = %s", [(song_id,) for song_id in song_ids])
                db.commit()
                messagebox.showinfo("Success", f"{len(song_ids)} songs have been removed.")
                # load_songs()  # Reload to reflect changes
            except mysql.connector.Error as err:
                db.rollback()
                messagebox.showerror("Database Error", f"An error occurred: {err}")
            finally:
                cursor.close()

    # Remove button
    remove_button = tk.Button(remove_song_window, text="Remove Selected Songs", command=confirm_and_remove_songs, bg="#555555", fg="white", font=("Helvetica", 12))
    remove_button.pack(pady=20)

    # Load songs initially
    load_songs()