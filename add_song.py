import tkinter as tk
from tkinter import messagebox
from tkcalendar import DateEntry
from datetime import datetime
import mysql.connector

# Handle adding new artist or album if they do not exist
def get_or_create_artist_id(db, artist_name):
    cursor = db.cursor()
    cursor.execute("SELECT artist_id FROM Artists WHERE name = %s", (artist_name,))
    result = cursor.fetchone()
    if result:
        return result[0]  # Return existing artist_id
    else:
        cursor.execute("INSERT INTO Artists (name) VALUES (%s)", (artist_name,))
        db.commit()
        return cursor.lastrowid  # Return new artist_id

def get_or_create_album_id(db, album_name, artist_id):
    cursor = db.cursor()
    cursor.execute("SELECT id FROM Albums WHERE title = %s AND artist_id = %s", (album_name, artist_id))
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
        artist_id = get_or_create_artist_id(db, artist_name) if artist_name else None
        album_id = get_or_create_album_id(db, album_name, artist_id) if album_name else None

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