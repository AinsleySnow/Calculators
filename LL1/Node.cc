#include "Node.h"
#include <cmath>

Node::Node()
{
    t = {};
    left = {};
    right = {};
}

Node::Node(const Token& token)
{
    t = token;
    left = {};
    right = {};
}

Node::Node(const Token& token, std::shared_ptr<Node> l, std::shared_ptr<Node> r)
{
    t = token;
    left = l;
    right = r;
}

const Token& Node::GetToken()
{
    return t;
}

std::shared_ptr<Node> Node::GetLeft()
{
    return left;
}

std::shared_ptr<Node> Node::GetRight()
{
    return right;
}

void Node::SetLeft(std::shared_ptr<Node> l)
{
    left = l;
}

void Node::SetRight(std::shared_ptr<Node> r)
{
    right = r;
}

double Node::Yield()
{
    if (t.type != Tag::num)
    {
        double leftside = left->Yield();
        double rightside = right->Yield();
        switch (t.field.op)
        {
        case '+':
            return leftside + rightside;
        case '-':
            return leftside - rightside;
        case '*':
            return leftside * rightside;
        case '/':
            return leftside / rightside;
        case '%':
            return static_cast<long long>(leftside) % static_cast<long long>(rightside);
        case '^':
            return pow(leftside, rightside);
        }

        throw 21;
    }
    else
        return t.field.num;
    
}
