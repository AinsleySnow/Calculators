from LR1_items import *
from SLR_table import CStyleTable


if __name__ == '__main__':
    nts = ParseBNF('grammar.txt').Build()
    augmentedSymbol = '<expr\'>'

    init = LRState()
    init += Item1('<expr\'>', ['<expr>',], 0, 'eof')
    C, transition = GetStates(init, nts, '<expr>', closureLR1)

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
                    actionTable[(name, item.lookahead)] = item # an item to reduce
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
        print(key, ': ', sep=' ', end = '')
        if isinstance(value, Item1):
            print('reduce ' + str(value))
        elif value == 'Accept!':
            print(value)
        else:
            print("shift ", value, sep = ' ')
            
    print('----------------------------------')
    print('GOTO TABLE')
    for key, value in gotoTable.items():
        print(key, ': ', value, sep=' ')

    print()
    
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

    print(CStyleTable('LR1ActionTable', actionTable, indexTable))
    print(CStyleTable('LR1GotoTable', gotoTable))
