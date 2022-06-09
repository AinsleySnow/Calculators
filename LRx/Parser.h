#ifndef _PARSER_H_
#define _PARSER_H_

#include <memory>
#include <stack>
#include "utilities/Lexer.h"
#include "utilities/Token.h"
#include "utilities/Node.h"

class Parser
{
private:
    Lexer lexer;
    Token current;

    int Convert(const Token& t);
    std::shared_ptr<Node> MakeNode(std::stack<Token>&, std::stack<std::shared_ptr<Node>>&);

public:
    std::shared_ptr<Node> Parse();
    void SetLine(std::string&);
};

#endif // _PARSER_H_
