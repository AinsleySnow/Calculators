#ifndef _GRAMMAR_H_
#define _GRAMMAR_H_

constexpr int _expr = 0, _expr_p = 1, _term = 2, _term_p = 3, 
   _factor = 4,  _factor_p = 5, _exponent = 6, _epsilon = 7;

constexpr int _plus = 8, _minus = 24, _times = 40, 
    _divide = 56, _mod = 72, _power = 88, _leftpar = 104, 
    _rightpar = 120, _num = 136, _eof = 152;

static int parseTable[7][10] = {
    { -1, -1, -1, -1, -1, -1,  0, -1,  0, -1 },
    {  1,  2, -1, -1, -1, -1, -1,  3, -1,  3 },
    { -1, -1, -1, -1, -1, -1,  4, -1,  4, -1 },
    {  8,  8,  5,  6,  7, -1, -1,  8, -1,  8 },
    { -1, -1, -1, -1, -1, -1,  9, -1,  9, -1 },
    { 11, 11, 11, 11, 11, 10, -1, 11, -1, 11 },
    { -1, -1, -1, -1, -1, -1, 12, -1, 13, -1 }
};

static int grammars[14][5] = {
    { 3, _expr, _term, _expr_p, 0 },
    { 4, _expr_p, _plus, _term, _expr_p },
    { 4, _expr_p, _minus, _term, _expr_p },
    { 2, _expr_p, _epsilon, 0, 0 },
    { 3, _term, _factor, _term_p, 0 },
    { 4, _term_p, _times, _factor, _term_p },
    { 4, _term_p, _divide, _factor, _term_p },
    { 4, _term_p, _mod, _factor, _term_p },
    { 2, _term_p, _epsilon, 0, 0 },
    { 3, _factor, _exponent, _factor_p, 0 },
    { 4, _factor_p, _power, _exponent, _factor_p },
    { 2, _factor_p, _epsilon, 0, 0 },
    { 4, _exponent, _leftpar, _expr, _rightpar },
    { 2, _exponent, _num, 0, 0 }
};

#endif // _GRAMMAR_H_
