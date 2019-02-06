from wtypes.object import WObject
from wtypes.string import WString
from wtypes.symbol import WSymbolAt, WSymbol


class WScope(WObject):
    def __init__(self, values=None, enclosing_scope=None,
                 builtins_module=None):
        super().__init__()
        if values is None:
            values = {}
        self.enclosing_scope = enclosing_scope
        self.dict = {self.normalize_key(key): value
                     for key, value in values.items()}
        self.deleted = set()
        self.builtins_module = builtins_module

    @staticmethod
    def normalize_key(key):
        from functions.str import w_str
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

    def __str__(self):
        return f'WScope({len(self)} keys)'

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

    def get_builtins_module(self):
        if self.builtins_module is not None:
            return self.builtins_module
        if self.enclosing_scope is None:
            return None
        return self.enclosing_scope.get_builtins_module()
