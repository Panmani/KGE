var express = require('express');
var app = express();
var path = require('path');

// app.get('/', function(req, res) {
//     res.sendFile(path.join(__dirname + '/../index.html'));
// });

app.use('/', express.static(path.join(__dirname, '..')))

// viewed at http://localhost:3000
var server = app.listen(3000, "127.0.0.1", function (){
    var host = server.address().address;
    var port = server.address().port;
    console.log('KGE server listening at http://%s:%s', host, port);
});
