// database.js

export default {
    backup: function() {
        fetch('/api/database')
        .then(response => response.blob())
        .then(function(myBlob) {
            var link = document.createElement('a');
            link.setAttribute('href', URL.createObjectURL(myBlob));
            link.setAttribute('download', 'database.db');
            link.click();
        });
    },
    restore: function() {
        var upload = document.createElement("input");
        upload.setAttribute("type", "file");
        upload.addEventListener('change', function(e) {
            var file = e.target.files[0];
            var formData = new FormData();
            formData.append('file', file);
            fetch('/api/database', {
                method: 'POST',
                body: formData
            });
        });
        upload.click();
    }
}
