<script>
    export let label;
    export let value;
</script>

<p>
    <label>{label} <input type="password" bind:value={value} /></label>
</p>
