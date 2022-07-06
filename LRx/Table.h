#ifndef _TABLE_H_
#define _TABLE_H_

extern int _expr, _term, _factor, _exponent;

extern int _plus, _minus, _times, _divide, _mod, 
        _power, _leftpar, _rightpar, _eof, _num;

extern int actionTable[][10];
extern int gotoTable[][4];

#endif // _TABLE_H_
