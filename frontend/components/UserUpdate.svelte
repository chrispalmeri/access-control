<script>
    import TextInput from './TextInput.svelte';
    import NumberInput from './NumberInput.svelte';

    export let user = {
        id: null,
        name: '',
        pin: null,
        card: null,
        facility: null
    };

    let dialog;

    function show() {
        dialog.showModal();
    }

    async function save() {
        await put(user);
        dialog.close();

        // need to refresh user list after
    }

    function cancel() {
        // need to reset the entered values
        // actually dunno if the input values being bound may be a problem
        dialog.close();
    }

    async function put(body) {
        const response = await fetch(`/api/users/${body.id}`, {
            method: 'PUT',
            body: JSON.stringify(body)
        });

        const data = await response.json();

        if (response.ok) {
            return data;
        } else {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
    }
</script>

<button on:click={show}>Edit</button>

<dialog bind:this={dialog} on:click|self={cancel}>
    <div class="card">
        <h2>Edit user</h2>
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
