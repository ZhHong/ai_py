exports.makecode = function(str,user_id){
    var ss ="";
    var len = str.length;
    for(var i=0;i<len;++i){
        ss += String.fromCharCode(str.charCodeAt(i)^(user_id%i));
    }
    return ss;
}

exports.cutecode = function(str,user_id){
    var ss = "";
    var len = str.length;
    for(var i=0;i<len;++i){
        ss += String.fromCharCode(str.charCodeAt(i)^(user_id%i));
    }
    return ss;
}