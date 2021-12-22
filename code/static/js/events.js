// events.js

export default {
    get: function() {
        fetch('/api/events')
        .then(function(response) {
            return response.json();
        })
        .then(function(data) {
            var html = '<table>';
            for (var event of data) {
                html += '<tr>';

                /*for (var key in event) {
                    html += '<td>' + event[key] + '</td>';
                }*/
                html += '<td>' + new Date(event.time).toLocaleString() + '</td>';
                html += '<td>' + event.level + '</td>';
                html += '<td>' + event.message + '</td>';

                html += '</tr>';
            }
            html += '</table>';
            document.getElementById('api_data').innerHTML = html;
        });
    }
}
