<script>
    import TextInput from '../components/TextInput.svelte';

    const payload = {};
    payload.username = null;
    payload.password = null;

    async function submit() {
        const response = await fetch('/api/auth', {
            method: 'POST',
            body: JSON.stringify(payload, (k, v) => v === '' ? null : v)
        });

        if (!response.ok) {
            throw new Error(`HTTP Status Code ${response.status}`);
        }

        // const data = await response.json();
        // return data;

        // redirect to home
        location.hash = '/';
    }
</script>

<div class="dialog-mask">
    <div class="dialog-modal">
        <div class="card">
            <h2>Login</h2>
            <TextInput label='Username' bind:value={payload.username} />
            <TextInput label='Password' bind:value={payload.password} />
            <p class="buttons">
                <button class="primary" on:click={submit}>Login</button>
            </p>
            <a href="#/">Home</a>
        </div>
    </div>
</div>

<style>
.dialog-mask {
    position: fixed;
    top: 0;
    left: 0;
    height: 100vh;
    width: 100vw;
    display: grid;
    place-content: center;
    background: rgba(128, 128, 128, 0.28);
}
.dialog-modal {
    overflow-y: auto;
}
</style>
