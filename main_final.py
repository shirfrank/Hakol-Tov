import tkinter as tk
from tkinter import messagebox, simpledialog, PhotoImage
import subprocess
import json
import os
from PIL import Image, ImageTk, ImageFont, ImageDraw


# Paths to your game scripts
squeaky_bird_SCRIPT = "squeaky_bird_final.py"  # Replace with the actual file name
pitch_perfect_SCRIPT = "pitch_perfect_final.py"  # Replace with the actual file name
voice_target_SCRIPT = "voice_target_final.py"  # Replace with the actual file name

# Paths to my game jsons
SQUEAKY_BIRD_LEADERBOARD_FILE = "squeaky_bird_leaderboard.json"
PITCH_PERFECT_LEADERBOARD_FILE = "pitch_perfect_leaderboard.json"
VOICE_TARGET_LEADERBOARD_FILE = "voice_target_leaderboard.json"

THRESHOLD_FILE = "thresholds.json"  # File to store threshold values

# User authentication

ADMINS = {
    "clinait": {"password": "", "is_admin": True},
}
USERS = {
    "shir": {"password": "", "is_admin": False},
    "tom": {"password": "", "is_admin": False},
    "ofri": {"password": "", "is_admin": False},
    "mai": {"password": "", "is_admin": False},
    "shaked": {"password": "", "is_admin": False},
}
# Helper function to run a game script
def run_game(script_name, threshold_db=None):
    try:
        # Run the game script
        if threshold_db is not None:
            subprocess.run(
                ["python", script_name, str(threshold_db)],
                text=True,
                capture_output=True,
            )
        else:
            subprocess.run(
                ["python", script_name],
                text=True,
                capture_output=True,
            )

        # Read the score from the JSON file
        if script_name == "squeaky_bird_final.py":
            with open(SQUEAKY_BIRD_LEADERBOARD_FILE, "r") as score_file:
                data = json.load(score_file)
                return data.get("score", 0)
        elif script_name == "pitch_perfect_final.py":
            with open(PITCH_PERFECT_LEADERBOARD_FILE, "r") as score_file:
                data = json.load(score_file)
                return data.get("score", 0)
        elif script_name == "voice_target_final.py":
            with open(VOICE_TARGET_LEADERBOARD_FILE, "r") as score_file:
                data = json.load(score_file)
                return data.get("score", 0)
        else:
            return 0

    except Exception as e:
        messagebox.showerror("Error", f"Could not start the game or read the score: {e}")
        return 0  # Return 0 if there was an error


# Helper function to save leaderboard
def save_leaderboard(game, data):
    if game == "squeaky_bird_final":
        file_path = SQUEAKY_BIRD_LEADERBOARD_FILE
    elif game == "pitch_perfect_final":
        file_path = PITCH_PERFECT_LEADERBOARD_FILE
    elif game == "voice_target_final":
        file_path = VOICE_TARGET_LEADERBOARD_FILE
    else:
        return

    with open(file_path, "w") as file:
        json.dump(data, file, indent=4)


# Helper function to load thresholds
def load_thresholds():
    if os.path.exists(THRESHOLD_FILE):
        with open(THRESHOLD_FILE, "r") as file:
            return json.load(file)
    return {}

# Helper function to save thresholds
def save_thresholds(data):
    with open(THRESHOLD_FILE, "w") as file:
        json.dump(data, file, indent=4)


