var secret = require('./secret')

var dh1 = secret.dh64_gen_key();
var dh2 = secret.dh64_gen_key();

var s1 = secret.dh64_secret(dh1,dh2.getPublicKey('base64'));
var s2 = secret.dh64_secret(dh2,dh1.getPublicKey('base64'));

console.log("s1 :",s1);
console.log("s2 :",s2);

var plantext ='hello crypto.';
var encrypto_text = secret.aes_encrypt(plantext,s1);
var decrypto_text = secret.aes_decrypt(encrypto_text,s2);

console.log("plantext       :",plantext);
console.log("encrypto_text  :",encrypto_text);
console.log("decrypto_text  :",decrypto_text);