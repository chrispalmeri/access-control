<script>
    import ThemeSwitch from '../components/ThemeSwitch.svelte';
    import Footer from '../components/Footer.svelte';
    import ApiDoc from '../components/ApiDoc.svelte';
    import CodeBlock from '../components/CodeBlock.svelte';

    import api from '../apiDocs.js';

    let selected = api[0];

    function selectId(event) {
        event.preventDefault();
        const clicked = parseInt(event.target.dataset.id);
        selected = api[clicked];
    }

    const mapLabels = {
        POST: 'success',
        PUT: 'warning',
        GET: 'info-alert',
        DELETE: 'danger-alert'
    };
</script>

<ThemeSwitch />

<main>
    <div class="card">
        <h2>API</h2>
        <p><a href="/">Home</a></p>

        <ul>
        {#each api as endpoint, id}
        <li on:click={selectId} data-id={id}>
            <span class={'alert ' + mapLabels[endpoint.method || 'GET']}>{endpoint.method || 'GET'}</span>{endpoint.resource}
        </li>
        {/each}
        </ul>
    </div>

    <div class="card">
        <h2>Details</h2>
        <ApiDoc
            method={selected.method}
            resource={selected.resource}
            description={selected.description}
            request={selected.request}
            responseCode={selected.responseCode}
            responseType={selected.responseType}
            response={selected.response}
        />
    </div>

    <div class="card">
        <h2>Errors</h2>
        <p>403 Forbidden</p>
        <p>404 Not Found</p>
        <p>405 Method Not Allowed</p>
        <p>422 Unprocessable Entity</p>
        <p>500 Internal Server Error</p>
        <CodeBlock value={{ code: 403, message: 'Forbidden' }} />
    </div>
</main>

<Footer />

<style>
    ul {
        list-style: none;
        padding-left: 0;
    }
    li {
        font-family: 'Fira Mono', monospace;
        font-size: 18px;
        line-height: 22px;
        margin: 16px 0;
    }
    li span {
        display: inline-block;
        text-align: center;
        font-size: 16px;
        line-height: 20px;
        pointer-events: none;
        min-width: 64px;
        margin-right: 12px;
    }
</style>
