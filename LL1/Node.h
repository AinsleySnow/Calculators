#ifndef _NODE_H_
#define _NODE_H_

#include <string>
#include <memory>
#include "utilities/Token.h"

class Node
{
private:
    Token t;  
    std::shared_ptr<Node> left;
    std::shared_ptr<Node> right;
    
public:
    Node();
    Node(const Token&);
    Node(const Token&, std::shared_ptr<Node>, std::shared_ptr<Node>);

    const Token& GetToken();
    void SetToken();
    std::shared_ptr<Node> GetLeft();
    std::shared_ptr<Node> GetRight();
    void SetLeft(std::shared_ptr<Node>);
    void SetRight(std::shared_ptr<Node>);

    double Yield();
    std::string ToString();
};

#endif // _NODE_H_
