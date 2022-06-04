#include "Parser.h"
#include <stack>

std::shared_ptr<Node> Parser::Parse()
{
    std::stack<int> stack = {};
    std::stack<std::shared_ptr<Node>> nodes = {};
    std::stack<Token> op = {};

    Token token = lexer.NextToken();
    stack.push(-1); // eof
    stack.push(_expr);

    while (true)
    {
        if (stack.top() == -1 && token.type == Tag::null)
            return nodes.top();
        else if (stack.top() > 7 || stack.top() == -1)
        {
            if (Matches(stack.top(), token))
            {
                stack.pop();
                if (token.type == Tag::num)
                    nodes.push(std::make_shared<Node>(token));
                else if (token.type != Tag::op)
                {
                    if (!op.empty() && op.top().type == token.type)
                    {
                        Token t = op.top();
                        op.pop();
                        std::shared_ptr<Node> right = nodes.top();
                        nodes.pop();
                        std::shared_ptr<Node> left = nodes.top();
                        nodes.pop();
                        nodes.push(std::make_shared<Node>(t, left, right));
                    }
                    op.push(token);
                }
                else if (token.type == Tag::op && token.field.op == '(')
                    op.push(token);
                else if (token.type == Tag::op && token.field.op == ')')
                    op.pop();
                
                token = lexer.NextToken();
            }
            else
                throw 1;
        }
        else // focus is a non-terminal
        {
            int rule = parseTable[stack.top()][Convert(token) >> 4];
            if (rule != -1)
            {
                stack.pop();
                if (grammars[rule][2] == _epsilon && !op.empty())
                {
                    if (Matches(grammars[rule][1], op.top().type))
                    {
                        Token t = op.top();
                        op.pop();
                        std::shared_ptr<Node> right = nodes.top();
                        nodes.pop();
                        std::shared_ptr<Node> left = nodes.top();
                        nodes.pop();
                        nodes.push(std::make_shared<Node>(t, left, right));
                    }
                }
                
                for (int i = grammars[rule][0]; i >= 2; --i)
                    if (grammars[rule][i] != _epsilon)
                        stack.push(grammars[rule][i]);
            }
            else
                throw 4;
        }
    }
}

bool Parser::Matches(int nonterminal, Tag tag)
{
    switch (tag)
    {
    case Tag::op1:
        return nonterminal == _expr_p;
    case Tag::op2:
        return nonterminal == _term_p;
    case Tag::op3:
        return nonterminal == _factor_p;
    }

    return false;
}

bool Parser::Matches(int terminal, const Token& t)
{
    switch (terminal)
    {
    case _plus:
        return t.field.op == '+';
    case _minus:
        return t.field.op == '-';
    case _times:
        return t.field.op == '*';
    case _divide:
        return t.field.op == '/';
    case _mod:
        return t.field.op == '%';
    case _power:
        return t.field.op == '^';
    case _leftpar:
        return t.field.op == '(';
    case _rightpar:
        return t.field.op == ')';
    case _num:
        return t.type == Tag::num;
    case _eof:
        return t.type == Tag::null;
    }

    return false;
}

int Parser::Convert(const Token& t)
{
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
    if (t.type == Tag::num)
        return _num;
    if (t.type == Tag::null)
        return _eof;
        
    return -1;
}

void Parser::SetLine(std::string& l)
{
    lexer.SetLine(l);
}
