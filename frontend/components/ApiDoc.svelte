<script>
    import CodeBlock from '../components/CodeBlock.svelte';

    export let method = 'GET';
    export let resource;
    export let description;
    export let request = null;
    export let responseCode = 200;
    export let responseType = 'application/json';
    export let response = null;

    $: method = method || 'GET';
    $: responseCode = responseCode || 200;
    $: responseType = responseType || 'application/json';
</script>

<h3>{method} {resource}</h3>

{#if description}
<p>{description}</p>
{/if}

{#if request}
<h4>Request</h4>
<CodeBlock value={request} />
{/if}

<h4>Response</h4>
<p>{responseCode} {responseType}</p>
{#if response}
<CodeBlock value={response} />
{/if}
