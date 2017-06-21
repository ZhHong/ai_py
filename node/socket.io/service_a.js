/**
 * service a
 */

var app = require('express')();
var secret = require('../secret_test/secret');

var server_name = '[service a]'
var port =15151

var io = require('socket.io')(port);

var clients ={}

exports.start = function(config){
    io.sockets.on('connection',function(socket){
        //握手
        socket.on('handshake',function(data){
            console.log(server_name +" on handshake data =>",Object.keys(data))
            var dhblob = secret.dh64_gen_key();
            var rdchan = secret.random_b64();
            socket.fdid = data.id;
            socket.secret = secret.dh64_secret(dhblob,data.data)
            socket.hmac = secret.hmac64(rdchan,socket.secret);
            socket.emit('handshake',{id:rdchan,key:dhblob.getPublicKey('base64')})
        });
        //验证
        socket.on('hmac',function(data){
            if(socket.hmac === data.cert){
                socket.cert = true;
                clients[socket.fdid] = socket;
                var msg = secret.aes_encrypt("hello",socket.secret);
                socket.emit('challenge',msg);
            }else{
                socket.disconnect(true);
            }
        });

        //断开连接
        socket.on('disconnect',function(data){
            console.warn(server_name +' client disconneted.');
            socket.disconnect();
        });
        //心跳
        socket.on('selfping',function(data){
            socket.last_tick_time = Math.floor(Date.now()/1000);
            console.log(server_name + '===>',data)
            if(socket.cert){
                socket.emit('selfping','pong')
            }else{
                socket.disconnect(true);
            }
        });
    })
    console.log(server_name +" running on: "+port)
}

function tick(){
    // console.log(clients)
    var now = Math.floor(Date.now()/1000);
    for(var a in clients){
        if(clients[a].last_tick_time +40 <now){
            console.log("client [%s] out of time",clients[a].fdid)
        }
    }
}

setInterval(tick,20000);