// events.js

function get() {
    fetch('/api/events?channel=DEBUG&channel=INFO&channel=WARNING&limit=15')
    .then(function(response) {
        return response.json();
    })
    .then(function(data) {
        var html = '';
        if(data.length > 0) {
            html = '<table><tr><th>Time</th><th>Channel</th><th>Message</th></tr>';
            for (var event of data) {
                html += '<tr>';
                html += '<td>' + new Date(event.time).toLocaleString() + '</td>';
                html += '<td>' + event.channel + '</td>';
                html += '<td>' + event.message + '</td>';
                html += '</tr>';
            }
            html += '</table>';
        } else {
            html += 'No events found';
        }
        document.getElementById('event_list').innerHTML = html;
    });
}

export default {
    get: get
}
