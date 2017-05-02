class RecDict(dict):
    def __getitem__(self, key):
        if key in self:
            return dict.__getitem__(self, key)
        else:
            self[key] = RecDict()
            return self[key]

    def find_item(self, key, info=None):
        if info is None:
            info = []
        if key in self:
            info.append(key)
            return self[key], info
        for k, v in self.items():
            if isinstance(v, dict):
                info.append(k)
                item, info = v.find_item(key, info)
                if item is not None:
                    return item, info
