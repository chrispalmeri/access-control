<script>
    let theme = localStorage.getItem('theme');

    function light() {
        theme = 'light';
        document.documentElement.className = 'light';
        localStorage.setItem('theme', 'light');
    }

    function dark() {
        theme = 'dark';
        document.documentElement.className = 'dark';
        localStorage.setItem('theme', 'dark');
    }
</script>

<p class="theme">
    {#if theme === 'dark'}
    <button id="light-sw" on:click={light} title="Switch to light theme">
        <svg viewBox="0 0 24 24">
            <circle cx="12" cy="12" r="5"></circle>
            <line x1="12" y1="1" x2="12" y2="3"></line>
            <line x1="12" y1="21" x2="12" y2="23"></line>
            <line x1="4.22" y1="4.22" x2="5.64" y2="5.64"></line>
            <line x1="18.36" y1="18.36" x2="19.78" y2="19.78"></line>
            <line x1="1" y1="12" x2="3" y2="12"></line>
            <line x1="21" y1="12" x2="23" y2="12"></line>
            <line x1="4.22" y1="19.78" x2="5.64" y2="18.36"></line>
            <line x1="18.36" y1="5.64" x2="19.78" y2="4.22"></line>
        </svg>
    </button>
    {:else}
    <button id="dark-sw" on:click={dark} title="Switch to dark theme">
        <svg viewBox="0 0 24 24">
            <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path>
        </svg>
    </button>
    {/if}
</p>

<style>
    .theme {
        justify-self: end;
        padding-right: 24px;
    }
    button {
        border: none;
        border-radius: var(--radius);
    }
    #light-sw, #dark-sw {
        display: block;
        min-width: 0;
        padding: 2px;
        color: var(--soft);
        background-color: transparent;
    }
    #light-sw:hover, #dark-sw:hover {
        color: var(--label);
        background-color: transparent;
    }
    svg {
        display: block;
        width: 20px;
        height: 20px;
        fill: none;
        stroke: currentColor;
        stroke-width: 2;
        stroke-linecap: round;
        stroke-linejoin: round;
    }
</style>
