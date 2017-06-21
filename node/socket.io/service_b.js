/**
 * service b
 */
var app = require('express')();
var secret = require('../secret_test/secret');
var port =15152
var server_name = '[service b]'

exports.start = function(config){
    var io = require('socket.io')(port);
    io.sockets.on('connection',function(socket){

        //握手
        socket.on('handshake',function(data){
            console.log("on handshake data =>",Object.keys(data))
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
                var msg = secret.aes_encrypt('world',socket.secret);
                socket.emit('challenge',msg);
            }else{
                socket.disconnect(true);
            }
        });

        //断开连接
        socket.on('disconnect',function(data){
            console.warn('client disconneted.');
            socket.disconnect(true);
        });
        //心跳
        //内置有ping 所以这里不能用ping
        socket.on('selfping',function(data){
            console.log(server_name + '===>',data)
            if(socket.cert){
                socket.emit('selfping','pong')
            }else{
                socket.disconnect();
            }
        });
    })
    console.info(server_name+" running on:"+port)
}