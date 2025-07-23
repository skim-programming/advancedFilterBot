import re
from rapidfuzz import fuzz

messageThreshold = 75.0

filteredWords = ["niger", "tranny", "boykisser", "ngr", "nigers", "ngrs", "nigr", "nigrs"]
allowedWords = [""]

substitutes = {
    # ... [your existing substitutions here, unchanged] ...
    '4': 'a', '@': 'a', 'à': 'a', 'á': 'a', 'â': 'a', 'ã': 'a', 'ä': 'a', 'å': 'a',
    'ɑ': 'a', 'а': 'a',
    'ß': 'b', '฿': 'b', 'в': 'b',
    'ç': 'c', '¢': 'c', 'с': 'c',
    'ԁ': 'd', 'đ': 'd', 'ԃ': 'd',
    '3': 'e', '€': 'e', 'è': 'e', 'é': 'e', 'ê': 'e', 'ë': 'e', 'е': 'e',
    'ƒ': 'f',
    '6': 'g', '9': 'g', 'ɢ': 'g', 'ġ': 'g', '8': 'g',
    'н': 'h',
    '1': 'i', '!':'i', 'í': 'i', 'ì': 'i', 'î': 'i', 'ï': 'i', 'İ': 'i', 'і': 'i',
    '(':'i', ')':'i', '[':'i', ']':'i', '7':'i',
    'ј': 'j', 'ʝ': 'j',
    'κ': 'k', 'k': 'k',
    '|': 'l', 'ł': 'l',
    'м': 'm',
    'ñ': 'n', 'η': 'n', 'п': 'n', 'и': 'n', 'ń': 'n', '/' : 'n', '\\':'n',
    '0': 'o', 'ò': 'o', 'ó': 'o', 'ô': 'o', 'ö': 'o', 'õ': 'o', 'ø': 'o', 'ο': 'o', 'о': 'o',
    'ρ': 'p', 'р': 'p',
    'գ': 'q',
    '®': 'r', 'г': 'r', 'ř': 'r',
    '5': 's', '$': 's', 'ś': 's', 'ѕ': 's', 'š': 's',
    '+': 't', 'ţ': 't', 'т': 't',
    'µ': 'u', 'υ': 'u', 'ù': 'u', 'ú': 'u', 'û': 'u', 'ü': 'u',
    'ν': 'v', 'v': 'v',
    'ω': 'w', 'ш': 'w',
    '%': 'x', '×': 'x', 'х': 'x',
    '¥': 'y', 'у': 'y', 'ý': 'y', 'ÿ': 'y',
    '2': 'z', 'ž': 'z', 'ź': 'z', 'ż': 'z', 'з': 'z',
    '*': '', '#': '', '^': '', '~': '', '`': '', '"': '', "'": '', ' ': ''
}

def findSub(char):
    return substitutes.get(char, char)

def strip_repeating_noise(s):
    return re.sub(r'((..)\2{1,})', r'\2', s)

def reduce_consecutive_duplicates(s):
    return re.sub(r'(.)\1{2,}', r'\1', s)  # e.g., niiiiigggg -> nig

def filter(message):
    message = message.lower()

    # Step 1: Replace lookalikes
    cleaned = ''.join(findSub(c) for c in message)

    # Step 2: Reduce floods and junk
    cleaned = reduce_consecutive_duplicates(cleaned)
    cleaned = strip_repeating_noise(cleaned)

    # Step 3: If the cleaned string exactly matches allowed word, let it through
    if cleaned in allowedWords:
        return 0.0

    # Step 4: Sliding window fuzzy check
    highest = 0
    for word in filteredWords:
        wlen = len(word)
        for i in range(len(cleaned) - wlen + 1):
            chunk = cleaned[i:i + wlen]
            score = fuzz.ratio(chunk, word)
            if score > highest:
                highest = score

    return highest


# Test
tests = [
    "nigga",         # should pass
    "nigger",        # should be blocked
    "n1gger",        # blocked
    "niiiiigggggger",# blocked
    "nigegegeger",   # blocked
    "dirtyniggas",   # blocked
    "clean message"  # pass
]

for t in tests:
    print(f"{t:<20}: {filter(t):.2f}")
