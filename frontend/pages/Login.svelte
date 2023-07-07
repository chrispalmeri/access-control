<script>
    import TextInput from '../components/TextInput.svelte';
    import PasswordInput from '../components/PasswordInput.svelte';

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

        const data = await response.json();

        // redirect to home
        if (data.success === true) {
            location.replace('/');
        }
    }

    function keyPress(event) {
        if (event.key === 'Enter') {
            submit();
        }
    }
</script>

<div class="dialog-mask">
    <div class="dialog-modal">
        <div class="card" on:keypress={keyPress}>
            <h2>Login</h2>
            <TextInput label='Username' bind:value={payload.username} />
            <PasswordInput label='Password' bind:value={payload.password} />
            <p class="buttons">
                <button class="primary" on:click={submit}>Login</button>
            </p>
            <a href="/">Home</a>
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
}
.dialog-modal {
    overflow-y: auto;
}
</style>
