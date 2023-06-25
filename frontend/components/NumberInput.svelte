<script>
    export let label;
    export let value;
    export let disabled = false;

    // cause firefox lets you enter text in number inputs
    // all the caret position preservation is probably overkill
    function clean(e) {
        let input = e.target.value;
        let caret = e.target.selectionStart;
        let cleaned = input.replace(/\D/g, '');
        let diff = input.length - cleaned.length;

        value = cleaned;

        // don't care if cursor is at the end already
        // rewind caret position after removing alpha
        // usually 1, but get the diff in case pasting
        // animation frame so it happens after the bound value update
        if (caret < input.length && diff) {
            requestAnimationFrame(() => {
                caret = Math.max(caret - diff, 0);
                e.target.setSelectionRange(caret, caret);
            });
        }
    }
</script>

<p>
    <label>{label} <input bind:value={value} on:input={clean} {disabled}/></label>
</p>
