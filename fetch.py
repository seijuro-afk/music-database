# This file interacts and fetches data from the Music Library Database
import mysql.connector
from tkinter import messagebox

# Connect to MySQLs
def create_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',       # Replace with your MySQL username
            password='pissword',    # Replace with your MySQL password
            database='musiclibrarydb'     # Replace with your database name
        )
        return connection
    except mysql.connector.Error as e:
        messagebox.showerror("Database Error", f"Error connecting to database: {e}")
        return None

# Function to fetch all albums and add "All Songs"
def albums(db):
    cursor = db.cursor()
    cursor.execute("SELECT album_id, title FROM Albums")
    albums = cursor.fetchall()
    cursor.close()
    # Insert "All Songs" option at the beginning of the list
    return [("All Songs",)] + albums

# Function to fetch songs, filtered by album if specified
def songs_by_album(db, album_id=None):
    cursor = db.cursor()
    if album_id == "All Songs" or album_id is None:
        cursor.execute("""
            SELECT s.title, a.name AS artist, al.title AS album, s.genre, s.duration
            FROM Songs s
            JOIN Artists a ON s.artist_id = a.artist_id
            JOIN Albums al ON s.album_id = al.album_id
        """)
    else:
        cursor.execute("""
            SELECT s.title, a.name AS artist, al.title AS album, s.genre, s.duration
            FROM Songs s
            JOIN Artists a ON s.artist_id = a.artist_id
            JOIN Albums al ON s.album_id = al.album_id
            WHERE al.album_id = %s
        """, (album_id,))
    songs = cursor.fetchall()
    cursor.close()
    return songs

# Fetch/Search songs from the database
def search_songs(db, search_term=""):
    cursor = db.cursor()
    query = """
        SELECT s.song_id, s.title, a.name AS artist, al.title AS album, s.genre, s.duration
        FROM Songs s
        LEFT JOIN Artists a ON s.artist_id = a.artist_id
        LEFT JOIN Albums al ON s.album_id = al.album_id
        WHERE s.title LIKE %s
        """
    cursor.execute(query, (f"%{search_term}%",))
    songs = cursor.fetchall()
    cursor.close()
    return songs

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