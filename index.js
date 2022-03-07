var app = require('express')();
var http = require('http').Server(app);
var io = require('socket.io')(http, {
    cors: {
      origin: '*' ,
      methods: ["GET", "POST"],
      allowedHeaders: ["my-custom-header"],
      credentials: true
    }
});
const { exec } = require('child_process')
var sh = "echo test_data/test.wav | adintool -in file -out adinnet -server localhost";

io.on('connection', function(socket){ 
  //ソケット接続時
  console.log('a user connected'); 
  //ブラウザ側からの音声の受け取り
  socket.on('upload', function(data) {

    var fs = require('fs');
    var writeFile = data.file;
    var writePath = './test_data/test.wav'; 

    var writeStream = fs.createWriteStream(writePath);
    writeStream.on('drain', function () {} )
                      .on('error', function (exception) {
                      //エラー処理
                           console.log("exception:"+exception);
                       }) 
                      .on('close', function () {
                        console.log('ファイル受け取り成功');
                        //シェルでjuliusに送る
                        exec(sh, (err, stdout, stderr) => {
                          if (err) {
                            console.log(`stderr: ${stderr}`)
                            return
                          }
                          console.log(`stdout: ${stdout}`)
                        })
                      })  
                      .on('pipe', function (src) {}); 

    writeStream.write(writeFile,'binary');
    writeStream.end();
  }); 
  //pythonファイルからの受け取り
  socket.on('v-command', function(cmd) {
    console.log(`GetCommand:cmd=${cmd}`);
    //ブラウザへ返す
    io.emit('command', cmd); 
  });
});



http.listen(3001, function(){ 
    console.log('listening on *:3001'); }
);
