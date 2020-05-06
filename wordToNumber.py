d = {'zero': 0, 'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5, 'six': 6, 'seven': 7, 'eight': 8, 'nine': 9,
     'ten': 10, 'eleven': 11, 'twelve': 12, 'thirteen': 13, 'fourteen': 14, 'fifteen': 15, 'sixteen': 16,
     'seventeen': 17, 'eighteen': 18, 'nineteen': 19, 'twenty': 20, 'thirty': 30, 'forty': 40, 'fifty': 50}


def wordToNumber(wordNumberString):
    '''
    Converts number in words to number
    :param wordNumberString: Number in Words
    :return: Number in words to number
    '''
    # convert to lowercase and split
    wordNumberString = wordNumberString.lower()
    wordNumberString = wordNumberString.split()

    # remove 'only'
    if wordNumberString[-1] == 'only':
        wordNumberString.pop(-1)

    length = len(wordNumberString)
    ans = 0
    i = 0
    if ('crore' in wordNumberString):
        temp = []
        while (i < length and wordNumberString[i] != r'crore'):
            temp.append(wordNumberString[i])
            i += 1
        i += 1
        ans += convert(temp, 10000000)
    if ('lakh' in wordNumberString):
        temp = []
        while (i < length and wordNumberString[i] != r'lakh'):
            temp.append(wordNumberString[i])
            i += 1
        i += 1
        ans += convert(temp, 100000)
    if ('thousand' in wordNumberString):
        temp = []
        while (i < length and wordNumberString[i] != r'thousand'):
            temp.append(wordNumberString[i])
            i += 1
        i += 1
        ans += convert(temp, 1000)
    if ('hundred' in wordNumberString):
        temp = []
        while (i < length and wordNumberString[i] != r'hundred'):
            if (wordNumberString[i] != 'and'):
                temp.append(wordNumberString[i])
            i += 1
        i += 1
        ans += convert(temp, 100)
    temp = []
    while (i < length):
        if (wordNumberString[i] != 'and'):
            temp.append(wordNumberString[i])
        i += 1
    if len(temp) != 0:
        ans += convert(temp, 1)
    return ans


def convert(listString, num):
    '''
    Coverts number in words and multiplies it with num
    :param listString: Number in words
    :param num: integer to be multiplied with
    :return: converted number
    '''
    if len(listString) == 1:
        if listString[0] in d:
            return d[listString[0]] * num
        else:
            temp = listString[0][:-2]
            if temp in d:
                if d[temp] < 10:
                    return d[temp] * 10 * num
                else:
                    return d[temp] * num
    else:
        temp = 0
        if listString[0] in d:
            temp += d[listString[0]]
        else:
            temp2 = listString[0][:-2]
            if temp2 in d:
                if d[temp2] < 10:
                    temp += d[temp2] * 10
                else:
                    temp += d[temp2]
        temp += d[listString[1]]
        return temp * num
