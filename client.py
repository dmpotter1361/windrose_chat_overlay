import os
import json
import time
import threading
import win32gui
import keyboard
import websocket
import tkinter as tk
import random

# --- GLOBALS & DEFAULTS ---
CONFIG_FILE = "chat_config.json"
SERVER_URL = ""
GAME_WINDOW_TITLE = ""
PLAYER_NAME = ""
MAX_HISTORY = 5
CHAT_TIMEOUT = 10

ws_connection = None
overlay = None

# --- CONFIGURATION LOGIC ---
def load_or_prompt_config():
    global PLAYER_NAME, SERVER_URL, GAME_WINDOW_TITLE, MAX_HISTORY, CHAT_TIMEOUT
    
    # Default settings including the new HUD variables
    config_data = {
        "name": "PlayerName", 
        "server_url": "ws://127.0.0.1:8080", 
        "game_window": "Windrose",
        "max_history_rows": 5,
        "chat_timeout_seconds": 10
    }

    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            try:
                saved_data = json.load(f)
                config_data.update(saved_data)
            except json.JSONDecodeError:
                print("Error reading config file. Using defaults.")

    SERVER_URL = config_data.get("server_url", "ws://127.0.0.1:8080")
    GAME_WINDOW_TITLE = config_data.get("game_window", "Windrose")
    PLAYER_NAME = config_data.get("name", "PlayerName")
    MAX_HISTORY = config_data.get("max_history_rows", 5)
    CHAT_TIMEOUT = config_data.get("chat_timeout_seconds", 10)

    # Force a random name if they left it blank
    if PLAYER_NAME == "PlayerName" or not PLAYER_NAME.strip():
        random_id = random.randint(1000, 9999)
        PLAYER_NAME = f"Explorer_{random_id}"
        config_data["name"] = PLAYER_NAME

    with open(CONFIG_FILE, 'w') as f:
        json.dump(config_data, f, indent=4)

# --- WEBSOCKET HANDLERS ---
def on_message(ws, message):
    if overlay:
        # Pass the incoming message to the HUD overlay safely
        overlay.root.after(0, overlay.add_message, message)

def on_error(ws, error):
    pass

def on_open(ws):
    if overlay:
        overlay.root.after(0, overlay.add_message, f"[System]: Connected to Chat Server!")

def start_websocket():
    global ws_connection
    ws_connection = websocket.WebSocketApp(SERVER_URL,
                                           on_open=on_open,
                                           on_message=on_message,
                                           on_error=on_error)
    while True:
        ws_connection.run_forever()
        time.sleep(5)

# --- HUD OVERLAY LOGIC ---
class ChatOverlay:
    def __init__(self):
        self.root = tk.Tk()
        self.root.overrideredirect(True) # Removes window borders
        self.root.attributes('-topmost', True) # Forces it over the game
        self.root.configure(bg='black')
        self.root.attributes('-alpha', 0.8) # Semi-transparent dark mode
        
        # Position the HUD in the bottom left corner of the screen
        screen_height = self.root.winfo_screenheight()
        self.root.geometry(f"500x300+20+{screen_height - 380}")

        # Chat History Label
        self.history_var = tk.StringVar(value="[System]: Initializing Bridge...")
        self.history_label = tk.Label(self.root, textvariable=self.history_var, bg='black', fg='white', 
                                      justify='left', anchor='sw', font=('Arial', 11))
        self.history_label.pack(fill='both', expand=True, padx=10, pady=5)

        # Chat Input Box (Hidden by default)
        self.input_var = tk.StringVar()
        self.input_entry = tk.Entry(self.root, textvariable=self.input_var, bg='gray20', fg='white', 
                                    font=('Arial', 11), insertbackground='white')

        self.messages = []
        self.hide_job = None
        self.is_typing = False
        self.game_hwnd = None

        self.reset_hide_timer()
        self.check_window_loop()

    def add_message(self, msg):
        self.messages.append(msg)
        # Cull old messages based on the JSON setting
        if len(self.messages) > MAX_HISTORY:
            self.messages.pop(0)
            
        self.history_var.set("\n".join(self.messages))
        self.show_chat()
        
        # Restart the dismissal timer if we aren't currently typing
        if not self.is_typing:
            self.reset_hide_timer()

    def show_chat(self):
        self.root.deicon