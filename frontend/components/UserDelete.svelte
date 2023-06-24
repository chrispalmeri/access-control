<script>
    export let user;

    let dialog;

    function show() {
        dialog.showModal();
    }

    async function del() {
        const response = await fetch(`/api/users/${user.id}`, {
            method: 'DELETE'
        });

        if (!response.ok) {
            throw new Error(`HTTP Status Code ${response.status}`);
        }

        dialog.close();
    }

    function cancel() {
        dialog.close();
    }
</script>

<button on:click={show}>Delete</button>

<dialog bind:this={dialog} on:click|self={cancel}>
    <div class="card">
        <h2>Delete user</h2>
        <p>Are you sure you want to delete {user.name}?</p>
        <p>
            <button on:click={del}>Delete</button>
            <button on:click={cancel}>Cancel</button>
        </p>
    </div>
</dialog>
