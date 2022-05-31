from LR0_items import *
from bnf import *
from sets import *


if __name__ == '__main__':
    nts = ParseBNF('simplegrammar.txt').Build()
    augmentedSymbol = '<S\'>'

    init = LRState()
    init += Item0(augmentedSymbol, ['<S>',], 0)
    C, transition = getStates(init, nts, '<S>')

    actionTable = dict()
    gotoTable = dict()

    first = FirstSet(nts, nts.GetTermName())
    follow = FollowSet(nts, first, None)

    for state in C:
        name = state.name
        for item in state:
            if item.name == augmentedSymbol and (not item.Where()):
                actionTable[(name, 'eof')] = 'Accept!'
            else:
                next2Dot = item.Where()
                if not next2Dot:
                    for symbol in follow[item.name]:
                        actionTable[(name, symbol)] = "reduce " + str(item)
                elif next2Dot and next2Dot[0] != '<':
                    to = transition[(name, next2Dot)]
                    actionTable[(name, next2Dot)] = "shift " + str(to)
    
    for state in C:
        for symbolName in nts.GetName():
            key = (state.name, symbolName)
            if key in transition.keys():
                gotoTable[key] = transition[key]

    print('ACTION TABLE:')
    for key, value in actionTable.items():
        print(key, ': ', value, sep=' ')
    print('----------------------------------')
    print('GOTO TABLE')
    for key, value in gotoTable.items():
        print(key, ': ', value, sep=' ')
