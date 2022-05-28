#ifndef _TOKEN_H_
#define _TOKEN_H_

enum class Tag
{
    num,
    op,
    op1,
    op2,
    op3,
    null
};

struct Token
{
    union
    {
        char op;
        double num;
    } field;
    
    Tag type;
};

#endif // _TOKEN_H_
