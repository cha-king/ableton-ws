const connectButton = document.getElementById("connect_button");
const noteButton = document.getElementById("note_button");
const urlInput = document.getElementById("url");
const idInput = document.getElementById("client_id");


connectButton.onclick = function() {
    const host = urlInput.value;
    const id = idInput.value;
    const url = `${host}/publish/${id}`

    const ws = new WebSocket(url);

    ws.onerror = function(error) {
        console.log(error);
    };

    ws.onopen = function() {
        console.log("Connected");
        connectButton.innerText = "Connected!";
        noteButton.onclick = function() {
            const note = {
                pitch: 60,
                velocity: 100,
            };
            ws.send(JSON.stringify(note));
        };
    };
};
