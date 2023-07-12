<script>
    import TextInput from './TextInput.svelte';
    import NumberInput from './NumberInput.svelte';
    import { users } from '../stores.js';

    export let user;

    let dialog;
    const payload = {};

    function show() {
        // this is so user is unchanged if you cancel
        payload.name = user.name;
        payload.pin = user.pin;
        payload.card = user.card;
        payload.facility = user.facility;
        dialog.showModal();
    }

    async function save() {
        await put(payload);
        users.refresh();
        dialog.close();

        // need to refresh user list after
    }

    function cancel() {
        dialog.close();
    }

    // json replacer to not save empty strings
    // binding input values has some flip-flop between '' and null
    async function put(body) {
        const response = await fetch(`/api/users/${user.id}`, {
            method: 'PUT',
            body: JSON.stringify(body, (k, v) => v === '' ? null : v)
        });

        if (!response.ok) {
            throw new Error(`HTTP Status Code ${response.status}`);
        }

        // not catching json errors though
        const data = await response.json();
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

<button on:click={show}>Edit</button>

<dialog bind:this={dialog} on:click|self={cancel}>
    <div class="card">
        <h2>Edit user</h2>
        <NumberInput label='Id' value={user.id} disabled={true} />
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
