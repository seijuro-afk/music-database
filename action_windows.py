import tkinter as tk
from tkinter import messagebox, ttk
from tkcalendar import DateEntry
from datetime import datetime
import mysql.connector
import fetch

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
        artist_id = fetch.get_create_artist(db, artist_name) if artist_name else None
        album_id = fetch.get_create_album(db, album_name, artist_id) if album_name else None

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

    # Load songs into Treeview based on search input
    def load_songs():
        search_term = search_entry.get()
        songs = fetch.search_songs(db, search_term)

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

def open_add_album_window(db, root):
    # Create new Toplevel window for adding an album
    add_album_window = tk.Toplevel(root)
    add_album_window.title("Add New Album")
    add_album_window.geometry("700x450")
    add_album_window.config(bg="#1c1c1c")

    # Configure layout: left for song table, right for album details
    left_frame = tk.Frame(add_album_window, bg="#1c1c1c")
    left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(10, 5), pady=10)

    right_frame = tk.Frame(add_album_window, bg="#1c1c1c")
    right_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=(5, 10), pady=10)

    # Song Table
    columns = ("Title", "Duration (mins)")
    song_tree = ttk.Treeview(left_frame, columns=columns, show="headings", selectmode="extended")
    song_tree.pack(expand=True, fill=tk.BOTH)

    for col in columns:
        song_tree.heading(col, text=col)
    song_tree.column("Title", width=200, anchor="w")
    song_tree.column("Duration (mins)", width=120, anchor="center")

    # Add button to add a new song entry to the table
    def add_song():
        song_tree.insert("", "end", values=("Enter Title", "Enter Duration"))

    add_song_button = tk.Button(left_frame, text="Add Song", command=add_song, bg="#555555", fg="white")
    add_song_button.pack(pady=10)

    # Make table editable
    def edit_cell(event):
        selected_item = song_tree.selection()
        if not selected_item:
            return

        item = selected_item[0]
        col = song_tree.identify_column(event.x)
        col_num = int(col.replace("#", "")) - 1

        # Get current cell value
        x, y, width, height = song_tree.bbox(item, col)
        value = song_tree.item(item, "values")[col_num]

        # Create an Entry widget for editing
        edit_widget = tk.Entry(left_frame)
        edit_widget.insert(0, value)
        edit_widget.select_range(0, tk.END)
        edit_widget.focus()
        edit_widget.place(x=x, y=y, width=width, height=height)

        # Update cell value on Enter or focus out
        def save_edit(event=None):
            new_value = edit_widget.get()
            song_values = list(song_tree.item(item, "values"))
            song_values[col_num] = new_value
            song_tree.item(item, values=song_values)
            edit_widget.destroy()

        edit_widget.bind("<Return>", save_edit)
        edit_widget.bind("<FocusOut>", lambda e: edit_widget.destroy())

    song_tree.bind("<Double-1>", edit_cell)

    # Album Details 
    label_font = ("Arial", 12)
    entry_font = ("Arial", 11)
    fields = {}

    tk.Label(right_frame, text="Album Title:", font=label_font, fg="white", bg="#1c1c1c").pack(anchor="w", pady=(20, 5))
    fields["Title"] = tk.Entry(right_frame, font=entry_font, width=25)
    fields["Title"].pack(pady=5)

    tk.Label(right_frame, text="Artist:", font=label_font, fg="white", bg="#1c1c1c").pack(anchor="w", pady=(10, 5))
    fields["Artist"] = tk.Entry(right_frame, font=entry_font, width=25)
    fields["Artist"].pack(pady=5)

    tk.Label(right_frame, text="Date Created:", font=label_font, fg="white", bg="#1c1c1c").pack(anchor="w", pady=(10, 5))
    fields["Date"] = DateEntry(right_frame, font=entry_font, width=22, background="darkblue", foreground="white", borderwidth=2)
    fields["Date"].set_date(datetime.now())
    fields["Date"].pack(pady=5)

    # Back and Confirm Buttons
    def confirm_album():
        confirm = messagebox.askyesno("Confirm", "Are you sure you want to add this album?")
        if confirm:
            album_title = fields["Title"].get()
            artist = fields["Artist"].get()
            created_at = fields["Date"].get_date()

            # Gather song data from the table
            songs = []
            for item in song_tree.get_children():
                song_data = song_tree.item(item)["values"]
                songs.append(song_data)

            # Insert album and songs into the database
            try:
                cursor = db.cursor()
                artist_id = fetch.get_create_artist(db, artist)
                album_id = fetch.get_create_album(db, album_title, artist_id)

                for song in songs:
                    song_title, duration = song
                    cursor.execute(
                        "INSERT INTO Songs (title, artist_id, album_id, duration, created_at) VALUES (%s, %s, %s, %s, %s)",
                        (song_title, artist_id, album_id, duration, created_at)
                    )

                db.commit()
                messagebox.showinfo("Success", "Album and songs added successfully!")
                add_album_window.destroy()
            except Exception as e:
                db.rollback()
                messagebox.showerror("Error", f"Failed to add album and songs: {e}")
            finally:
                cursor.close()

    def go_back():
        add_album_window.destroy()

    back_button = tk.Button(right_frame, text="Back", command=go_back, bg="#333333", fg="white", font=label_font)
    back_button.pack(pady=(30, 10))

    confirm_button = tk.Button(right_frame, text="Confirm", command=confirm_album, bg="#4CAF50", fg="white", font=label_font)
    confirm_button.pack(pady=10)