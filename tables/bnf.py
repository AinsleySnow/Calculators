from copy import deepcopy
import re

class Rule:
    def __init__(self, i, c) -> None:
        self.__index = i
        self.__content = c
    
    @property
    def Index(self):
        return self.__index
    
    def __str__(self) -> str:
        return str(self.__content)

    def __len__(self) -> int:
        return len(self.__content)
    
    def __getitem__(self, i: int):
        return self.__content[i]

    def __iter__(self):
        return (ele for ele in self.__content)

    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, list):
            return self.__content == __o
        elif not isinstance(__o, Rule):
            return False
        return self.Index == __o.Index

    def append(self, ele):
        self.__content.append(ele)

    def pop(self, i):
        self.__content.pop(i)


class Rules:
    def __init__(self) -> None:
        self.__content = []

    def __str__(self) -> str:
        strrule = []
        for rule in self.__content:
            strrule.append(''.join([('%s ' % s) for s in rule]))
        return ''.join([('  %s\n') % s for s in strrule])

    def __iter__(self):
        return (ele for ele in self.__content)

    def __len__(self) -> int:
        return len(self.__content)

    def __getitem__(self, i: int) -> list:
        return self.__content[i]

    def __delitem__(self, i: int) -> None:
        self.__content.pop(i)

    def __set__(self):
        return set(self.__content)

    def __iadd__(self, ele: list[str]):
        self.__content.append(ele)
        return self

    def Append(self, ele: list):
        self.__content.append(ele)

    @classmethod
    def FromList(cls, lst):
        r = Rules()
        r.__content = deepcopy(lst)
        return r


class NonTerminals:
    def __init__(self) -> None:
        self.__nts = dict()

    def __len__(self) -> int:
        return len(self.__nts)

    def __iter__(self):
        return iter(self.__nts.items())

    def __getitem__(self, s: str) -> Rules:
        return self.__nts[s]

    def __setitem__(self, i: str, value):
        self.__nts[i] = value

    def __str__(self):
        nts = []
        for (name, rules) in self.__nts.items():
            nts.append('%s:\n%s\n' % (str(name), str(rules)))
        return ''.join(nts)

    def GetName(self) -> list:
        return list(self.__nts.keys())

    def GetTermName(self) -> list:
        terminals = set()
        for rules in self.__nts.values():
            for rule in rules:
                for ele in rule:
                    if ele[0] != '<':
                        terminals.add(ele)
        return list(terminals)


class ParseBNF:
    def __init__(self, name: str) -> None:
        self.file = open(name, 'r')
        self.line = re.findall('\\S+', self.file.readline())
        self.__index = 0

    def __del__(self) -> None:
        self.file.close()

    def __nextLine(self) -> bool:
        line = self.file.readline()
        if not line:
            self.line = None
            return False
        self.line = re.findall('\\S+', line)
        return True
        
    def __nextRule(self):
        start = 0
        try:
            start = self.line.index('::=')
        except:
            start = self.line.index('|')
        
        rule = Rule(self.__index, self.line[start + 1:])
        self.__index += 1
        return rule

    def __nextNonTerminal(self):
        if not self.line or self.line[0][0] != '<':
            while self.__nextLine():
                if self.line[0][0] == '<':
                    break
            else:
                return None

        name = str(self.line[0])
        r = Rules()
        r += self.__nextRule()

        while True:
            self.__nextLine()
            if (not self.line) or self.line[0][0] == '<' or self.line[0][0] == '\n':
                break
            r += self.__nextRule()
        
        return (name, r)

    def Build(self) -> NonTerminals:
        nts = NonTerminals()
        while True:
            pack = self.__nextNonTerminal()
            if not pack:
                break
            nts[pack[0]] = pack[1]

        return nts


if __name__ == '__main__':
    grammar = ParseBNF('grammar.txt')
    print(str(grammar.Build()))
