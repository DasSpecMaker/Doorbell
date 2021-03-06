var net = require('net');
var fs = require("fs");
var proc= require('process');
var io = require('socket.io-client');
var ffmpegCommand = require('fluent-ffmpeg');
var EventEmitter = require('events')
const {PassThrough} = require('stream')
const readline = require('readline').createInterface({
  input: process.stdin,
  output: process.stdout
})
var socket = io('http://192.168.0.108:9000');
var client = new net.Socket();
let file;
let command;
var passthrustream = new PassThrough();
var recursiveReadline = function(){
  readline.question('Please input a command to send to the server\n', (command) => {
    //console.log("Command:" + command);
    if (command.valueOf() != "0" && command.valueOf() != "1" && command.valueOf() != "2" && command.valueOf() != "3" && command.valueOf() != "4" && command.valueOf() != "5") {
      console.log("invalid input");
      recursiveReadline()
    } else {
      if (command.valueOf() == "1") {
        console.log("Emit 1");
        socket.emit('stream_request');
        // file = fs.createWriteStream('strem.h264').on('finish',()=>{
        //   console.log("Write Finish.");
        //   file.end();
        // }).on('error',()=>{
        //   console.log(".h264 error");
        // })
      } else if (command.valueOf() == "2") {
        socket.emit('stream_snapshot_request');
      } else if (command.valueOf() == "3") {
        client.end()
      }
      recursiveReadline();
    }
  })
}

socket.on('connection',()=>{
  console.log("Connection has been established")
})

socket.on('disconnect',()=>{
  console.log('SocketIO has been disconnected.')
  socket.disconnect();
  if(client){
    client.end();
  }
})
socket.on('stream_response',()=>{
  console.log("Picture Response Received");
  client.connect(8000, '192.168.0.108', function () {
    console.log('CONNECTED TO: ' + '192.168.0.108' + ':' + 8000);
  }).on('ready',()=>{
    command = ffmpegCommand({
      source:client
    }).inputOptions([
      'ffmpeg','-nostats','-hide_banner','-loglevel','panic','-i','-','-f', 'webm', '-'
    ]).noAudio().withSize('320x240').on
  }).pipe(passthrustream);
})

socket.on('button_response',()=>{
  console.log('button has been pressed')
})

socket.on('ultra_m',(data)=>{
  console.log(data);
})

passthrustream.on('data',(chunk)=>{
  
})

client.on('data',(data)=>{
  //console.log("Data received")
  // console.log("video write");
  // file.write(data, (err) => {
  //  console.log("ERROR:" + err);
  // })
})

client.on('end',()=>{
  console.log('Streaming server has closed')
  client.end();
  file.end();
})

recursiveReadline();