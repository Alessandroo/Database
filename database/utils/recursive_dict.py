class RecDict(dict):
    def __getitem__(self, key):
        if key in self:
            return dict.__getitem__(self, key)
        else:
            self[key] = RecDict()
            return self[key]

    # TODO check function
    def find_item(self, key, info=None):
        print("kedul")
        if info is None:
            info = []
        if key in self:
            info.append(key)
            return self[key], info
        print("self")
        print(self)
        if isinstance(self, RecDict):
            for k, v in self.items():
                if isinstance(v, RecDict):
                    alt = info[:]
                    alt.append(k)
                    print("alt")
                    print(alt)
                    item = v.find_item(key, alt)
                    # item, info = v.find_item(key, info)
                    print("lkl;k")
                    if item is not None:
                        return item[0], item[1]
                # elif k == key:
                #     print(k == key)
                #     info.append(key)
                #     return self[key], info
                else:
                    print("iiiii")
                    print(v)
                    return None
