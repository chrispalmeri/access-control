<script>
    export let label;
    export let value;
</script>

<p>
    <label>{label} <input type="text" bind:value={value} /></label>
</p>
