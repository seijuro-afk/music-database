import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

class MusicPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("Music Player")
        self.root.configure(bg="black")

        # Playlist frame
        self.playlist_frame = tk.Frame(root, bg="#2e2e2e")
        self.playlist_frame.place(x=0, y=0, width=200, height=600)

        self.playlist_label = tk.Label(self.playlist_frame, text="Playlist", bg="#2e2e2e", fg="white")
        self.playlist_label.pack(pady=10)

        self.playlist_listbox = tk.Listbox(self.playlist_frame, bg="#333333", fg="white")
        self.playlist_listbox.pack(fill=tk.BOTH, expand=True, pady=20)

        # Account center button (borderless) with adjusted top margin
        self.account_button = tk.Button(root, text="Account Center", bg="#2e2e2e", fg="white", relief=tk.FLAT)
        self.account_button.place(x=600, y=0, width=200, height=100)  # Restoring y value to 0 to align at the top

        # Queue frame
        self.queue_frame = tk.Frame(root, bg="#2e2e2e")
        self.queue_frame.place(x=600, y=100, width=200, height=500)  # Adjusted y value for the queue frame

        self.queue_label = tk.Label(self.queue_frame, text="Queue", bg="#2e2e2e", fg="white")
        self.queue_label.pack(pady=10)

        self.queue_listbox = tk.Listbox(self.queue_frame, bg="#333333", fg="white")
        self.queue_listbox.pack(fill=tk.BOTH, expand=True, pady=20)

        # Latest songs and albums frame
        self.latest_frame = tk.Frame(root, bg="#2e2e2e")
        self.latest_frame.place(x=200, y=0, width=400, height=500)

        self.latest_label = tk.Label(self.latest_frame, text="Latest Songs and Albums", bg="#2e2e2e", fg="white")
        self.latest_label.pack(pady=10)

        # Music player controls frame
        self.controls_frame = tk.Frame(root, bg="#2e2e2e")
        self.controls_frame.place(x=200, y=500, width=400, height=100)

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
        self.previous_button.place(relx=0.25, rely=0.5, anchor=tk.CENTER)

        self.play_button = tk.Button(self.controls_frame, image=self.play_pause_image, bg="#2e2e2e", relief=tk.FLAT)
        self.play_button.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        self.next_button = tk.Button(self.controls_frame, image=self.next_image, bg="#2e2e2e", relief=tk.FLAT)
        self.next_button.place(relx=0.75, rely=0.5, anchor=tk.CENTER)

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("800x600")
    app = MusicPlayer(root)
    root.mainloop()
