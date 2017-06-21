var ood = require('./random').ood;


var config =[];

for(var i=0;i<10;i++){
    var tmp ={
        rd_index:i,
        rd_ood: Math.pow((10-i),4),
        max_hit:999,
        current_hit:0,
        route_name:'随机项'+i,
    }
    config.push(tmp);
}

config[7].max_hit =10;
config[8].max_hit =10;
config[9].max_hit =1;


ood.init(config);
ood.init_random_box();
ood.init_random_rate();

console.log("OOD RATE:",ood.rate);

var hit_map ={};

function tick(){
    //test for box
    var hit =ood.random_box();
    console.log("ood box length----->",ood.box.length);
    console.log("hit index --------->",hit);
    //test for rate
    var hit2 = ood.random_rate();
    console.log("rate hit index ---->",hit2)
    if(!hit_map[hit]){
        hit_map[hit] =1;
    }else{
        hit_map[hit] +=1;
    }
    var mem = process.memoryUsage();
    var format = function(bytes) {  
            return (bytes/1024/1024).toFixed(2)+'MB';  
    }; 
    console.log('Process: heapTotal '+format(mem.heapTotal) + ' heapUsed ' + format(mem.heapUsed) + ' rss ' + format(mem.rss));
}


setInterval(tick,5000);