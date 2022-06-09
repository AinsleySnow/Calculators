CC = g++
CFLAGS = -Wall -Og
D = descent
U = utilities
L = LL1
LR = LRx

desc: $U/lex.o
	$(CC) $(CFLAGS) $U/lex.o $D/Paser.cc $D/main.cc -o $D/descent

ll: $U/lex.o
	$(CC) $(CFLAGS) -I. $U/lex.o $U/Node.cc $L/main.cc $L/Parser.cc -o $L/LL1

slr: $U/lex.o
	$(CC) $(CFLAGS) -I. $U/lex.o $U/Node.cc $(LR)/SLRTable.cc $(LR)/main.cc $(LR)/Parser.cc -o $(LR)/SLR

$U/lex.o: 
	$(CC) $(CFLAGS) $U/Lexer.cc -c -o $U/lex.o

LL1_table:
	cd tables;\
	python3.9 LL1_table.py;

SLR_table:
	cd tables;\
	python3.9 SLR.py;

LR1_table:
	cd tables;\
	python3.9 LR1_table.py;

clean: 
	rm -f $D/descent
	rm -f $U/lex.o
	rm -f $L/LL1
	rm -f $(LR)/SLR