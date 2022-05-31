from copy import deepcopy
from bnf import *


class Item0:
    def __init__(self, name, rule: list, pos) -> None:
        self._name = name
        self._rule = rule
        self._pos = pos

    def __str__(self) -> str:
        s = [self._name, ' ::= ']
        for i in range(len(self._rule)):
            if i == self._pos:
                s.append('• ')
            s.extend((self._rule[i], ' '))
        if self._pos == len(self._rule):
            s.append('•')
        return ''.join(s)

    def __eq__(self, __o: object) -> bool:
        return __o._name == self._name and __o._rule == self._rule and __o._pos == self._pos

    def Move(self):
        if self._pos < len(self._rule):
            moved = deepcopy(self)
            moved._pos += 1
            return moved
        return None

    def Where(self):
        if self._pos < len(self._rule):
            return self._rule[self._pos]
        return None

    @property
    def name(self):
        return self._name


class LRState:
    def __init__(self) -> None:
        self.name = 0
        self.__items = []

    def __iter__(self):
        return (item for item in self.__items)

    def __getitem__(self, i):
        return self.__items[i]

    def __setitem__(self, i, value):
        self.__items[i] = value

    def __len__(self):
        return len(self.__items)
    
    def __iadd__(self, value):
        if value not in self.__items:
            self.__items.append(value)
        return self

    def __str__(self) -> str:
        s = [str(self.name), ':\n']
        for item in self.__items:
            s.extend(['\t', str(item), '\n'])
        return ''.join(s)
    
    def __eq__(self, __o: object) -> bool:
        return self.__items == __o.__items


def closure(items: LRState, nts: NonTerminals):
    old = 0

    while len(items) != old:
        old = len(items)
        for item in items:
            name = item.Where()
            if name and name[0] == '<':
                for rule in nts[name]:
                    items += Item0(name, rule, 0)


def goto(items: LRState, symbol: str, nts: NonTerminals):
    gotoset = LRState()
    for item in items:
        name = item.Where()
        if name == symbol:
            gotoset += item.Move()
        
    if len(gotoset) != 0:
        closure(gotoset, nts)
        return gotoset
    return None


def getStates(init: LRState, nts: NonTerminals, startSymbol: str):
    transition = dict()
    statenumber = 1

    closure(init, nts)
    C = [init,]
    symbols = nts.GetName()
    symbols.extend(nts.GetTermName())

    old = 0
    while len(C) != old:
        old = len(C)

        for i in range(old):
            for symbol in symbols:
                newstate = goto(C[i], symbol, nts)
                if newstate and (newstate not in C):
                    newstate.name = statenumber
                    transition[(C[i].name, symbol)] = statenumber
                    statenumber += 1
                    C.append(newstate)
                elif newstate and newstate in C:
                    index = C.index(newstate)
                    transition[(C[i].name, symbol)] = C[index].name

    beforeAccept = transition[(0, startSymbol)]
    transition[(beforeAccept, 'eof')] = 'Accept!'
    return C, transition


if __name__ == '__main__':
    nts = ParseBNF('simplegrammar.txt').Build()
    
    init = LRState()
    init += Item0('<S\'>', ['<S>',], 0)
    c, transition = getStates(init, nts, '<S>')
    
    for state in c:
        print(state)
    for (key, value) in transition.items():
        print(key, ':', value, sep=' ')
