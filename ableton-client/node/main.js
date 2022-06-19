const readline = require("readline");

const max = require("max-api");
const WebSocket = require("ws");


const heldNotes = new Set();


const url = process.argv[2];

console.log(`Attempting to connect to URL: ${url}`);

const ws = new WebSocket(url);
ws.on("error", () => {
    console.error("Error");
})
ws.on("message", data => {
    note = JSON.parse(data);
    max.outlet(note.pitch, note.velocity);
    console.log(note);
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
