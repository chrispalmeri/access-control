<script>
    // this is nearly a duplicate of UserUpdate

    import TextInput from './TextInput.svelte';
    import NumberInput from './NumberInput.svelte';

    let user = {
        name: '',
        pin: null,
        card: null,
        facility: null
    };

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
        dialog.showModal();
    }

    async function save() {
        await post(user);
        dialog.close();

        // need to refresh user list after
    }

    function cancel() {
        // need to nuke entered values
        dialog.close();
    }

    async function post(body) {
        const response = await fetch('/api/users', {
            method: 'POST',
            body: JSON.stringify(body)
        });

        const data = await response.json(); // will be request but with `id` added

        if (response.ok) { // this is out of order
            return data;
        } else {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
    }
</script>

<button on:click={show}>Add</button>

<dialog bind:this={dialog} on:click|self={cancel}>
    <div class="card">
        <h2>Add user</h2>
        <TextInput label='Name' bind:value={user.name} />
        <NumberInput label='Pin' bind:value={user.pin} />
        <NumberInput label='Card' bind:value={user.card} />
        <NumberInput label='Facility' bind:value={user.facility} />
        <p>
            <button on:click={save}>Save</button>
            <button on:click={cancel}>Cancel</button>
        </p>
    </div>
</dialog>
