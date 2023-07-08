<script>
    /*
    type to jump to option
    white-space pre handling long lines

    Native select observations:

    outline goes away on open
        unseen on click to open, seen on click to close
    tab out selects the hovered item??

    all have drop shadow
    border in between maintained

    outside window click closes
    label click focuses but does not open, closes also

    click outside windows blurs element, you can use that probably
    i don't think it really does
    */

    export let options = [
        { value: '', text: '' }
    ];

    export let value = '';

    let input;
    let dropdown;
    let open = false;
    let valueIndex = 0;
    let focusIndex = 0;

    function findValue(x) {
        const i = options.findIndex(option => option.value.toLowerCase().startsWith(x.toLowerCase()));
        if (i > -1) {
            setEverything(i);
        }
    }

    // initial provided value
    findValue(value);

    function setEverything(x) {
        valueIndex = x;
        value = options[valueIndex].value;
        focusIndex = valueIndex;
    }

    function toggle() {
        open = !open;
        focusIndex = valueIndex;
    }

    function openSelect() {
        open = true;
        focusIndex = valueIndex;
    }

    function closeSelect() {
        open = false;
        focusIndex = valueIndex;
    }

    function deselect(e) {
        requestAnimationFrame(() => {
            const caret = e.target.selectionEnd;
            e.target.setSelectionRange(caret, caret);
        });
    }

    let keyTimer;
    let searchString = '';

    function keySearch(input) {
        clearTimeout(keyTimer);

        if (input === 'Backspace') {
            searchString = searchString.substring(0, searchString.length - 1);
        } else {
            searchString = searchString + input;
        }

        // console.log(searchString);

        if (searchString) { // skip if empty string
            findValue(searchString);
        }

        keyTimer = setTimeout(() => { searchString = ''; }, 1000);
    }

    function keyPress(e) {
        if (e.key === 'Escape') {
            closeSelect();
        } else if (e.key === ' ') {
            openSelect();
        } else if (e.key === 'Tab') {
            if (open) {
                closeSelect();
                input.focus();
                e.preventDefault();
            }
        } else if (e.key === 'ArrowUp' || e.key === 'ArrowLeft') {
            setEverything(Math.max(focusIndex - 1, 0));
        } else if (e.key === 'ArrowDown' || e.key === 'ArrowRight') {
            setEverything(Math.min(focusIndex + 1, options.length - 1));
        } else if (e.key.length === 1 || e.key === 'Backspace') {
            keySearch(e.key);
        } else {
            console.log("'" + e.key + "'");
            // 'Shift', 'Enter', 'Control', 'Alt', 'CapsLock', etc
        }
    }

    function optionClick(e) {
        setEverything(+e.target.dataset.value);
        closeSelect();
        input.focus();
    }

    function optionHover(e) {
        if (!e.target.classList.contains('current')) {
            focusIndex = +e.target.dataset.value;
        }
    }

    window.addEventListener('click', (e) => {
        // really any click would close it if open
        // but don't want to conflict with other handlers
        if (open && e.target !== dropdown && e.target !== input) {
            closeSelect();
        }
    });
</script>

<div class="select">
    <input bind:this={input} on:click={toggle} on:keydown={keyPress}
        on:focus={deselect} value={options[valueIndex].text}
        class:open={open} readonly data-type="select" />
    <svg xmlns='http://www.w3.org/2000/svg' width='10' height='10'>
        <polygon points='1,1 5,8 9,1' />
    </svg>
    {#if open}
    <ul bind:this={dropdown}>
        {#each options as option, i}
        <li><button on:click={optionClick} on:mousemove={optionHover}
            class:current={option.value === options[focusIndex].value}
            data-value={i}>{option.text}</button></li>
        {/each}
    </ul>
    {/if}
</div>

<style>
    .select {
        position: relative;
        width: fit-content;
    }
    input[data-type='select'] {
        cursor: default;
    }
    input.open {
        outline: 2px solid var(--selection);
    }
    .select svg {
        position: absolute;
        top: 14px;
        right: 12px;
        pointer-events: none;
        fill: var(--soft);
    }
    .select ul {
        box-sizing: border-box;
        width: 100%;
        padding: 0;
        margin: 2px 0 0;
        position: absolute;
        z-index: 10;
        list-style: none;
        cursor: default;
        border-radius: 4px;
        /*box-shadow: 0 1px 2px 0 rgba(0,0,0,0.1);*/
        overflow: hidden;
        outline: 2px solid var(--selection);
    }

    .select button {
        width: 100%;
        display: block;
        min-height: 34px; /* not ideal */
        text-align: left;
        background: var(--input);
        border-radius: 0;
    }
    button.current {
        background: var(--button2);
    }
    button:focus {
        outline: none;
    }
</style>
