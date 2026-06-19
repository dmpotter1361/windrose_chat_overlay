# Windrose Chat Overlay — notes for Claude Code

Bridges in-game chat for the game **Windrose** to Discord, with an on-screen HUD.
Two parts: a Python (tkinter) HUD client + a Node.js (discord.js) relay.
Repo `dmpotter1361/windrose_chat_overlay`. **Not yet tested end-to-end** (needs a
Discord bot token).

## Run

```powershell
# Client HUD (Python)
pip install -r requirements.txt
python client.py

# Relay (Node.js)
npm install
node server.js
```

## Layout

- **`client.py`** — tkinter HUD overlay client.
- **`server.js`** — Node/discord.js relay bridging chat <-> Discord.
- **`server_status.py`** — status helper.
- **`*_config.example.json`** — config templates. Copy to the real names and add the
  bot token / settings. **Never commit a real bot token.**

## Conventions / next steps

- Keep secrets (bot token) out of git — use the `*_config.example.json` pattern.
- Next planned work: finish the server relay + client app and run a full end-to-end test.
- Python + Node here (not .NET) — different from the sibling WinForms projects.
