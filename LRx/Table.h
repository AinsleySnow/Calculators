#ifndef _TABLE_H_
#define _TABLE_H_

extern int _expr, _term, _factor, _exponent;

extern int _plus, _minus, _times, _divide, _mod, 
        _power, _leftpar, _rightpar, _eof, _num;

#ifdef SLR
extern int SLRActionTable[21][10];
extern int SLRGotoTable[13][4];
#elif LR1
extern int LR1ActionTable[40][10];
extern int LR1GotoTable[32][4];
#endif // SLR

#endif // _TABLE_H_