# Main GUI class
class GameApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Game Hub")
        self.logged_in_user = None
        self.leaderboard = {}  # Initialize as an empty dictionary
        self.thresholds = load_thresholds()

        # Set the window size and background color
        self.root.attributes("-fullscreen", True)
        self.root.configure(bg="black")  # Black background
        self.create_login_screen()

    def create_login_screen(self):
        self.clear_screen()

        # Styling
        label_style = {"bg": "black", "fg": "#61dafb", "font": ("Bangers Regular", 20)}
        entry_style = {"font": ("Bangers Regular", 14)}
        button_style = {"font": ("Bangers Regular", 14), "bg": "#61dafb", "fg": "black"}

        # Add the logo
        try:
            logo_path = r"C:\Users\97254\OneDrive - mail.tau.ac.il\שולחן העבודה\לימודים\שנה ד\hackathon\logo.png"
            logo_image = PhotoImage(file=logo_path)
            logo_label = tk.Label(self.root, image=logo_image, bg="black")
            logo_label.image = logo_image  # Keep a reference to prevent garbage collection
            logo_label.pack(side="top", pady=10)  # Adjust padding to position higher
        except Exception as e:
            tk.Label(self.root, text="Logo could not be loaded", **label_style).pack(pady=20)

        # Login form
        tk.Label(self.root, text="Username", **label_style).pack(pady=10)
        username_entry = tk.Entry(self.root, **entry_style)
        username_entry.pack(pady=10)

        tk.Label(self.root, text="Password", **label_style).pack(pady=10)
        password_entry = tk.Entry(self.root, show="*", **entry_style)
        password_entry.pack(pady=10)

        def login():
            username = username_entry.get()
            password = password_entry.get()
            user = USERS.get(username) or ADMINS.get(username)

            if user and user["password"] == password:
                self.logged_in_user = username
                self.is_admin = user["is_admin"]
                self.create_landing_screen()
            else:
                messagebox.showerror("Login Failed", "Invalid username or password")

        # Login button
        tk.Button(self.root, text="Login", command=login, **button_style).pack(pady=10)
        # Quit button
        tk.Button(self.root, text=" Quit ", command=self.root.quit, **button_style).pack(pady=10)

    def create_landing_screen(self):
        self.clear_screen()

        # Styling
        label_style = {"bg": "black", "fg": "#61dafb", "font": ("Bangers Regular", 24, "bold")}
        button_style = {"font": ("Bangers Regular", 16), "bg": "#61dafb", "fg": "#282c34", "width": 30}

        tk.Label(self.root, text=f"Welcome, {self.logged_in_user}!", **label_style).pack(pady=30)

        # Frame to organize buttons
        button_frame = tk.Frame(self.root, bg="black")
        button_frame.pack(pady=20)

        if not self.is_admin:
            # User view: Game buttons and their leaderboards side by side
            # Row 1: Squeaky Bird
            tk.Button(button_frame, text="Play Squeaky Bird", command=self.play_game_squeaky, **button_style).grid(row=0,
                                                                                                            column=0,
                                                                                                            padx=20,
                                                                                                            pady=10)
            tk.Button(
                button_frame,
                text="Squeaky Bird Zone",
                command=lambda: self.create_leaderboard_screen(SQUEAKY_BIRD_LEADERBOARD_FILE, "Squeaky Bird_final"),
                **button_style
            ).grid(row=0, column=1, padx=20, pady=10)

            # Row 2: Pitch Perfect
            tk.Button(button_frame, text="Play Pitch Perfect", command=self.play_game_pitch_perfect,
                      **button_style).grid(row=1, column=0, padx=20, pady=10)
            tk.Button(
                button_frame,
                text="Pitch Perfect Zone",
                command=lambda: self.create_leaderboard_screen(PITCH_PERFECT_LEADERBOARD_FILE, "Pitch Perfect_final"),
                **button_style
            ).grid(row=1, column=1, padx=20, pady=10)

            # Row 3: Voice Target
            tk.Button(button_frame, text="Play Voice Target", command=self.play_game_voice_target,
                      **button_style).grid(row=2, column=0, padx=20, pady=10)
            tk.Button(
                button_frame,
                text="Voice Target Zone",
                command=lambda: self.create_leaderboard_screen(VOICE_TARGET_LEADERBOARD_FILE, "Voice Target_final"),
                **button_style
            ).grid(row=2, column=1, padx=20, pady=10)
        else:
            # Admin view: Show only leaderboard buttons
            tk.Button(button_frame, text="Squeaky Bird Leaderboard",
                      command=lambda: self.create_leaderboard_screen(SQUEAKY_BIRD_LEADERBOARD_FILE, "squeaky_bird_final"), **button_style).grid(row=0,
                                                                                                           column=0,
                                                                                                           padx=20,
                                                                                                           pady=10)
            tk.Button(button_frame, text="Pitch Perfect Leaderboard",
                      command=lambda: self.create_leaderboard_screen(PITCH_PERFECT_LEADERBOARD_FILE, "pitch_perfect_final"), **button_style).grid(row=1,
                                                                                                            column=0,
                                                                                                            padx=20,
                                                                                                            pady=10)
            tk.Button(button_frame, text="Voice Target Leaderboard",
                      command=lambda: self.create_leaderboard_screen(VOICE_TARGET_LEADERBOARD_FILE, "voice_target_final"), **button_style).grid(row=2,
                                                                                                           column=0,
                                                                                                           padx=20,
                                                                                                           pady=10)
            # Add admin-specific buttons for "Set Threshold" and "Clear Leaderboard"
            tk.Button(button_frame, text="Set Thresholds", command=self.set_thresholds, **button_style).grid(row=3,
                                                                                                             column=0,
                                                                                                             padx=20,
                                                                                                             pady=10)
            tk.Button(button_frame, text="Clear Leaderboard", command=self.reset_leaderboard, **button_style).grid(
                row=4, column=0, padx=20, pady=10)

        # Logout button
        tk.Button(self.root, text="Logout", command=self.create_login_screen, **button_style).pack(pady=30)

    def play_game_squeaky(self):
        threshold_db = self.thresholds.get(self.logged_in_user, 35)

        # Run the game and get the new score
        new_score = run_game(squeaky_bird_SCRIPT, threshold_db)
        print(new_score)

        # Update the leaderboard in the main code
        self.update_leaderboard_from_score(SQUEAKY_BIRD_LEADERBOARD_FILE, new_score)


    def play_game_pitch_perfect(self):
        threshold_db = self.thresholds.get(self.logged_in_user, 35)

        # Run the game and get the new score
        new_score = run_game(pitch_perfect_SCRIPT, threshold_db)

        # Update the leaderboard for Pitch Perfect
        self.update_leaderboard_from_score(PITCH_PERFECT_LEADERBOARD_FILE, new_score)

    def play_game_voice_target(self):
        threshold_db = self.thresholds.get(self.logged_in_user, 35)

        # Run the game and get the new score
        new_score = run_game(voice_target_SCRIPT, threshold_db)

        # Update the leaderboard for Voice Target
        self.update_leaderboard_from_score(VOICE_TARGET_LEADERBOARD_FILE, new_score)

    def create_leaderboard_screen(self, game_file, game_name):
        self.clear_screen()

        try:
            with open(game_file, "r") as file:
                leaderboard = json.load(file)
        except FileNotFoundError:
            leaderboard = {}

        header_style = {"bg": "black", "fg": "#FFD700", "font": ("Bangers Regular", 28, "bold")}
        admin_style = {"bg": "black", "fg": "#61dafb", "font": ("Bangers Regular", 14)}

        tk.Label(self.root, text=f"🏆 {game_name} Leaderboard 🏆", **header_style).pack(pady=20)

        for user, scores in leaderboard.items():
            if isinstance(scores, int):  # Legacy format: single integer
                tk.Label(
                    self.root,
                    text=f"{user}: Total Score: {scores}",
                    **admin_style
                ).pack(pady=5)
            elif isinstance(scores, dict):  # New format: dictionary with multiple keys
                tk.Label(
                    self.root,
                    text=f"{user}:\n"
                         f"Cumulative: {scores.get('cumulative_score', 0)}\n"
                         f"Highest: {scores.get('highest_score', 0)}\n"
                         f"Latest: {scores.get('latest_score', 0)}",
                    **admin_style
                ).pack(pady=5)

        tk.Button(
            self.root,
            text="Back",
            command=self.create_landing_screen,
            font=("Bangers Regular", 14),
            bg="#61dafb",
            fg="#282c34",
        ).pack(pady=30)

    def reset_leaderboard(self):
        if messagebox.askyesno("Reset Leaderboard", "Are you sure you want to reset the leaderboard?"):
            # Reset the leaderboard
            self.leaderboard = {user: {"game1": 0, "game2": 0, "total": 0} for user in USERS.keys()}
            save_leaderboard(self.leaderboard)

            # Reset score.json
            default_scores = {"game": "", "score": 0}
            with open("score.json", "w") as score_file:
                json.dump(default_scores, score_file, indent=4)

            messagebox.showinfo("Reset Successful", "Leaderboard and scores have been reset")
            self.create_leaderboard_screen()

    def update_leaderboard_from_score(self, game_file, new_score):
        try:
            with open(game_file, "r") as file:
                leaderboard = json.load(file)
        except FileNotFoundError:
            leaderboard = {}

        if self.logged_in_user not in leaderboard:
            leaderboard[self.logged_in_user] = 0

        leaderboard[self.logged_in_user] += new_score

        with open(game_file, "w") as file:
            json.dump(leaderboard, file, indent=4)

    def set_thresholds(self):
        user = simpledialog.askstring("Set Threshold", "Enter username:")
        if user in USERS:
            current_threshold = self.thresholds.get(user, 35)
            threshold = simpledialog.askfloat(
                "Set Threshold",
                f"Set threshold for {user} (current: {current_threshold}):",
                minvalue=35,
                maxvalue=70
            )
            if threshold is not None:
                self.thresholds[user] = threshold
                save_thresholds(self.thresholds)
                messagebox.showinfo("Success", f"Threshold for {user} updated to {threshold} dB!")
        else:
            messagebox.showerror("Error", "User does not exist")

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()


# Run the GUI
if __name__ == "__main__":
    root = tk.Tk()
    app = GameApp(root)
    root.mainloop()