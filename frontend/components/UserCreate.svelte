<script>
    // this is nearly a duplicate of UserUpdate

    import TextInput from './TextInput.svelte';
    import NumberInput from './NumberInput.svelte';
    import { users } from '../stores.js';

    let payload = {};

    /*
    const myForm = [
        {name: 'Name', id: 'name', type: TextInput, value: ''},
        {name: 'Pin', id: 'pin', type: NumberInput, value: null},
        {name: 'Card', id: 'card', type: NumberInput, value: null},
        {name: 'Facility', id: 'facility', type: NumberInput, value: null}
    ];
    {#each myForm as field}
    <svelte:component this={field.type} label={field.name} bind:value={field.value}/>
    {/each}
    */

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

        // need to refresh user list after
    }

    function cancel() {
        dialog.close();
    }

    async function post(body) {
        const response = await fetch('/api/users', {
            method: 'POST',
            body: JSON.stringify(body, (k, v) => v == '' ? null : v)
        });

        if (!response.ok) {
            throw new Error(`HTTP Status Code ${response.status}`);
        }

        const data = await response.json(); // will be request but with `id` added
        return data;
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
        <p class="buttons">
            <button on:click={cancel}>Cancel</button>
            <button class="primary" on:click={save}>Save</button>
        </p>
    </div>
</dialog>
