import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import mysql.connector

connection = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "add password here",
    database = "add database here"
)

class MusicPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("Music Player")
        self.root.configure(bg="black")

        # Main frame to ensure consistent background
        self.main_frame = tk.Frame(root, bg="#2e2e2e")
        self.main_frame.place(x=0, y=0, width=800, height=600)

        # Create a canvas for the rounded border
        self.search_canvas = tk.Canvas(self.main_frame, bg="#dddddd", highlightthickness=0)
        self.search_canvas.place(relx=0.5, rely=0, anchor=tk.N, width=410, height=40)

        # Draw a rounded rectangle
        self.create_rounded_rectangle(self.search_canvas, 5, 5, 405, 35, 10, outline="#2e2e2e", width=2)

        # Search frame on the canvas
        self.search_frame = tk.Frame(self.search_canvas, bg="#2e2e2e")
        self.search_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER, width=400, height=30)

        self.search_entry = tk.Entry(self.search_frame, bg="#333333", fg="white", relief=tk.FLAT)
        self.search_entry.pack(side=tk.LEFT, padx=10, pady=5, fill=tk.X, expand=True)

        # Placeholder text
        self.search_placeholder_text = "Search here..."
        self.search_entry.insert(0, self.search_placeholder_text)
        self.search_entry.bind("<FocusIn>", self.on_entry_click)
        self.search_entry.bind("<FocusOut>", self.on_focus_out)

        self.search_button = tk.Button(self.search_frame, text="Search", bg="#2e2e2e", fg="white", relief=tk.FLAT)
        self.search_button.pack(side=tk.RIGHT, padx=10, pady=5)

        # Playlist frame
        self.playlist_frame = tk.Frame(self.main_frame, bg="#2e2e2e")
        self.playlist_frame.place(x=0, y=50, width=200, height=550)

        self.playlist_label = tk.Label(self.playlist_frame, text="Playlist", bg="#2e2e2e", fg="white")
        self.playlist_label.pack(pady=10)

        self.playlist_listbox = tk.Listbox(self.playlist_frame, bg="#333333", fg="white")
        self.playlist_listbox.pack(fill=tk.BOTH, expand=True, pady=20)

        # Account center button (borderless)
        self.account_button = tk.Button(self.main_frame, text="Account Center", bg="#2e2e2e", fg="white", relief=tk.FLAT)
        self.account_button.place(x=600, y=50, width=200, height=50)

        # Queue frame
        self.queue_frame = tk.Frame(self.main_frame, bg="#2e2e2e")
        self.queue_frame.place(x=600, y=100, width=200, height=500)

        self.queue_label = tk.Label(self.queue_frame, text="Queue", bg="#2e2e2e", fg="white")
        self.queue_label.pack(pady=10)

        self.queue_listbox = tk.Listbox(self.queue_frame, bg="#333333", fg="white")
        self.queue_listbox.pack(fill=tk.BOTH, expand=True, pady=20)

        # Latest songs and albums frame
        self.latest_frame = tk.Frame(self.main_frame, bg="#2e2e2e")
        self.latest_frame.place(x=200, y=50, width=400, height=450)

        self.latest_label = tk.Label(self.latest_frame, text="Latest Songs and Albums", bg="#2e2e2e", fg="white")
        self.latest_label.pack(pady=10)

        # Music player controls frame
        self.controls_frame = tk.Frame(self.main_frame, bg="#2e2e2e")
        self.controls_frame.place(x=200, y=500, width=400, height=100)

        # Custom progress bar
        self.progress_canvas = tk.Canvas(self.controls_frame, bg="#2e2e2e", highlightthickness=0)
        self.progress_canvas.place(relx=0.5, rely=0.2, anchor=tk.CENTER, width=380, height=15)

        self.create_rounded_rectangle(self.progress_canvas, 5, 5, 375, 10, 7, fill="#808080", outline="")

        # Dummy progress for demonstration
        self.progress = self.progress_canvas.create_rectangle(5, 5, 50, 10, fill="#999999", outline="")

        # Load and resize images using PIL
        self.previous_image = Image.open("prev.png")
        self.previous_image = self.previous_image.resize((50, 50), Image.LANCZOS)  # Adjust the size as needed
        self.previous_image = ImageTk.PhotoImage(self.previous_image)

        self.play_pause_image = Image.open("play.png")
        self.play_pause_image = self.play_pause_image.resize((50, 50), Image.LANCZOS)
        self.play_pause_image = ImageTk.PhotoImage(self.play_pause_image)

        self.next_image = Image.open("next.png")
        self.next_image = self.next_image.resize((50, 50), Image.LANCZOS)
        self.next_image = ImageTk.PhotoImage(self.next_image)

        # Adjust the control buttons with icons
        self.previous_button = tk.Button(self.controls_frame, image=self.previous_image, bg="#2e2e2e", relief=tk.FLAT)
        self.previous_button.place(relx=0.3, rely=0.7, anchor=tk.CENTER)

        self.play_button = tk.Button(self.controls_frame, image=self.play_pause_image, bg="#2e2e2e", relief=tk.FLAT)
        self.play_button.place(relx=0.5, rely=0.7, anchor=tk.CENTER)

        self.next_button = tk.Button(self.controls_frame, image=self.next_image, bg="#2e2e2e", relief=tk.FLAT)
        self.next_button.place(relx=0.7, rely=0.7, anchor=tk.CENTER)

        self.like_button = tk.Button(self.controls_frame, text="Like", bg="#2e2e2e", fg="white", relief=tk.FLAT, command=self.toggle_like)
        self.like_button.place(relx=0.9, rely=0.7, anchor=tk.CENTER)

    def create_rounded_rectangle(self, canvas, x1, y1, x2, y2, radius=25, **kwargs):
        points = [x1+radius, y1,
                  x1+radius, y1,
                  x2-radius, y1,
                  x2-radius, y1,
                  x2, y1,
                  x2, y1+radius,
                  x2, y1+radius,
                  x2, y2-radius,
                  x2, y2-radius,
                  x2, y2,
                  x2-radius, y2,
                  x2-radius, y2,
                  x1+radius, y2,
                  x1+radius, y2,
                  x1, y2,
                  x1, y2-radius,
                  x1, y2-radius,
                  x1, y1+radius,
                  x1, y1+radius,
                  x1, y1]

        return canvas.create_polygon(points, **kwargs, smooth=True)

    def on_entry_click(self, event):
        if self.search_entry.get() == self.search_placeholder_text:
            self.search_entry.delete(0, "end")
            self.search_entry.config(fg="white")

    def on_focus_out(self, event):
        if self.search_entry.get() == "":
            self.search_entry.insert(0, self.search_placeholder_text)
            self.search_entry.config(fg="grey")

    def toggle_like(self):
        if self.like_button.config('text')[-1] == 'Like':
            self.like_button.config(text='Unlike')
        else:
            self.like_button.config(text='Like')

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("800x600")
    app = MusicPlayer(root)
    root.mainloop()