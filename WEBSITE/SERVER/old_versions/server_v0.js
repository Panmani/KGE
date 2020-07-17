var express = require('express');
var app = express();
var path = require('path');
var multer  = require('multer');
// var upload = multer({ dest: 'uploads/' });

var upload = multer({
  dest: 'uploads/',
  fileFilter: function (req, file, cb) {

    var filetypes = /zip|txt/;
    var mimetype = filetypes.test(file.mimetype);
    var extname = filetypes.test(path.extname(file.originalname).toLowerCase());

    console.log(req, "=======", file, cb);
    console.log(mimetype, extname);

    if (mimetype && extname) {
      return cb(null, true);
    }
    req.fileValidationError = "Error: File upload only supports the following filetypes - " + filetypes;
    return cb(null, false, new Error('goes wrong on the mimetype'));
    // cb(new Error("Error: File upload only supports the following filetypes - " + filetypes));
  }
});

// app.get('/', function(req, res) {
//     res.sendFile(path.join(__dirname + '/../index.html'));
// });

app.use('/', (req, res, next) => {
  console.log(req.method +  " request from " + req.connection.remoteAddress + " at " + req.url);
  next()
})

app.use('/', express.static(path.join(__dirname, '..')))

app.post('/upload', upload.single('zipfile'), function (req, res, next) {
  // req.file is the `avatar` file
  // req.body will hold the text fields, if there were any
  if(req.fileValidationError) {
    return res.end(req.fileValidationError);
  }
})

// viewed at http://localhost:3000
var server = app.listen(3000, "127.0.0.1", function (){
    var host = server.address().address;
    var port = server.address().port;
    console.log('KGE server listening at http://%s:%s', host, port);
});
