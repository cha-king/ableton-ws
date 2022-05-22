const max = require("max-api");
const WebSocket = require("ws");


const URL = "ws://localhost:8000/receive"


const ws = new WebSocket(URL);
ws.on("error", () => {
    max.post("error");
})
ws.on("message", data => {
    note = JSON.parse(data);
    max.outlet(note.pitch, note.velocity);
})
