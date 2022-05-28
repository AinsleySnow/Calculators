from copy import deepcopy
from bnf import *


class Item0:
    def __init__(self, name, rule, pos) -> None:
        self._name = name
        self._rule = rule
        self._pos = pos

    def __str__(self) -> str:
        s = [self._name, ': ']
        for i in range(len(self._rule)):
            if i == self._pos:
                s.append('·')
            s.append(self._rule[i])
            s.append(' ')
        return ''.join(s)

    def Move(self):
        if self._pos < len(self._rule):
            self._pos += 1
            return deepcopy(self)
        return None

    def Where(self):
        if self._pos < len(self._rule):
            return self._rule[self._pos]
        return None


class LRState:
    def __init__(self) -> None:
        self.name = 0
        self.__items = []
        self.__goto = dict()

    def __iter__(self):
        return self.__items

    def __getitem__(self, i):
        return self.__items[i]

    def __setitem__(self, i, value):
        self.__items[i] = value

    def __len__(self):
        return len(self.__items)
    
    def __iadd__(self, value):
        self.__items.append(value)
        return self

    def SetTransfer(self, alpha, goto):
        self.__goto[alpha] = goto

    def GetTransfer(self, alpha):
        return self.__goto[alpha]


def closure(items: LRState, nts: NonTerminals):
    old = 0

    while len(items) != old:
        old = len(items)
        for item in items:
            name = item.Where()
            if name[0] == '<':
                for rule in nts[name]:
                    items += Item0(name, rule, 0)


def goto(items: LRState, symbols: set, nts: NonTerminals):
    newname = items.name + 1
    
    for x in symbols:
        gotoset = LRState()
        for item in items:
            name = item.Where()
            if name == x:
                find = True
                gotoset += item.Move()
        
        if find:
            find = False
            gotoset.name = newname
            newname += 1
            closure(gotoset, nts)
            items.SetTransfer(x, gotoset)
            yield gotoset


def getItems0(init: LRState, nts: NonTerminals):
    closure(init, nts)
    c = {init,}
    symbols = nts.GetName()
    symbols.extend(nts.GetTermName())

    old = 0
    while len(c) != old:
        old = len(c)
        for state in c:
            for newstate in goto(state, symbols, nts):
                c.add(newstate)
    
    return c


if __name__ == '__main__':
    pass
