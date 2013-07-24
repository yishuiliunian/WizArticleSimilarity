def getValueFromNotNilKey(key, dic):
    if dic.has_key(key):
        return dic[key]
    else:
        return None

def getIntValueFromNotNilKey(key, dic):
    value = getValueFromNotNilKey(key, dic)
    if value != None:
        return int(value)
    return 0


