<script>
    import Select from './Select.svelte';

    let state = 'Disconnected';
    let events = [];

    // pagination
    // let page = 1;
    // let perPage = 15;

    const options = [
        { value: 'CRITICAL', text: 'Critical' },
        { value: 'ERROR', text: 'Error' },
        { value: 'WARNING', text: 'Warning' },
        { value: 'INFO', text: 'Info' },
        { value: 'DEBUG', text: 'Debug' }
    ];
    let selected = 'DEBUG';
    // what you selected will be reset on page reload

    // when selected changes, get() again
    $: get(selected);

    // this hits endpoint twice on page load
    // cause both selected change and websocket connect
    // also websocket hits it even when events created that will not display

    async function get() {
        // query builder
        const url = new URL('/api/events', window.location.origin);
        url.searchParams.append('limit', 15);

        for (const option of options) {
            url.searchParams.append('channel', option.value);
            if (option.value === selected) break;
        }

        const response = await fetch(url);
        const data = await response.json();
        events = data;
    }

    // this should be a class so you can reconnect
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
    <p class="smallgap">
        {state} <!-- change to disconnect/reconnect button -->
        <Select options={options} bind:value={selected} />
    </p>
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
    <!-- <p>
        <button>&lt;</button>
        {page}
        <button>&gt;</button>
    </p> -->
</div>
