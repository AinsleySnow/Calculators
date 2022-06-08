#include "Parser.h"
#include "Table.h"
#include <stack>

static int lengthOfRule[11] = {
    3, 3, 1, // expr
    3, 3, 3, 1, // term
    3, 1, // factor
    3, 1 // exponent
};

std::shared_ptr<Node> Parser::Parse()
{
    Token token = lexer.NextToken();
    std::stack<Token> op = {};
    std::stack<std::shared_ptr<Node>> nodes = {};
    std::stack<int> states = {};
    states.push(0); 
    
    while (true)
    {
        const int top = states.top();
        int indexOfToken = Convert(token);
        int action = SLRActionTable[top][indexOfToken];
        if (action > 255) // shift to some state
        {
            states.push(action & ~(1 << 8));
            if (token.type == Tag::num)
                nodes.push(std::make_shared<Node>(token));
            else
                op.push(token);
            token = lexer.NextToken();
        }
        else if (action) // reduce a handle
        {
            for (int i = lengthOfRule[action]; i > 0; --i)
                states.pop();

            switch (action)
            {
            case 0: case 1:
                states.push(SLRGotoTable[states.top()][_expr]);
                nodes.push(MakeNode(op, nodes));
                break;
            case 2:
                states.push(SLRGotoTable[states.top()][_expr]);
                break;
            
            case 3: case 4: case 5:
                states.push(SLRGotoTable[states.top()][_term]);
                nodes.push(MakeNode(op, nodes));
                break;
            case 6:
                states.push(SLRGotoTable[states.top()][_term]);
                break;
            
            case 7:
                states.push(SLRGotoTable[states.top()][_factor]);
                nodes.push(MakeNode(op, nodes));
                break;
            case 8:
                states.push(SLRGotoTable[states.top()][_factor]);
                break;
            
            case 9:
                states.push(SLRGotoTable[states.top()][_exponent]);
                break;
            case 10:
                states.push(SLRGotoTable[states.top()][_exponent]);
                break;
            } 
        }
        else if (!SLRActionTable[top][indexOfToken])
            return nodes.top();
        else
            throw 4;
    }
}

void Parser::SetLine(std::string& l)
{
    line = l;
}

int Parser::Convert(const Token& t)
{
    if (t.type == Tag::num)
        return _num;
    if (t.type == Tag::null)
        return _eof;
    if (t.field.op == '+')
        return _plus;
    if (t.field.op == '-')
        return _minus;
    if (t.field.op == '*')
        return _times;
    if (t.field.op == '/')
        return _divide;
    if (t.field.op == '%')
        return _mod;
    if (t.field.op == '^')
        return _power;
    if (t.field.op == '(')
        return _leftpar;
    if (t.field.op == ')')
        return _rightpar;
        
    return -1;
}

std::shared_ptr<Node> Parser::MakeNode(std::stack<Token>& op, std::stack<std::shared_ptr<Node>>& nodes)
{
    Token t = op.top();
    op.pop();
    std::shared_ptr<Node> right = nodes.top();
    nodes.pop();
    std::shared_ptr<Node> left = nodes.top();
    nodes.pop();
    return std::make_shared<Node>(t, left, right);
}
