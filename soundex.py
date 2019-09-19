def Soundex(data):
    result = ""
    if (data):
        previousCode = ""
        currentCode = ""
        result = result + data[0].upper()

        for i in range(1, len(data)):
            currentCode = EncodeChar(data[i])
            if (currentCode != previousCode):
                result = result + currentCode

            if (len(result) == 4):
                break

            if (currentCode != ""):
                previousCode = currentCode
    if (len(result) < 4):
        result = result + ('0' * (4 - len(result)))
    return result

def EncodeChar(c):
    c = c.lower()
    if (c in ['b','f','p','v']):
        return "1"
    if (c in ['c','g','j','k','q','s','x','z']):
        return "2"
    if (c in ['d','t']):
        return "3"
    if (c in ['l']):
        return "4"
    if (c in ['m','n']):
        return "5"
    if (c in ['r']):
        return "6"
    return ""

def Difference(data1, data2):
    result = 0
    if (data1 == "" or data2 == ""):
        return 0
    soundex1 = Soundex(data1)
    soundex2 = Soundex(data2)
    if (soundex1 == soundex2):
        result = 4
    else:
        if (soundex1[0] == soundex2[0]):
            result = 1
        sub1 = soundex1[1:3]
        if (Index(soundex2, sub1) > -1):
            result += 3
            return result
        sub2 = soundex1[2:2]
        if(Index(soundex2, sub2) > -1):
            result += 2
            return result
        sub3 = soundex1[1:2]
        if (Index(soundex2, sub3) > -1):
            result += 2
            return result
        sub4 = soundex1[1]
        if (Index(soundex2, sub4) > -1):
            result += 1
        sub5 = soundex1[2]
        if (Index(soundex2, sub5) > -1):
            result += 1
        sub6 = soundex1[3]
        if (Index(soundex2, sub6) > -1):
            result += 1
    
    if (result == 1):
        return 0
    if (result == 2):
        return 0.333333
    if (result == 3):
        return 0.666667
    if (result == 4):
        return 1

def Index(string, sub):
    try:
        return string.index(sub)
    except ValueError as e:
        return -1
