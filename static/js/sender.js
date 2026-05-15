const socket = io();

document.getElementById("send-btn").addEventListener("click", () => {

    const text = document.getElementById("text-input").value;

    socket.emit("send_text", {
        session_id: SESSION_ID,
        text: text
    });

});