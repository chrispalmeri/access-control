<script>
    import { users } from '../stores.js';

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

        users.refresh();
        dialog.close();
    }

    function cancel() {
        dialog.close();
    }
</script>

<button class="danger" on:click={show}>Delete</button>

<dialog bind:this={dialog} on:click|self={cancel}>
    <div class="card">
        <h2 class="danger">Delete user</h2>
        <p>Are you sure you want to delete {user.name}?</p>
        <p class="buttons">
            <button class="danger" on:click={del}>Delete</button>
            <button on:click={cancel}>Cancel</button>
        </p>
    </div>
</dialog>
