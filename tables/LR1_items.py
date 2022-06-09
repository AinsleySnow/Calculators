from LR0_items import *
from sets import FirstSet


class Item1(Item0):
    def __init__(self, name, rule, pos, lookahead) -> None:
        super().__init__(name, rule, pos)
        self.__lookahead = lookahead

    def __str__(self) -> str:
        return ''.join([super().__str__(), ', ', self.__lookahead])
        
    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, Item1):
            return super().__eq__(__o) and self.__lookahead == __o.lookahead
        elif isinstance(__o, Item0):
            return super().__eq__(__o) 
        return False

    @property
    def lookahead(self):
        return self.__lookahead

    def GetThingsRightofDot(self) -> list:
        return self._rule[self._pos + 1:]


def FastFirstSet(rule: list[str], first: dict) -> set:
    firstSet = set()
    
    for ele in rule:
        if ele[0] != '<':
            firstSet.add(ele)
            return firstSet
        else:
            firstSet.update(first[ele])
            if '""' in first[ele]:
                firstSet.discard('""')
            else:
                return firstSet
    
    firstSet.add('eof')
    return firstSet


def closureLR1(items: LRState, nts: NonTerminals):
    old = 0
    first = FirstSet(nts, nts.GetTermName())

    while len(items) != old:
        old = len(items)
        for item in items:
            name = item.Where()
            if name and name[0] == '<':
                for rule in nts[name]:
                    remain = item.GetThingsRightofDot()
                    remain.append(item.lookahead)
                    firstSetOfRemaining = FastFirstSet(remain, first)
                    for terminal in firstSetOfRemaining:
                        items += Item1(name, rule, 0, terminal)


if __name__ == '__main__':
    nts = ParseBNF('grammar.txt').Build()
    
    init = LRState()
    init += Item1('<expr\'>', ['<expr>',], 0, 'eof')
    c, transition = GetStates(init, nts, '<expr>', closureLR1)
    
    for state in c:
        print(state)
    for (key, value) in transition.items():
        print(key, ':', value, sep=' ')
