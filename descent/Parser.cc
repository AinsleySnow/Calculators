#include "Parser.h"

void Parser::SetLine(std::string& s)
{
    lexer.SetLine(s);
}

void Parser::move()
{
    current = lexer.NextToken();
}

void Parser::move(char op)
{
    if (current.field.op != op)
        throw 1;
    move();
}

Token Parser::expr()
{
    Token newToken = term();

    while (current.type == Tag::op1)
    {
        switch (current.field.op)
        {
        case '+':
            move();
            newToken.field.num += term().field.num;
            break;

        case '-':
            move();
            newToken.field.num -= term().field.num;
            break;
        }
    }

    return newToken;
}

Token Parser::term()
{
    Token newToken = factor();

    while (current.type == Tag::op2)
    {
        switch (current.field.op)
        {
        case '*':
            move();
            newToken.field.num *= factor().field.num;
            break;

        case '/':
            move();
            newToken.field.num /= factor().field.num;
            break;

        case '%':
            move();
            newToken.field.num = static_cast<long>(newToken.field.num) % 
                static_cast<long>(factor().field.num);
            break;            
        }
    }

    return newToken;
}

Token Parser::factor()
{
    Token newToken = exponent();

    if (current.type == Tag::op3)
    {
        move();
        newToken.field.num = pow(newToken.field.num, exponent().field.num);
    }

    return newToken;
}

Token Parser::exponent()
{
    Token newToken;
    
    if (current.type == Tag::op && current.field.op == '(')
    {
        move();
        newToken = expr();
        move(')');
        return newToken;
    }
    else if (current.type == Tag::num)
    {
        newToken = current;
        move();
        return newToken;
    }

    throw 2;
}

Token Parser::Parse()
{
    move();
    return expr();
}
