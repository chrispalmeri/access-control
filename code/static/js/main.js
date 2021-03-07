// main.js

import events from './events.js';

// Create WebSocket connection.
const socket = new WebSocket('ws://' + location.host + '/ws');

// Connection opened
socket.addEventListener('open', function (event) {
    socket.send('Hello Server!');
});

// Listen for messages
socket.addEventListener('message', function (event) {
    console.log('Message from server:', event.data);
    document.getElementById('ws_data').innerHTML = event.data;

    // refresh the event list
    events.get();
});

// Connection closed by server
socket.addEventListener('close', function (event) {
    console.log('The connection has been closed');
    document.getElementById('ws_data').innerHTML = 'Disconnected'
});
