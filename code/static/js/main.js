// main.js

import events from './events.js';
import users from './users.js';
import database from './database.js';

// Create WebSocket connection.
const socket = new WebSocket('ws://' + location.host + '/ws');

// Connection opened
socket.addEventListener('open', function (event) {
    socket.send('Hello Server!');
});

// Listen for messages
socket.addEventListener('message', function (event) {
    console.log('Message from server:', event.data);
    document.getElementById('ws_data').innerHTML = 'Connected';

    // refresh the event list
    events.get();
});

// Connection closed by server
socket.addEventListener('close', function (event) {
    console.log('The connection has been closed');
    document.getElementById('ws_data').innerHTML = 'Disconnected'
});

document.getElementById('backup').addEventListener('click', database.backup)
document.getElementById('restore').addEventListener('click', database.restore)

window.addEventListener('load', function() {
    users.get();
});
