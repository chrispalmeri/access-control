<script>
    import { onDestroy } from 'svelte';
    import Select from './Select.svelte';
    import { events } from '../stores.js';

    let state = 'Disconnected';

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
        const url = new URL('/api/events', location.origin);
        url.searchParams.append('limit', 15);

        for (const option of options) {
            url.searchParams.append('channel', option.value);
            if (option.value === selected) break;
        }

        const response = await fetch(url);
        if (response.status === 403) {
            events.set([]);
            location.replace('/login');
            return;
        }
        const data = await response.json();
        events.set(data);

        // you usually get a hardware loop startup log in webui on restart.
        // i guess it gets hit with a last websocket, and then hits the api,
        // but the api doesn't respond til service is back up.
        // so use that to reconnect automatically
        // also this is now how socket is opened on initial page load
        if (!socket) {
            console.log('open from api');
            startWebsocket();
        }
    }

    let socket = null; // does not respect existing socket onMount?

    function startWebsocket() {
        // not entirely necessary
        if (socket) {
            console.log('rejected');
            return;
        }

        // Create WebSocket connection.
        socket = new WebSocket('ws://' + location.host + '/ws');

        // Connection opened
        socket.addEventListener('open', function () {
            // socket.send('Hello Server!');
            state = 'Connected';
        });

        // Listen for messages
        socket.addEventListener('message', function (event) {
            console.log('Message from server:', event.data);
            // state = 'Connected';

            // refresh the event list
            if (event.data === 'New events available') {
                get();
            }
        });

        // Connection closed by server
        // also get this event on failed to open connection, and after errors
        socket.addEventListener('close', function (event) {
            // https://developer.mozilla.org/en-US/docs/Web/API/CloseEvent
            console.log(event.code, event.reason, event.wasClean);

            console.log('The connection has been closed');
            state = 'Disconnected';
            socket = null;
            // check immediatley?

            if (event.reason === 'login') {
                location.replace('/login');
            }
        });
    }

    // https://stackoverflow.com/a/31985557

    // rename startWebsocket and check

    // if there is no attempted activity, browser won't detect cable disconnect
    // for 10 minutes, with activity it detects in 20 sec, don't even need to
    // get a text response
    function check() {
        if (socket && socket.readyState === WebSocket.OPEN) {
            // console.log('ping');
            socket.send('ping');
        } else if (!socket) {
            console.log('open from interval');
            startWebsocket();
        }
    }

    // should build some incremental backoff
    // and some option to force clearInterval would probably be smart
    const detector = setInterval(check, 5000);

    // don't even need anymore, cause navigation is new page
    onDestroy(() => {
        clearInterval(detector);
        if (socket) {
            socket.close(); // can get reopend by interval though
        }
    });
</script>

<div class="card">
    <h2>Events</h2>
    <p class="smallgap">
        {state} <!-- change to disconnect/reconnect button -->
        <Select options={options} bind:value={selected} />
    </p>
    {#if $events.length > 0}
    <table>
        <tr>
            <th>Time</th>
            <th>Channel</th>
            <th>Message</th>
        </tr>
        {#each $events as event (event.id)}
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
