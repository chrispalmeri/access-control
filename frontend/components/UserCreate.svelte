<script>
    // this is nearly a duplicate of UserUpdate

    import TextInput from './TextInput.svelte';
    import NumberInput from './NumberInput.svelte';
    import { users } from '../stores.js';

    const payload = {};

    let dialog;

    function show() {
        payload.name = null;
        payload.pin = null;
        payload.card = null;
        payload.facility = null;
        dialog.showModal();
    }

    async function save() {
        await post(payload);
        users.refresh();
        dialog.close();
    }

    function cancel() {
        dialog.close();
    }

    async function post(body) {
        const response = await fetch('/api/users', {
            method: 'POST',
            body: JSON.stringify(body, (k, v) => v === '' ? null : v)
        });

        if (!response.ok) {
            throw new Error(`HTTP Status Code ${response.status}`);
        }

        const data = await response.json(); // will be request but with `id` added
        return data;
    }

    async function lastSwiped() {
        const response = await fetch('/api/card');

        if (!response.ok) {
            throw new Error(`HTTP Status Code ${response.status}`);
        }

        const data = await response.json();

        // "Access denied for Card: 54009 Facility: 204"
        const numbers = data.message.match(/\d+/g);

        payload.card = numbers[0];
        payload.facility = numbers[1];
    }
</script>

<button class="primary" on:click={show}>Add</button>

<dialog bind:this={dialog} on:click|self={cancel}>
    <div class="card">
        <h2>Add user</h2>
        <TextInput label='Name' bind:value={payload.name} />
        <NumberInput label='Pin' bind:value={payload.pin} />
        <NumberInput label='Card' bind:value={payload.card} />
        <NumberInput label='Facility' bind:value={payload.facility} />
        <p>
            <button on:click={lastSwiped}>Last denied card</button>
        </p>
        <p class="buttons">
            <button class="primary" on:click={save}>Save</button>
            <button on:click={cancel}>Cancel</button>
        </p>
    </div>
</dialog>
