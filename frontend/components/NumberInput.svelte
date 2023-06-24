<script>
    export let label;
    export let value;
</script>

<p>
    <label>{label} <input type="number" bind:value={value} /></label>
</p>
