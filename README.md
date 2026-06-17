# Windrose Chat Overlay

A lightweight, seamless in-game chat overlay for *Windrose*, designed to bridge in-game communication with Discord. This project provides a secure, non-intrusive HUD that allows players to chat without leaving the game window.

## Purpose
The goal of this project is to provide a native-feeling chat experience. It automatically captures keyboard input when the game is active, displays recent messages in a semi-transparent HUD, and bridges that text directly to a designated Discord channel via a private relay server.

## Project Structure
* `client.py`: The main overlay application. It monitors the game window, captures `Enter` key presses, renders the semi-transparent HUD, and manages the WebSocket connection.
* `server.js`: The backend relay server. It acts as the bridge between the WebSocket game clients and Discord. It also hosts a health-check endpoint.
* `server_status.py`: A utility script to perform a "ping" check on the server to verify it is online and responsive before launching the game.
* `chat_config.json`: The client-side configuration file containing user settings for display, timeout, and server connectivity.
* `server_config.json`: The server-side configuration file containing your Discord bot credentials and port settings.

## Configuration
### Client Settings (`chat_config.json`)
* **name**: The player's display name. If left blank or as "PlayerName", the system automatically assigns a random `Explorer_XXXX` name.
* **server_url**: The address of the relay server (e.g., `ws://127.0.0.1:8080`).
* **max_history_rows**: The number of lines of chat kept on the HUD.
* **chat_timeout_seconds**: How long the HUD remains visible after the last message or after closing the input box.

### Server Settings (`server_config.json`)
* **websocket_port**: The port the server binds to for both WebSocket chat and the HTTP health check.
* **discord_token**: Your bot's API token.
* **channel_id**: The ID of the Discord channel where the relay should post.

## Health Check
The server provides a simple HTTP endpoint for status verification. You can verify server health by hitting the `/ping` endpoint on your server's port. The `server_status.py` utility does this automatically and returns `ACK` if the server is healthy.

## Development Notes
* **Security**: The client side uses `win32gui` to ensure it only listens for the `Enter` key when the specific game window is active.
* **Deployment**: The server is designed to be compiled into a standalone `.exe` using `pkg`, and the client/status apps are designed for `pyinstaller`.
