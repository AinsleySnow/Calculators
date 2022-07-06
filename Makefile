CC = g++
CFLAGS = -Wall -Og
D = descent
U = utilities
L = LL1
LR = LRx
G = generated

desc: $U/lex.o
	$(CC) $(CFLAGS) $U/lex.o $D/Paser.cc $D/main.cc -o $D/descent

ll: $U/lex.o $U/Node.o
	$(CC) $(CFLAGS) -I. $U/lex.o $U/Node.o $L/main.cc $L/Parser.cc -o $L/LL1

slr: $U/lex.o $U/Node.o
	$(CC) $(CFLAGS) -I. $U/lex.o $U/Node.o $(LR)/SLRTable.cc $(LR)/main.cc $(LR)/Parser.cc -o $(LR)/SLR

lr1: $U/lex.o $U/Node.o
	$(CC) $(CFLAGS) -I. $U/lex.o $U/Node.o $(LR)/LR1Table.cc $(LR)/main.cc $(LR)/Parser.cc -o $(LR)/LR1

lexyacc: $G/lex.l $G/yacc.y
	lex -o $G/lex.yy.c $G/lex.l ; 	
	yacc -o $G/y.tab.c $G/yacc.y

gcalc: lexyacc
	gcc $(CFLAGS) $G/y.tab.c -lm -o $G/gcalc

$U/lex.o: 
	$(CC) $(CFLAGS) $U/Lexer.cc -c -o $U/lex.o

$U/Node.o:
	$(CC) $(CFLAGS) -I. $U/Node.cc -c -o $U/Node.o

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
	rm -f $D/descent $U/lex.o $U/Node.o     \
		$L/LL1 $(LR)/SLR $(LR)/LR1	\
		$G/gcalc $G/y.tab.c $G/lex.yy.c
