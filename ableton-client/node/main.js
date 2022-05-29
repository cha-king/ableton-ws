const max = require("max-api");
const WebSocket = require("ws");


const url = process.argv[2];

console.log(`Attempting to connect to URL: ${url}`);

const ws = new WebSocket(url);
ws.on("error", () => {
    max.post("error");
})
ws.on("message", data => {
    note = JSON.parse(data);
    max.outlet(note.pitch, note.velocity);
})
