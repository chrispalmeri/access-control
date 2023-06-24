<script>
    export let id;

    let dialog;

    function show() {
        dialog.showModal();
    }

    async function del() {
        const response = await fetch(`/api/users/${id}`, {
            method: 'DELETE'
        });

        if (response.ok) {
            dialog.close();
        }
    }

    function cancel() {
        dialog.close();
    }
</script>

<button on:click={show}>Delete</button>

<dialog bind:this={dialog} on:click|self={cancel}>
    <div class="card">
        <h2>Delete user</h2>
        <p>Are you sure?</p>
        <p>
            <button on:click={del}>Delete</button>
            <button on:click={cancel}>Cancel</button>
        </p>
    </div>
</dialog>
