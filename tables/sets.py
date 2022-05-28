from bnf import *
from leftrec import * 


def makechanging():
    length = None
    
    def changing(d: dict) -> bool:
        nonlocal length
        if not length:
            length = dict()
            for k in d.keys():
                length[k] = len(d[k])
            return True

        isChanging = False
        for k in d.keys():
            isChanging |= (length[k] != len(d[k]))
            length[k] = len(d[k])
        return isChanging

    return changing


def FirstSet(nts: NonTerminals, ts: list) -> dict:
    first = dict()
    for (name, rules) in nts:
        first[name] = set()
    for terminal in ts:
        first[terminal] = {terminal}

    changing = makechanging()
    
    while changing(first):
        for (name, rules) in nts:
            for rule in rules:
                if rule != ['""',]:
                    rhs = deepcopy(first[rule[0]])
                    rhs.discard('""') 
                    for i in range(0, len(rule) - 1):
                        if '""' not in first[rule[i]]:
                            break
                        rhs |= first[rule[i + 1]]
                        rhs.discard('""')
                    else:
                        if '""' in first[rule[-1]]:
                            rhs.add('""')
                else:
                    rhs.add('""')

                first[name] |= rhs
                
    return first


def FollowSet(nts: NonTerminals, first: dict, startsymbol: str) -> dict:
    follow = dict()
    for (name, rules) in nts:
        follow[name] = set()
    follow[startsymbol].add('eof')

    changing = makechanging()

    while changing(follow):
        for (name, rules) in nts:
            for rule in rules:
                trailer = deepcopy(follow[name])
                for i in range(len(rule) - 1, -1, -1):
                    if rule[i][0] == '<': # rule[i] is a non-terminal
                        follow[rule[i]] |= trailer
                        
                        if '""' in first[rule[i]]:
                            trailer |= first[rule[i]]
                            trailer.discard('""')
                        else:
                            trailer = deepcopy(first[rule[i]])
                    else:
                        trailer = deepcopy(first[rule[i]])

    return follow 


if __name__ == '__main__':
    nts = ParseBNF('grammar.txt').Build()
    nts = EliminateLeftRecursion(nts)
    ts = ['"+"', '"-"', '"*"', '"/"', '"%"', '"^"', 'num', '"("', '")"', '""', 'eof']
    first = FirstSet(nts, ts)
    follow = FollowSet(nts, first, '<expr>')

    for (name, firstset) in first.items():
        print('%s: ' % name, firstset, sep=' ')
    print()
    for (name, followset) in follow.items():
        print('%s: ' % name, followset, sep=' ')
