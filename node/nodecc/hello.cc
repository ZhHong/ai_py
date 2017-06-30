// hello.cc
#include <node.h>
#include "Crypt.h"
#include "simple.h"

namespace demo
{

using v8::Exception;
using v8::FunctionCallbackInfo;
using v8::Isolate;
using v8::Local;
using v8::Object;
using v8::String;
using v8::Value;
using v8::Number;
using v8::Function;

//simple example
void ShowHello(const FunctionCallbackInfo<Value> &args)
{
    Isolate *isolate = args.GetIsolate();
    args.GetReturnValue().Set(String::NewFromUtf8(isolate, "world"));
}

//args example
void AddNumber(const FunctionCallbackInfo<Value> &args)
{
    Isolate *isolate = args.GetIsolate();
    if (args.Length() < 2)
    {
        isolate->ThrowException(Exception::TypeError(String::NewFromUtf8(isolate, "Wrong number of argments")));
        return;
    }
    if (!args[0]->IsNumber() || !args[1]->IsNumber())
    {
        isolate->ThrowException(Exception::TypeError(String::NewFromUtf8(isolate, "Wrong argments")));
        return;
    }

    double value = args[0]->NumberValue() + args[1]->NumberValue();
    Local<Number> num = Number::New(isolate, value);

    args.GetReturnValue().Set(num);
}
//callback example
void ShowCallBack(const FunctionCallbackInfo<Value> &args){
    Isolate *isolate = args.GetIsolate();
    Local<Function> cb = Local<Function>::Cast(args[0]);
    const unsigned argc = 1;
    Local<Value> argv[argc] ={String::NewFromUtf8(isolate,"i am a callback")};
    cb->Call(Null(isolate),argc,argv);
}

//gen key
void GenMyKey(const FunctionCallbackInfo<Value> & args){
    Isolate *isolate = args.GetIsolate();
    std::string s1;
    std::string s2; 
    Crypt::GenKey(&s1,&s2);
    // std::reverse(s1.begin(),s1.end());
    // std::reverse(s2.begin(),s2.end());
    Local<Object> obj = Object::New(isolate);
    Local<String> retval_p = String::NewFromUtf8(isolate,s1.c_str());
    Local<String> retval_pri = String::NewFromUtf8(isolate,s2.c_str());
    obj->Set(String::NewFromUtf8(isolate,"public_key"),retval_p);
    obj->Set(String::NewFromUtf8(isolate,"private_key"),retval_pri);    
    args.GetReturnValue().Set(obj);
}
//gen secret
void GenSecret(const FunctionCallbackInfo<Value> & args){
    Isolate *isolate = args.GetIsolate();
    String::Utf8Value pub(args[0]);
    String::Utf8Value priv(args[0]);
    std::string p(*pub);
    std::string pri(*priv);
    std::reverse(p.begin(),p.end());
    std::reverse(pri.begin(),pri.end());
    std::string s;
    Crypt::GenSecret(p,pri,s);
    Local<Object> obj = Object::New(isolate);
    Local<String> retval = String::NewFromUtf8(isolate,s.c_str());
    obj->Set(String::NewFromUtf8(isolate,"secret"),retval);
    args.GetReturnValue().Set(obj);
}

void encode(const FunctionCallbackInfo<Value> &args){
    Isolate *isolate = args.GetIsolate();
    String::Utf8Value txt(args[0]);
    // unsigned long offset =args[1] ->NumberValue();
    std::string text(*txt);
    char * tt = (char *)text.data();
    simple::Makecode(tt);
    text = tt;
    Local<String> retval = String::NewFromUtf8(isolate,text.c_str());
    args.GetReturnValue().Set(retval);
}

void decode(const FunctionCallbackInfo<Value> &args){
    Isolate *isolate = args.GetIsolate();
    String::Utf8Value txt(args[0]);
    // unsigned long offset =args[1] ->NumberValue();
    std::string text(*txt);
    char * tt = (char *)text.data();
    simple::Cutecode(tt);
    text = tt;
    Local<String> retval = String::NewFromUtf8(isolate,text.c_str());
    args.GetReturnValue().Set(retval);
}

void Init(Local<Object> exports, Local<Object> module){
    NODE_SET_METHOD(exports, "hello", ShowHello);
    NODE_SET_METHOD(exports, "add", AddNumber);
    NODE_SET_METHOD(exports,"do_call",ShowCallBack);
    NODE_SET_METHOD(exports,"gen_key",GenMyKey);
    NODE_SET_METHOD(exports,"gen_secret",GenSecret);
    NODE_SET_METHOD(exports,"encode",encode);
    NODE_SET_METHOD(exports,"decode",decode);
}

NODE_MODULE(addon, Init)

} // namespace demo