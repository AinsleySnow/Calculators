#include "Parser.h"
#include "Table.h"
#include <stack>

#ifdef SLR
#define actionTable SLRActionTable
#define gotoTable SLRGotoTable
#elif LR1
#define actionTable LR1ActionTable
#define gotoTable LR1GotoTable
#elif LALR
#define actionTable LALRActionTable
#define gotoTable LALRGotoTable
#endif

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
        int action = actionTable[top][indexOfToken];
        // printf("indexoftoken = %d, action = %d, top = %d\n", indexOfToken, action, top);
        if (action > 0 && action < 256) // shift to some state
        {
            states.push(action);
            if (token.type == Tag::num)
                nodes.push(std::make_shared<Node>(token));
            else if (token.type != Tag::op)
                op.push(token);
            token = lexer.NextToken();
        }
        else if (action > 255) // reduce a handle
        {
            int indexOfRule = action & ~(1 << 8);
            for (int i = lengthOfRule[indexOfRule]; i > 0; --i)
                states.pop();

            switch (indexOfRule)
            {
            case 0: case 1:
                states.push(gotoTable[states.top()][_expr]);
                nodes.push(MakeNode(op, nodes));
                break;
            case 2:
                states.push(gotoTable[states.top()][_expr]);
                break;
            
            case 3: case 4: case 5:
                states.push(gotoTable[states.top()][_term]);
                nodes.push(MakeNode(op, nodes));
                break;
            case 6:
                states.push(gotoTable[states.top()][_term]);
                break;
            
            case 7:
                states.push(gotoTable[states.top()][_factor]);
                nodes.push(MakeNode(op, nodes));
                break;
            case 8:
                states.push(gotoTable[states.top()][_factor]);
                break;
            
            case 9:
                states.push(gotoTable[states.top()][_exponent]);
                break;
            case 10:
                states.push(gotoTable[states.top()][_exponent]);
                break;
            } 
        }
        else if (!action)
            return nodes.top();
        else
            throw 4;
    }
}

void Parser::SetLine(std::string& l)
{
    lexer.SetLine(l);
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
