from functions.str import w_str
from wtypes.object import WObject
from wtypes.string import WString
from wtypes.symbol import WSymbolAt, WSymbol


class WScope(WObject):
    def __init__(self, values=None, enclosing_scope=None):
        if values is None:
            values = {}
        self.enclosing_scope = enclosing_scope
        self.dict = {self.normalize_key(key): value
                     for key, value in values.items()}
        self.deleted = set()

    @staticmethod
    def normalize_key(key):
        if isinstance(key, WSymbolAt):
            return key.src
        if isinstance(key, WSymbol):
            return key
        if isinstance(key, str):
            return WSymbol.get(WString(key))
        return WSymbol.get(w_str(key))

    def __getitem__(self, item):
        key = self.normalize_key(item)
        if key in self.deleted:
            raise KeyError
        if key in self.dict:
            return self.dict.get(key)
        if self.enclosing_scope is not None:
            return self.enclosing_scope[key]
        raise KeyError(key.name)

    def __setitem__(self, key, value):
        key2 = self.normalize_key(key)
        self.dict[key2] = value
        self.deleted.discard(key2)

    def __contains__(self, item):
        key = self.normalize_key(item)
        if key in self.deleted:
            return False
        if key in self.dict:
            return True
        if self.enclosing_scope is not None:
            return key in self.enclosing_scope
        return False

    def __delitem__(self, key):
        key2 = self.normalize_key(key)
        self.deleted.add(key2)

    def __len__(self):
        return len(list(self.keys()))

    def keys(self):
        keys = set(self.dict.keys())
        if self.enclosing_scope is not None:
            keys.update(self.enclosing_scope.keys())
        keys.difference_update(self.deleted)
        for key in sorted(keys, key=lambda s: str(s)):
            yield key

    def update(self, values):
        for key, value in values.items():
            self[key] = value

    def get_outermost(self):
        s = self
        while s.enclosing_scope is not None:
            s = s.enclosing_scope
        return s
