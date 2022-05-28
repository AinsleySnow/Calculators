#ifndef _LEXER_H_
#define _LEXER_H_

#include <string>
#include <cctype>
#include "Token.h"

class Lexer
{
private:
    std::string line;
    int pos = 0;
    char c = 0;

    inline char readChar();
    inline void unreadChar();
    
public:
    void SetLine(std::string&);
    Token NextToken();
};

#endif // _LEXER_H_
