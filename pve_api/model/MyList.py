from typing import Iterable

class MyList(Iterable):
    def __iter__(self):
        return self.list.__iter__()

    def __init__(self, items: list):
        self.list = items

    def __len__(self):
        return len(self.list)

    def __getitem__(self, index):
        return self.list[index]

    def __setitem__(self, index, value):
        self.list[index] = value

    def query(self, key, value):
        for item in self.list:
            if hasattr(item, key):
                if getattr(item, key) == value:
                    return item
        return None

    def query_all(self, key, value):
        result = []
        for item in self.list:
            if hasattr(item, key):
                if hasattr(item, key):
                    if getattr(item, key) == value:
                        result.append(item)
        return MyList(result)