// events.js

export default {
    get: function() {
        fetch('/api/events')
        .then(function(response) {
            return response.json();
        })
        .then(function(data) {
            var html = '<table><tr><th>Time</th><th>Channel</th><th>Message</th></tr>';
            for (var event of data) {
                html += '<tr>';
                html += '<td>' + new Date(event.time).toLocaleString() + '</td>';
                html += '<td>' + event.channel + '</td>';
                html += '<td>' + event.message + '</td>';
                html += '</tr>';
            }
            html += '</table>';
            document.getElementById('event_list').innerHTML = html;
        });
    }
}
