// events.js

export default {
    get: function() {
        fetch('/api/events')
        .then(function(response) {
            return response.json();
        })
        .then(function(data) {
            var html = '<table>';
            for (var log of data) {
                html += '<tr>';
                for (var key in log) {
                    html += '<td>' + log[key] + '</td>';
                }
                html += '</tr>';
            }
            html += '</table>';
            document.getElementById('api_data').innerHTML = html;
        });
    }
}