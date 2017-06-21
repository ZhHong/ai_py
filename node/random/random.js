var ood={}

//随机概率配置
ood.config={};
//
ood.rate_config={};
//盒子
ood.box=[];
//概率
ood.rate={};

ood.config_info ={};


ood.init_random_box =function(){
    for(var i=0;i<ood.config.length;++i){
        var cf = ood.config[i];
        if(cf.rd_ood >0){
            if(cf.max_hit == 999){
                ood.box =ood.box.concat(new Array(cf.rd_ood).fill(cf.rd_index));
            }else{
                if(cf.current_hit < cf.max_hit){
                    var offset = cf.max_hit - cf.current_hit;
                    ood.box =ood.box.concat(new Array(offset).fill(cf.rd_index));
                }
            }
        }
    }
    console.log("init random box :",ood.box.length);
}
ood.init_random_rate =function(){
    var sum = 0;
    for(var i=0;i<ood.config.length;++i){
        var cf = ood.config[i];
        sum += cf.rd_ood;
    }
    for(var i=0;i<ood.config.length;++i){
        var cf = ood.config[i];
        ood.rate[cf.rd_index] =  Math.fround(cf.rd_ood/sum); 
    }
};
ood.init=function(conf){
    ood.config = conf;
    for(var i=0;i<conf.length;++i){
        var tmp = conf[i];
        ood.config_info[tmp.rd_index]= tmp; 
    }
    console.log("init ood config :",ood.config.length)
};
//随机盒子
ood.random_box=function(){
    var rd_len = ood.box.length;
    var rd = Math.floor(Math.random()*rd_len);
    var hit = ood.box[rd];

    console.log(" show me rd hit",rd,hit)
    var hit_info = ood.config_info[hit];

    hit_info.current_hit +=1;
    if(hit_info.max_hit != 999){
        ood.box.splice(rd,1);
    }
    return hit;
};
//随机概率
ood.random_rate=function(){
    var rd = Math.random();
    var min_dis = null;
    var min_index =0;
    for(var a in ood.rate){
        if(min_dis == null){
            min_dis = Math.abs(ood.rate[a] - rd);
            min_index = a;
        }else{
            if(min_dis > Math.abs(ood.rate[a] -rd)){
                min_dis = Math.abs(ood.rate[a] -rd);
                min_dis = a;
            }
        }
    }
    return min_index;
};

exports.ood = ood;