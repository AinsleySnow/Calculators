from bnf import *
from leftrec import *
from sets import *


if __name__ == '__main__':
    nts = ParseBNF('grammar.txt').Build()
    nts = EliminateLeftRecursion(nts)

    terminalName = nts.GetTermName()
    terminalName.append('eof')
    first = FirstSet(nts, terminalName)
    follow = FollowSet(nts, first, '<expr>')

    for (name, rules) in nts:
        for rule in rules:
            for t in terminalName:
                if t in first[rule[0]]:
                    print('[%s][%s]: %s -> %s' % (name, t, name, rule))
            if '""' in first[rule[0]]:
                for t in follow[name]:
                    print('[%s][%s]: %s -> %s' % (name, t, name, rule))
