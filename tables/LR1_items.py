from LR0_items import *


class Item1(Item0):
    def __init__(self, name, rule, pos, lookahead) -> None:
        super().__init__(name, rule, pos)
        self.__lookahead = lookahead

    def __str__(self) -> str:
        pass
