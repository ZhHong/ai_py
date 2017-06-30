#ifndef __SIMPLEH__
#define __SIMPLEH__

namespace simple{
    //单个字符异或运算
    inline char MakecodeChar(char c,int key){
        return c^key;
    }
    //单个字符解密
    inline char CutcodeChar(char c,int key){
        return c^key;
    }

    //加密
    inline void Makecode(char *pstr){
        int len=strlen(pstr);//获取长度
        for(int i=0;i<len;i++)
            *(pstr+i)=MakecodeChar(*(pstr+i),i%9);
    }


    //解密
    inline void Cutecode(char *pstr){
        int len=strlen(pstr);
        for(int i=0;i<len;i++)
            *(pstr+i)=CutcodeChar(*(pstr+i),i%9);
    }
}
#endif