// users.js

export default {
    get: function() {
        fetch('/api/users')
        .then(function(response) {
            return response.json();
        })
        .then(function(data) {
            var html = '<table><tr><th>Name</th><th>Pin</th><th>Card</th></tr>';
            for (var user of data) {
                //var pin = user.pin ? user.pin.replace(/./g, '*') : '';
                //var card = user.card && user.facility ? user.card.replace(/./g, '*') : '';
                var pin = user.pin || '';
                var card = user.card || '';

                html += '<tr>';
                html += '<td>' + user.name + '</td>';
                html += '<td>' + pin + '</td>';
                html += '<td>' + card + '</td>';
                html += '</tr>';
            }
            html += '</table>';
            document.getElementById('user_list').innerHTML = html;
        });
    }
}
