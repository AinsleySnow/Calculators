CC = g++
CFLAGS = -Wall -Og
D = descent
U = utilities
L = LL1

desc: 
	$(CC) $(CFLAGS) $D/Lexer.cc $D/Paser.cc $D/main.cc

ll:
	$(CC) $(CFLAGS) -I. $L/Node.cc $U/Lexer.cc $L/main.cc $L/Parser.cc

clean: 
	rm -f $D/descent
