var express = require('express');
var app = express();
var path = require('path');
var multer  = require('multer');
// var upload = multer({ dest: 'uploads/' });

var UPLOAD_DIR = 'uploads/';
var upload = multer({
  dest: UPLOAD_DIR,
  fileFilter: function (req, file, cb) {

    var filetypes = /zip|text/;

    console.log(req, "=======", file, cb);

    if (filetypes.test(file.mimetype)) {
      return cb(null, true);
    }
    req.fileValidationError = "Error: File upload only supports the following filetypes - " + filetypes;
    return cb(null, false, new Error('goes wrong on the mimetype'));
    // cb(new Error("Error: File upload only supports the following filetypes - " + filetypes));
  }
});

if (!String.prototype.format) {
  String.prototype.format = function() {
    var args = arguments;
    return this.replace(/{(\d+)}/g, function(match, number) {
      return typeof args[number] != 'undefined'
        ? args[number]
        : match
      ;
    });
  };
}

// app.get('/', function(req, res) {
//     res.sendFile(path.join(__dirname + '/../index.html'));
// });

app.use('/', (req, res, next) => {
  console.log(req.method +  " request from " + req.connection.remoteAddress + " at " + req.url);
  next()
})

app.use('/', express.static(path.join(__dirname, '..')))

app.post('/upload', upload.single('inputfile'), function (req, res, next) {
  // req.file is the `avatar` file
  // req.body will hold the text fields, if there were any
  // console.log(req.body);
  if(req.fileValidationError) {
    res.status(415)
    return res.end(req.fileValidationError);
  } else {
    // File ID
    var fid = req.file.filename;
    // console.log(req.file.filename)

    const { exec } = require("child_process");

    var txt_filename = fid + ".txt";
    var input_buffer = UPLOAD_DIR + "/" + fid;
    // var loc = window.location.pathname;
    var cwd = process.cwd();
    console.log(cwd);
    // var command = "mv " + UPLOAD_DIR + "/" + fid + " " + UPLOAD_DIR + "/" + fid + ".txt ; "
    // command += 'mkdir ' + UPLOAD_DIR + "/" + fid + " ; ";
    // command += "mv " + UPLOAD_DIR + "/" + fid + ".txt " + UPLOAD_DIR + "/" + fid + " ; ";

    var command = "mv {0} {1} ; ".format(input_buffer, UPLOAD_DIR + "/" + txt_filename);
    command += "mkdir {0} ; ".format(input_buffer);
    command += "mv {0} {1} ; ".format(UPLOAD_DIR + "/" + txt_filename, input_buffer);
    command += "cd KGE ; ";
    command += "python pipeline.py {0}".format(path.join(cwd, input_buffer));
    // command += "python -c 'import extract_sfm \nextract_sfm.extract(\"{0}\")' ; ".format(input_buffer);

    exec(command, (error, stdout, stderr) => {
        if (error) {
            console.log(`error: ${error.message}`);
            return;
        }
        if (stderr) {
            console.log(`stderr: ${stderr}`);
            return;
        }
        console.log(`stdout: ${stdout}`);
    });


    res.send('Upload successful!')
  }
})

// viewed at http://localhost:3000
var server = app.listen(3000, "127.0.0.1", function (){
    var host = server.address().address;
    var port = server.address().port;
    console.log('KGE server listening at http://%s:%s', host, port);
});
