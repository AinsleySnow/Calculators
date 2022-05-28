#include "Lexer.h"

void Lexer::SetLine(std::string& s)
{
    line = s;
}

Token Lexer::NextToken()
{
    Token token;
    char c;
    while (isblank(c = readChar()));
    if (!c)
    {
        token.type = Tag::null;
        return token;
    } 
    
    if (!isdigit(c)) 
    {
        token.field.op = c;
        if (c == '+' || c == '-')
            token.type = Tag::op1;
        else if (c == '/' || c == '*' || c == '%')
            token.type = Tag::op2;
        else if (c == '^')
            token.type = Tag::op3;
        else
            token.type = Tag::op;
        return token;
    }

    // We suppose all input strings are well-formatted.
    double num = c - '0';
    while (isdigit(c = readChar())) 
    {
        num *= 10;
        num += c - '0';
    }

    if (c == '.') 
    {
        double frac = 0, d = 10;
        while (isdigit(c = readChar())) 
        {
            frac += (c - '0') / d;
            d *= 10;
        }
        num += frac;
    }
    if (c)
        unreadChar();
    token.field.num = num;
    token.type = Tag::num;
    
    return token;
}

inline char Lexer::readChar()
{
    if (pos < line.length())
        return line[pos++];
    return 0;
}

inline void Lexer::unreadChar()
{
    pos--;
}
