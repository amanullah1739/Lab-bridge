const socket = io();

socket.on("receive_text", (data) => {

    document.getElementById("received-text").innerText = data.text;

});