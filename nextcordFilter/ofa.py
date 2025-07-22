import difflib

# Target words to filter
filteredWords = ["niger", "tranny", "boykisser", "ngr"]

# Character substitution dictionary
substitutes = {
    # a
    '4': 'a', '@': 'a', 'à': 'a', 'á': 'a', 'â': 'a', 'ã': 'a', 'ä': 'a', 'å': 'a',
    'ɑ': 'a', 'а': 'a',  # Cyrillic 'a'

    # b
    'ß': 'b', '฿': 'b', 'в': 'b',  # Cyrillic 'v' looks like b

    # c
    'ç': 'c', '¢': 'c', 'с': 'c',  # Cyrillic 's'

    # d
    'ԁ': 'd', 'đ': 'd', 'ԃ': 'd',

    # e
    '3': 'e', '€': 'e', 'è': 'e', 'é': 'e', 'ê': 'e', 'ë': 'e', 'е': 'e',  # Cyrillic 'e'

    # f
    'ƒ': 'f',

    # g
    '6': 'g', '9': 'g', 'ɢ': 'g', 'ġ': 'g', '8': 'g',

    # h
    'н': 'h',  # Cyrillic 'n'

    # i
    '1': 'i', '!':'i', 'í': 'i', 'ì': 'i', 'î': 'i', 'ï': 'i', 'İ': 'i', 'і': 'i', '(':'i', ')':'i', '[':'i', ']':'i', # Cyrillic 'i'

    # j
    'ј': 'j', 'ʝ': 'j',  # Cyrillic 'j'

    # k
    'κ': 'k', 'k': 'k',

    # l
    '1': 'l', '|': 'l', 'ł': 'l',

    # m
    'м': 'm',  # Cyrillic

    # n
    'ñ': 'n', 'η': 'n', 'п': 'n', 'и': 'n', 'и': 'n', 'и': 'n', 'ń': 'n', '/' : 'n', '\\':'n', '|':'n',

    # o
    '0': 'o', 'ò': 'o', 'ó': 'o', 'ô': 'o', 'ö': 'o', 'õ': 'o', 'ø': 'o', 'ο': 'o', 'о': 'o',  # Greek, Cyrillic 'o'

    # p
    'ρ': 'p', 'р': 'p',  # Greek, Cyrillic

    # q
    'գ': 'q',

    # r
    '®': 'r', 'г': 'r', 'ř': 'r',

    # s
    '5': 's', '$': 's', 'ś': 's', 'ѕ': 's', 'š': 's',  # Cyrillic 's'

    # t
    '7': 't', '+': 't', 'ţ': 't', 'т': 't',

    # u
    'µ': 'u', 'υ': 'u', 'ù': 'u', 'ú': 'u', 'û': 'u', 'ü': 'u',

    # v
    'ν': 'v', 'v': 'v',

    # w
    'ω': 'w', 'ш': 'w',

    # x
    '%': 'x', '×': 'x', 'х': 'x',

    # y
    '¥': 'y', 'у': 'y', 'ý': 'y', 'ÿ': 'y',

    # z
    '2': 'z', 'ž': 'z', 'ź': 'z', 'ż': 'z', 'з': 'z',  # Cyrillic 'z'

    # common noise or neutral characters (optional to strip or ignore)
    '*': '', '#': '', '^': '', '~': '', '`': '', '"': '', "'": '', ' ': ''
}


def findSub(char):
    return substitutes.get(char, char)

def similarWord(message):
    bestMatch = ""
    simPercent = 0

    for word in filteredWords:
        percent = difflib.SequenceMatcher(None, message, word).ratio()
        if percent > simPercent:
            simPercent = percent
            bestMatch = word

    print(f"Best match: {bestMatch}, Similarity: {simPercent:.2f}")
    return simPercent

def remove_duplicates(s):
    seen = set()
    result = ''
    for char in s:
        if char not in seen:
            seen.add(char)
            result += char
    return result

def filter(message):
    message = message.lower()

    clean = ""
    prev = ""
    for c in message:
        clean += findSub(c)
    clean = remove_duplicates(clean)
    print("Cleaned message:", clean)

    highest = 0
    for word in filteredWords:
        word_len = len(word)
        if len(clean) >= word_len:
            for i in range(len(clean) - word_len + 1):
                chunk = clean[i:i + word_len]
                score = difflib.SequenceMatcher(None, chunk, word).ratio()
                if score > highest:
                    highest = score
                    print(f"Chunk '{chunk}' matched '{word}' with score {score:.2f}")
        else:
            chunk = clean
            score = difflib.SequenceMatcher(None, chunk, word).ratio()
            print(f"Chunk '{chunk}' matched '{word}' with score {score:.2f}")
            if score > highest:
                highest = score

    return highest

