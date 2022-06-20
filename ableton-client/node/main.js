const readline = require("readline");

const max = require("max-api");
const WebSocket = require("ws");


const heldNotes = new Set();


function hashCode(string) {
    let hash = 0, i, chr;
    if (string.length === 0) return hash;
    for (i = 0; i < string.length; i++) {
      chr   = string.charCodeAt(i);
      hash  = ((hash << 5) - hash) + chr;
      hash |= 0; // Convert to 32bit integer
    }
    return hash;
  };


const url = process.argv[2];

console.log(`Attempting to connect to URL: ${url}`);

const ws = new WebSocket(url);
ws.on("error", () => {
    console.error("Error");
})
ws.on("message", deviceId => {
    console.log("Message received");
    // Do nothing if no notes are held
    if (!heldNotes.size) {
        return
    }
    const id = hashCode(deviceId) % heldNotes.size
    const pitch = Array.from(heldNotes)[id];

    max.outlet(pitch, 100);
})
console.log("Connected");


const rl = readline.createInterface({input: process.stdin, terminal: false});
rl.on('line', line => {
    const [pitch, velocity] = line.split(' ').map(x => parseInt(x));
    if (velocity !== 0) {
        heldNotes.add(pitch);
    } else {
        heldNotes.delete(pitch);
    }
});
