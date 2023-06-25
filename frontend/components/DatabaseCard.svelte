<script>
    // these could be improved (async/await + svelte input maybe)

    function backup() {
        fetch('/api/database')
        .then(response => response.blob())
        .then(function(myBlob) {
            var link = document.createElement('a');
            link.setAttribute('href', URL.createObjectURL(myBlob));
            link.setAttribute('download', 'database.db');
            link.click();
        });
    }

    function restore() {
        var upload = document.createElement("input");
        upload.setAttribute("type", "file");
        upload.addEventListener('change', function(e) {
            var file = e.target.files[0];
            // apparently you can't manually change the content-type of the file part
            // it will probably be application/octet-stream
            var formData = new FormData();
            formData.append('file', file);
            fetch('/api/database', {
                method: 'POST',
                body: formData
            });
        });
        upload.click();
    }
</script>

<div class="card">
    <h2>Database</h2>
    <p class="smallgap">
        <button class="primary" on:click={backup}>Backup</button>
        <button class="danger" on:click={restore}>Restore</button>
    </p>
</div>
