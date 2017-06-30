var addon = require('./build/Release/addon');

console.log(addon.hello());
console.log(addon.add(1,2));
addon.do_call(function(msg){
    console.log(msg);
})
var obj1 = addon.gen_key();
console.log(obj1)
var obj2 = addon.gen_key();
console.log(obj2);

var b64p1 = new Buffer(obj1.public_key,'hex').toString('base64')
var b64pri1 = new Buffer(obj1.private_key,'hex').toString('base64')

var b64p2 = new Buffer(obj2.public_key,'hex').toString('base64')
var b64pri2 = new Buffer(obj2.private_key,'hex').toString('base64')

console.log(b64p1)
console.log(b64pri1)
console.log(b64p2)
console.log(b64pri2)

var s1obj = addon.gen_secret(obj1.public_key,obj2.private_key);
var s2obj = addon.gen_secret(obj2.public_key,obj1.private_key);


console.log(s1obj)
console.log(s2obj)

var sss1 = addon.encode('woshihaoren');
console.log(sss1);

var sss2 = addon.decode(sss1);
console.log(sss2);

var ss = {
    account:'我的我的',
    target:123456,
    ingot:1000,
    cacai:'dawddddddddddddddawdadddddddddddddddddddddddddddddd',
    statistic:{
        stat:1,
        status:1000,
        aeewe:123
    }
}



var simple = require('./simple');
var ssstr = JSON.stringify(ss);

var a1 = addon.encode(ssstr);
var a2 = addon.decode(a1);
var b64a = new Buffer(a1,'utf8').toString('base64');
console.log(b64a);
console.log(a1);
console.log(a2);

console.log("======================================")
console.log(ssstr)
var aa1 = simple.makecode(ssstr,100211);
var aa2 = simple.cutecode(aa1,100211);
var b64a1 = new Buffer(aa1,'utf8').toString('base64');
console.log(b64a1);
console.log(aa1);
console.log(aa2);