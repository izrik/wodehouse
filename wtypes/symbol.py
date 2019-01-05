from functions.str import w_str
from wtypes.object import WObject
from wtypes.string import WString


class WSymbol(WObject):
    def __init__(self, name, position=None):
        super().__init__(position=position)
        if isinstance(name, str):
            name = WString(name)
        if not isinstance(name, WString):
            name = w_str(name)
        self.name = name

    def __repr__(self):
        return 'Symbol({})'.format(self.name.value)

    def __str__(self):
        return self.name.value

    def __eq__(self, other):
        if not isinstance(other, WSymbol):
            return False
        return self.name == other.name

    def __hash__(self):
        return hash((WSymbol, self.name))

    __symbol_cache__ = {}

    @staticmethod
    def get(name):
        if isinstance(name, str):
            name = WString(name)
        if name not in WSymbol.__symbol_cache__:
            WSymbol.__symbol_cache__[name] = WSymbol(name)
        return WSymbol.__symbol_cache__[name]


class WSymbolAt(WSymbol):
    def __init__(self, name, position=None):
        if isinstance(name, WSymbol):
            name = name.name
        super().__init__(name, position=position)
        self.src = WSymbol.get(name)

    def __repr__(self):
        return repr(self.src)

    def __str__(self):
        return str(self.src)

    def __eq__(self, other):
        return self.src == other

    def __hash__(self):
        return hash(self.src)

