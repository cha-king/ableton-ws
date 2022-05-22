const URL = "ws://localhost:8000/publish";


const button = document.getElementsByTagName("button")[0];

const ws = new WebSocket(URL);

ws.onerror = function(error) {
    console.log(error);
};

ws.onopen = function() {
    console.log("Connected");
    button.onclick = function() {
        const note = {
            pitch: 60,
            velocity: 100,
        };
        ws.send(JSON.stringify(note));
    };
};
