from itertools import groupby
from LR0_items import *
from bnf import *
from sets import *


def CStyleTable(tableName: str, table: dict, indexTable: list = None) -> str:
    howToMap = [terminal for terminal, _ in groupby(sorted(table.keys(), key=lambda x: x[1]), lambda x: x[1])]
    maxState = max((state for state, _ in table.keys())) + 1

    output = [[-1 for i in range(len(howToMap))] for j in range(maxState)]
    if indexTable:
        for (key, value) in table.items():
            if isinstance(value, int):
                output[key[0]][howToMap.index(key[1])] = value
            elif value == 'Accept!':
                output[key[0]][howToMap.index(key[1])] = 0
            else:
                output[key[0]][howToMap.index(key[1])] = indexTable.index(value) | (1 << 8)
    else:
        for (key, value) in table.items():
            output[key[0]][howToMap.index(key[1])] = value

    for i in range(len(output)):
        output[i] = ''.join('%s, ' % (s) for s in output[i])
        output[i] = '\t{ %s},\n' % output[i]
    output = ''.join(output)

    output = '// {}\nint {}[{}][{}] = {{\n{}}};'.format(
        'how do terminals map to indices: %s' % ''.join(('%s -> %d; ' % (howToMap[i], i) for i in range(len(howToMap)))),\
        tableName, maxState, len(howToMap), output
    )
    return output


if __name__ == '__main__':
    nts = ParseBNF('grammar.txt').Build()
    augmentedSymbol = '<expr\'>'

    init = LRState()
    init += Item0(augmentedSymbol, ['<expr>',], 0)
    C, transition = GetStates(init, nts, '<expr>', closureLR0)

    actionTable = dict()
    gotoTable = dict()

    '''
    indexTable = [
        Item0('<expr>', ['<expr>', '"+"', '<term>'], 3),
        Item0('<expr>', ['<expr>', '"-"', '<term>'], 3),
        Item0('<expr>', ['<term>',], 1),

        Item0('<term>', ['<term>', '"*"', '<factor>'], 3),
	    Item0('<term>', ['<term>', '"/"', '<factor>'], 3),
        Item0('<term>', ['<term>', '"%"', '<factor>'], 3),
        Item0('<term>', ['<factor>',], 1),

        Item0('<factor>', ['<factor>', '"^"', '<exponent>'], 3),
	    Item0('<factor>', ['<exponent>',], 1),

        Item0('<exponent>', ['"("', '<expr>', '")"'], 3),
	    Item0('<exponent>', ['num',], 1)        
    ]
    '''

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
                        actionTable[(name, symbol)] = item # reduce item
                elif next2Dot and next2Dot[0] != '<':
                    to = transition[(name, next2Dot)]
                    actionTable[(name, next2Dot)] = to # shift to some state
    
    for state in C:
        for symbolName in nts.GetName():
            key = (state.name, symbolName)
            if key in transition.keys():
                gotoTable[key] = transition[key]

    print('ACTION TABLE:')
    for key, value in actionTable.items():
        print(key, ': ', sep = ' ', end = '')
        if isinstance(value, Item0):
            print("reduce " + str(value))
        elif value == 'Accept!':
            print(value)
        else:
            print("shift ", value, sep = ' ')

    print('----------------------------------')
    print('GOTO TABLE')
    for key, value in gotoTable.items():
        print(key, ': ', value, sep=' ')

    # print(CStyleTable('SLRActionTable', actionTable, indexTable))
    # print(CStyleTable('SLRGotoTable', gotoTable))
