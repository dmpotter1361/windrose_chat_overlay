import urllib.request
import json
import os

CONFIG_FILE = "chat_config.json"

def check_server():
    print("========================================")
    print("   Windrose Chat Server Status Check")
    print("========================================\n")
    
    # 1. Read the server IP from the shared config file
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r') as f:
                config = json.load(f)
                ws_url = config.get("server_url", "ws://127.0.0.1:8080")
        except Exception:
            ws_url = "ws://127.0.0.1:8080"
    else:
        ws_url = "ws://127.0.0.1:8080"
        
    print(f"Target Server: {ws_url}")
    print("Pinging...\n")
        
    # 2. Convert the WebSocket URL to a standard Web URL for the ping
    http_url = ws_url.replace("ws://", "http://").replace("wss://", "https://") + "/ping"
    
    # 3. Send the Ping
    try:
        # Timeout after 3 seconds so the app doesn't freeze if the server is dead
        response = urllib.request.urlopen(http_url, timeout=3)
        
        # 4. Check for the ACK
        if response.getcode() == 200 and response.read().decode() == "ACK":
            print("[SUCCESS] The Chat Server is ONLINE and ready!")
        else:
            print("[WARNING] The server replied, but the response was unexpected.")
            
    except urllib.error.URLError:
        print("[FAILED] The server is OFFLINE. (Connection Refused/Timeout)")
    except Exception as e:
        print(f"[ERROR] Could not connect: {e}")
        
    print("\n========================================")
    print("Press Enter to close this window...")
    input()

if __name__ == "__main__":
    check_server()