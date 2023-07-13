<script>
    export let value;

    import Prism from 'prismjs';
    import 'prismjs/components/prism-json';
    Prism.manual = true;

    // get html cause highlightElement() broke svelte and was no longer reactive
    function hilite(input) {
        const str = JSON.stringify(input, null, 4);

        if (str) {
            return Prism.highlight(str, Prism.languages.json);
        }

        return '';
    }

    $: code = hilite(value);
</script>

<pre><code>{@html code}</code></pre>
