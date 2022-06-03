from LR1_items import *


if __name__ == '__main__':
    nts = ParseBNF('simplegrammar.txt').Build()
    augmentedSymbol = '<S\'>'

    init = LRState()
    init += Item1('<S\'>', ['<S>',], 0, 'eof')
    C, transition = GetStates(init, nts, '<S>', closureLR1)

    actionTable = dict()
    gotoTable = dict()

    for state in C:
        name = state.name
        for item in state:
            if item.name == augmentedSymbol and (not item.Where()):
                actionTable[(name, 'eof')] = 'Accept!'
            else:
                next2Dot = item.Where()
                if not next2Dot:
                    actionTable[(name, item.lookahead)] = "reduce " + str(item)
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
