<script>
    let state = 'Disconnected';
    let events = [];

    async function get() {
        const response = await fetch('/api/events?channel=DEBUG&channel=INFO&channel=WARNING&limit=15');
        const data = await response.json();
        events = data;
    }

    // Create WebSocket connection.
    const socket = new WebSocket('ws://' + location.host + '/ws');

    // Connection opened
    socket.addEventListener('open', function () {
        socket.send('Hello Server!');
    });

    // Listen for messages
    socket.addEventListener('message', function (event) {
        console.log('Message from server:', event.data);
        state = 'Connected';

        // refresh the event list
        get();
    });

    // Connection closed by server
    socket.addEventListener('close', function () {
        console.log('The connection has been closed');
        state = 'Disconnected';
    });
</script>

<div class="card">
    <h2>Events</h2>
    <p>{state}</p>
    {#if events.length > 0}
    <table>
        <tr>
            <th>Time</th>
            <th>Channel</th>
            <th>Message</th>
        </tr>
        {#each events as event (event.id)}
        <tr>
            <td>{new Date(event.time).toLocaleString()}</td>
            <td>{event.channel}</td>
            <td>{event.message}</td>
        </tr>
        {/each}
    </table>
    {:else}
    <p>No items to show</p>
    {/if}
</div>
