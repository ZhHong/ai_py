/**
 * client test
 */

var io =require('socket.io-client');
var secret = require('../secret_test/secret');
var socket_a = io.connect('ws://localhost:15151');
var socket_b = io.connect('ws://localhost:15152');

var user ={};

//////////////scoket1/////////////////////////////
socket_a.on('connect',function(data){
    user.socket_a = socket_a;
    user.fdid_a = secret.md5_16(secret.random_b64());
    user.dhblob_a = secret.dh64_gen_key();
    user.socket_a.emit('handshake',{id:user.fdid_a,data:user.dhblob_a.getPublicKey('base64')});
});

socket_a.on('handshake',function(data){
    console.warn("server 1 handshake data ===>",Object.keys(data));
    user.secret_a = secret.dh64_secret(user.dhblob_a,data.key);
    var hmac = secret.hmac64(data.id,user.secret_a);
    user.hmac_a = hmac;
    user.socket_a.emit('hmac',{cert:user.hmac_a})
});

socket_a.on('challenge',function(data){
    var c = data;
    var decrypto_text = secret.aes_decrypt(c,user.secret_a);
    console.log("socket a challenge data: ",decrypto_text)
    socket_a.cert = true;
});

socket_a.on("disconnect",function(){
    console.log('server 1 disconneted.')
    socket_a.close();
});

socket_a.on("selfping",function(data){
    console.log("socket a :",data);
});

//////////////////socket2/////////////////////////
socket_b.on('connect',function(data){
    user.socket_b = socket_b;
    user.fdid_b = secret.md5_16(secret.random_b64());
    user.dhblob_b = secret.dh64_gen_key();
    user.socket_b.emit('handshake',{id:user.fdid_b,data:user.dhblob_b.getPublicKey('base64')});
});

socket_b.on('handshake',function(data){
    console.warn("server 1 handshake data ===>",Object.keys(data));
    user.secret_b = secret.dh64_secret(user.dhblob_b,data.key);
    var hmac = secret.hmac64(data.id,user.secret_b);
    user.hmac_b = hmac;
    user.socket_b.emit('hmac',{cert:user.hmac_b})
});

socket_b.on('challenge',function(data){
    var c = data;
    var decrypto_text = secret.aes_decrypt(c,user.secret_b);
    console.log("scoket b challenge data: ",decrypto_text)
    socket_b.cert = true;
});

socket_b.on("disconnect",function(){
    console.log('server 2 disconneted.')
    socket_b.close();
});

socket_b.on("selfping",function(data){
    console.log("socket b :",data);
});


function tick(){
    if(user.socket_a.cert){
        user.socket_a.emit('selfping','ping');
    }
    if(user.socket_b.cert){
        user.socket_b.emit('selfping','ping');
    }
}

setInterval(tick,10000);