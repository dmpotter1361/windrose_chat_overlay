# Windrose Chat Overlay

A lightweight, in-game chat overlay for *Windrose* — the chat the game never shipped.
It bridges your party's in-game messages to a Discord channel and back, through a small
private relay server. A semi-transparent HUD sits over the game, captures the `Enter`
key only while *Windrose* is focused, pops a quick text box to type, and shows recent
messages — so nobody has to alt-tab to talk.

> Personal project. Not affiliated with, endorsed by, or sponsored by the makers of *Windrose*.

## How it works

There are three moving parts:

```
 [Player types in game]                         [Discord channel]
          │                                             │
          ▼                                             ▼
   client.py  ───── ws:// ─────►  server.js (relay)  ◄──── Discord bot
   (tkinter HUD)   WebSocket      (Node + discord.js)
          ▲                                             ▲
          └──────── ws:// ◄──── messages from Discord ──┘
```

- **`client.py`** — the player-facing overlay. It watches the foreground window, and
  only when *Windrose* is active does pressing `Enter` open a small input box. What you
  type goes out over a WebSocket; messages coming back (from Discord or other players)
  scroll in a semi-transparent HUD that fades after a few seconds.
- **`server.js`** — the relay. It hosts the WebSocket endpoint the clients connect to,
  logs into Discord as a bot, and shuttles messages both directions: in-game chat is
  posted to your Discord channel, and anything typed in that channel is pushed back down
  to every connected client. It also serves a tiny `/ping` health check.
- **`server_status.py`** — a one-click "is the relay up?" check that pings `/ping` and
  reports `ONLINE` / `OFFLINE` before you launch the game.

## Project layout

| File | What it is |
|------|------------|
| `client.py` | The overlay app players run (tkinter HUD + WebSocket). |
| `server.js` | The Node relay that bridges WebSocket ↔ Discord. |
| `server_status.py` | Pings the relay's `/ping` endpoint to confirm it's live. |
| `chat_config.example.json` | Template for the client config — copy to `chat_config.json`. |
| `server_config.example.json` | Template for the server config — copy to `server_config.json`. |
| `requirements.txt` | Python client dependencies. |
| `package.json` | Node server dependencies. |

## Configuration

Both configs are created from the `.example.json` templates. The real `chat_config.json`
and `server_config.json` are git-ignored so your Discord token never lands in the repo.

**Client — `chat_config.json`**

- **name** — the player's display name. Left blank or as `PlayerName`, it's auto-assigned a
  random `Explorer_XXXX`.
- **server_url** — the relay address, e.g. `ws://127.0.0.1:8080` locally or
  `ws://your.server.ip:8080` in production.
- **game_window** — the window title to watch for (`Windrose`).
- **max_history_rows** — lines of chat kept on the HUD.
- **chat_timeout_seconds** — how long the HUD stays visible after the last message.

**Server — `server_config.json`**

- **websocket_port** — the port the relay binds for both WebSocket chat and the `/ping` check.
- **discord_token** — your bot's token (see [Set up the Discord bot](#set-up-the-discord-bot)).
- **channel_id** — the Discord channel the relay posts to and listens on.

## Set up the Discord bot

1. Open the [Discord Developer Portal](https://discord.com/developers/applications) → **New Application** (e.g. *Windrose Chat Bridge*).
2. **Bot** → **Reset Token**, copy it into `server_config.json` as `discord_token`. Under
   **Privileged Gateway Intents**, turn **Message Content Intent** ON and save.
3. **OAuth2 → URL Generator**: scope **bot**; permissions **Send Messages**, **Read Message
   History**, **View Channels**. Open the generated URL and invite the bot to your server.
4. In Discord, enable **Developer Mode** (Settings → Advanced), right-click your channel →
   **Copy Channel ID**, and paste it into `server_config.json` as `channel_id`.

## Run it locally

You can test the whole pipeline on one PC before deploying or compiling anything.

```bash
# 1. Server deps (Node 18+)
npm install

# 2. Client deps (Python 3.10+, Windows)
pip install -r requirements.txt

# 3. Create your configs from the templates
copy server_config.example.json server_config.json   # then add your bot token + channel id
copy chat_config.example.json   chat_config.json

# 4. Start the relay
node server.js

# 5. In a second terminal, start the overlay
python client.py
```

**Quick simulation (no game needed):** open Notepad and save an empty file as `Windrose.txt`
so the window title contains "Windrose". Click into that window, press `Enter`, and the HUD
input box should pop up. Type a message → it flows through the relay into your Discord
channel, and anything posted back in that channel appears on the HUD.

## Deploy

- **Server:** runs anywhere Node does. Point clients at its public address
  (`ws://your.server.ip:8080`) and open the port. The relay can be packaged into a
  standalone `.exe` with [`pkg`](https://github.com/vercel/pkg).
- **Client:** distribute `client.py` and `server_status.py` as `.exe` files with
  [`pyinstaller`](https://pyinstaller.org/) (`--noconsole` for the overlay) so players just
  double-click to run.

## Continuing development with Claude Code

This project was built with AI assistance and is set up so you can keep going the same way.

1. **Get the code onto your PC**

   ```bash
   git clone https://github.com/dmpotter1361/windrose_chat_overlay.git
   cd windrose_chat_overlay
   ```

2. **Install [Claude Code](https://claude.com/claude-code)** (Anthropic's coding CLI) and
   start it in the project folder:

   ```bash
   npm install -g @anthropic-ai/claude-code
   claude
   ```

   (You can also use the Claude Code extension for VS Code / JetBrains, or
   [claude.ai/code](https://claude.ai/code).)

3. **Point Claude at the project and ask for what you want.** A good first prompt:

   > Read the README, `client.py`, and `server.js` so you understand the pipeline, then
   > help me &lt;your change&gt;.

## Acknowledgments

Windrose Chat Overlay was designed and built collaboratively with **Claude** (Anthropic's AI),
pair-programming with the author from the idea through the relay, the overlay, and this README.
The direction, decisions, and real-world testing are human; a lot of the implementation was
AI-assisted — and we're happy to say so. 🤖🤝

## License

[MIT](LICENSE)
