const { Client, GatewayIntentBits } = require('discord.js');
const WebSocket = require('ws');
const http = require('http');
const fs = require('fs');

// --- LOAD CONFIG ---
// This will crash cleanly if you forget to create the file, 
// giving you a helpful error message in the console.
let config;
try {
    config = JSON.parse(fs.readFileSync('server_config.json', 'utf8'));
} catch (err) {
    console.error("CRITICAL ERROR: Could not find or parse 'server_config.json'. Make sure it exists!");
    process.exit(1);
}

const DISCORD_TOKEN = config.discord_token;
const CHANNEL_ID = config.channel_id;
const WEBSOCKET_PORT = config.websocket_port || 8080;

// --- DISCORD BOT SETUP ---
const discordClient = new Client({ 
    intents: [GatewayIntentBits.Guilds, GatewayIntentBits.GuildMessages, GatewayIntentBits.MessageContent] 
});

discordClient.once('ready', () => {
    console.log(`Discord Bot logged in as ${discordClient.user.tag}`);
});

// --- HTTP (HEALTH CHECK) & WEBSOCKET SETUP ---
const server = http.createServer((req, res) => {
    if (req.method === 'GET' && req.url === '/ping') {
        res.writeHead(200, { 'Content-Type': 'text/plain' });
        res.end('ACK'); // The health check reply
    } else {
        res.writeHead(404);
        res.end();
    }
});

const wss = new WebSocket.Server({ server });

wss.on('connection', (ws) => {
    console.log('New game client connected.');
    ws.on('message', (message) => {
        const text = message.toString();
        const channel = discordClient.channels.cache.get(CHANNEL_ID);
        if (channel) {
            channel.send(`**[In-Game]**: ${text}`);
        }
    });
});

discordClient.on('messageCreate', (message) => {
    if (message.author.bot || message.channel.id !== CHANNEL_ID) return;
    const outgoingMessage = `[Discord] ${message.author.username}: ${message.content}`;
    wss.clients.forEach((client) => {
        if (client.readyState === WebSocket.OPEN) {
            client.send(outgoingMessage);
        }
    });
});

// --- STARTUP ---
discordClient.login(DISCORD_TOKEN);
server.listen(WEBSOCKET_PORT, () => {
    console.log(`Server is live on port ${WEBSOCKET_PORT}.`);
});