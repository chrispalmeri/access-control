// Create WebSocket connection.
const socket = new WebSocket('ws://localhost:8080/ws');

// Connection opened
socket.addEventListener('open', function (event) {
    socket.send('Hello Server!');
});

// Listen for messages
socket.addEventListener('message', function (event) {
    console.log('Message from server ', event.data);
    document.getElementById('output').innerHTML = event.data
});

// Connection closed by server
socket.addEventListener('close', (event) => {
    console.log('The connection has been closed successfully.');
    document.getElementById('output').innerHTML = 'Disconnected'
});
