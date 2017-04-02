import re


class ParserError(TypeError):
    def __init__(self, obj):
        self.obj = obj

    def __str__(self):
        return "Value(" + str(self.obj) + ") of non build-in type: " + \
               str(type(self.obj))


def to_json(obj, raise_unknown=False):
    if obj is None:
        return 'null'
    elif isinstance(obj, (list, tuple)):
        if len(obj) == 0:
            return '[]'
        else:
            s = '[' + to_json(obj[0])
            for i in range(1, len(obj)):
                s += ', ' + to_json(obj[i])
            return s + ']'
    elif isinstance(obj, dict):
        if len(obj) == 0:
            return '{}'
        else:
            items = iter(obj.items())
            temp = next(items)
            s = '{' + to_json(temp[0]) + ': ' + to_json(temp[1])
            for item in items:
                s += ', ' + to_json(item[0]) + ': ' + to_json(item[1])
            return s + '}'
    elif isinstance(obj, bool):
        return str(obj).lower()
    elif isinstance(obj, (int, float)):
        return str(obj)
    elif isinstance(obj, str):
        return '"' + obj.replace('"', r'\"').replace('\n', r'\\n').replace('\t', r'\\t') + '"'
    elif not raise_unknown:
        if hasattr(obj, '__dict__'):
            return to_json(obj.__dict__)
        else:
            raise TypeError('This type {type} can\'t be parsed.'.format(type=str(type(obj))))
    else:
        raise ParserError(obj)


def parse_list(l, i):
    res = []
    while True:
        item, i = parse(l, i)
        res.append(item)
        if l[i] == ',':
            i += 1
        elif l[i] == ']':
            return res, i + 1
        else:
            raise ParserError()

    return res, i


def parse_dict(l, i):
    res = dict()
    while True:
        key, i = parse(l, i)
        if l[i] != ':':
            raise ParserError()
        value, i = parse(l, i + 1)
        res[key] = value
        if l[i] == ',':
            i += 1
        elif l[i] == '}':
            return res, i + 1
        else:
            raise ParserError()
    return res, i


def parse_str(l, i):
    if l[i][-1] != '"':
        raise ParserError()
    return l[i].replace(r'\"', '"').replace(r'\\n', '\n').replace(r'\\t', '\t').replace(r'\\\\', '\\')[1:-1], i + 1


def parse_literal(l, i):
    if l[i] == 'null':
        return None, i + 1
    elif l[i] == 'true':
        return True, i + 1
    elif l[i] == 'false':
        return False, i + 1
    else:
        try:
            return int(l[i]), i + 1
        except ValueError:
            raise ParserError()


def parse(l, i):
    if l[i] == '{':
        return parse_dict(l, i + 1)
    elif l[i] == '[':
        return parse_list(l, i + 1)
    elif l[i][0] == '"':
        return parse_str(l, i)
    else:
        return parse_literal(l, i)


def from_json(s):
    l = re.findall(r'(:|,|[\[\]]|[{}]|[\d]+|true|false|null|"([\w\d\s{}\[\]_|.]*(\\")*(\\\\)*(\\t)*(\\n)*)*")', s)
    l = list(map(lambda x: x[0], l))
    res, i = parse(l, 0)
    if i != len(l):
        raise ParserError()
    return res
