#include <cstdio>
#include <iostream>
#include "Parser.h"
#include "utilities/Node.h"
#include "utilities/Token.h"

int main(int argc, char* argv[])
{
    try
    {
        if (argc == 1)
        {
            while (1)
            {
                printf(">> ");
                std::string line;
                std::getline(std::cin, line);
                if (line == "quit")
                    return 0;

                Parser p;
                p.SetLine(line);
                std::shared_ptr<Node> root = p.Parse();

                printf(">> %lf\n", root->Yield());
                // printf(">> %s\n", root->ToString());

            }
        }

        for (int i = 1; i < argc; ++i)
        {
            std::string line = std::string(argv[i]);
            printf(">> %s\n", line.c_str());

            Parser p;
            p.SetLine(line);
            std::shared_ptr<Node> root = p.Parse();

            printf(">> %lf\n", root->Yield());
            // printf(">> %s\n", root->ToString());
        }
    }
    catch (int e)
    {
        printf("Expection: %d\n", e);
    }

    return 0;
}
