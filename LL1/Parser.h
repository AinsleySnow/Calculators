#ifndef _PARSER_H_
#define _PARSER_H_

#include <memory>
#include "utilities/Lexer.h"
#include "utilities/Token.h"
#include "grammar.h"
#include "utilities/Node.h"

class Parser
{
private:
    Lexer lexer;
    Token current;
    std::string line;

    bool Matches(int terminal, const Token& t);
    bool Matches(int, Tag);
    int Convert(const Token& t);

public:
    std::shared_ptr<Node> Parse();
    void SetLine(std::string&);
};

#endif // _PARSER_H_
