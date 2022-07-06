%{
    #include <stdio.h>
    extern double yylval;
%}

digit [0-9]
number ({digit}+)([\.]{digit}+)?
white [ \t\r]
%%
"\n"        { return EOL; }
"exit"      { return EXIT; }
"+"         { return PLUS; }
"-"         { return MINUS; }
"*"         { return TIMES; }
"/"         { return DIVIDE; }
"%"         { return MOD; }
"^"         { return POWER; }
"("         { return LEFT; }
")"         { return RIGHT; }
{number}    { yylval = atof(yytext); return NUM; }
{white}+    {}
%%
int yywrap(void) { return 1; }
