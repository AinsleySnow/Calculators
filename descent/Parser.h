#ifndef _PARSER_H_
#define _PARSER_H_

#include <string>
#include <cmath>
#include "utilities/Token.h"
#include "utilities/Lexer.h"

class Parser
{
private:
    Lexer lexer;
    Token current;

    Token expr();
    Token term();
    Token factor();
    Token exponent();
    void move();
    void move(char);
    
public:
    void SetLine(std::string&);
    Token Parse();
};

#endif // _PARSER_H_
