singleDict = {
    'A':'4', 'B':'8', 'C':'C', 'D':'0', 'E':'6', 'F':'F', 'G':'6', 'H':'H', 'I':'1',
    'J':'J', 'K':'K', 'L':'L', 'M':'M', 'N':'N', 'O':'0', 'P':'P', 'Q':'0', 'R':'R',
    'S':'5', 'T':'7', 'U':'0', 'V':'V', 'W':'W', 'X':'X', 'Y':'Y','Z':'2', '1':'I',
    '2':'Z', '3':'3','4':'A', '5':'S', '6':'B', '7':'T', '8':'B', '9':'9', '0':'O'
}
doubleDict = {'OS':'05','HH':'MH','HB':'WB','TP':'AP','IP':'AP','KQ':'KA'}

def correct(plateText):
    global singleDict, doubleDict

    plateText = plateText.upper()
    l = len(plateText)
    last = plateText[-1]
    first2 = plateText[0:2]
    second2 = plateText[2:4]

    if last.isalpha():
        plateText = plateText[:l-1] + singleDict[last]

    if first2 in doubleDict.keys():
        plateText = doubleDict[first2] + plateText[2:l]
    elif first2[0].isalpha() and first2[1].isdigit():
        plateText = plateText[0] + singleDict[plateText[1]] + plateText[2:l]
    elif first2[0].isdigit() and first2[1].isalpha():
        plateText = singleDict[plateText[0]] + plateText[1:l]

    if second2 in doubleDict.keys():
        plateText = plateText[0:2] + doubleDict[second2] + plateText[4:l]
    elif second2[0].isalpha() and second2[1].isdigit():
        plateText = plateText[0:2] + singleDict[plateText[2]] + plateText[3:l]
    elif second2[0].isdigit() and second2[1].isalpha():
        plateText = plateText[0:3] + singleDict[plateText[3]] + plateText[4:l]

    if l == 10:
        mid2 = plateText[4:6]
        nums = plateText[6:9]

        if mid2[0].isalpha() and mid2[1].isdigit():
            plateText = plateText[0:5] + singleDict[plateText[5]] + plateText[6:l]
        elif mid2[0].isdigit() and mid2[1].isalpha():
            plateText = plateText[0:4] + singleDict[plateText[4]] + plateText[5:l]

        if nums[0].isalpha():
            plateText = plateText[0:6] + singleDict[plateText[6]] + plateText[7:l]
        if nums[1].isalpha():
            plateText = plateText[0:7] + singleDict[plateText[7]] + plateText[8:l]
        if nums[2].isalpha():
            plateText = plateText[0:8] + singleDict[plateText[8]] + plateText[9:l]

    return plateText