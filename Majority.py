def pickFrom(listSample):
    freq = {}
    for item in listSample:
        freq[item] = freq.setdefault(item, 0) + 1

    bigKey, bigVal = freq.popitem()
    for key, val in freq.items():
        if val > bigVal:
            bigKey = key
            bigVal = val

    return listSample.index(bigKey)
