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

def subTopItemsIndictionary(dic ,length):
    wordMap = dic
    items = sorted(wordMap.items(), key = lambda wordMap:wordMap[1])
    i = 0
    ret = {}
    for item in reversed(items):
        if i >= length:
            break
        i = i + 1
        ret[item[0]] = item[1]
    
    return ret


def topItemsInDictionary(dic ,length):
    wordMap = dic
    items = sorted(wordMap.items(), key = lambda wordMap:wordMap[1])
    i = 0
    topKeys = []
    for item in reversed(items):
        if i >= length:
            break
        i = i + 1
        topKeys.append(item[0])
    return topKeys

