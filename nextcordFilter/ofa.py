import re  # alternative for re with more unicode features
from rapidfuzz import fuzz
import json

def is_valid_pattern(pattern):
    # Reject patterns that are only underscores (or only wildcards)
    if pattern and all(c == '_' for c in pattern):
        return False
    return True

def blregex(blacklist, text):
    text = text.lower()
    for pattern in blacklist:
        if("_" in pattern):
            pattern_lower = pattern.lower()
            regex_pattern = pattern_lower.replace("_", ".")
            plen = len(pattern_lower)

            # Check if regex pattern exists anywhere in the text:
            if re.search(regex_pattern, text):
                # Exact match found, block immediately
                #print("pattern found")
                return 100, pattern_lower, plen  # max score to block
    # no match found for any pattern
    return 0, "", 0 

def qFilter(text):
    text = text.lower()
    highest = 0
    highestchunk = ""

    # Step 1: Check underscore patterns with regex matching
    score, _, _ = blregex(blacklist, text)
    if score > highest:
        highest = score

    # Step 2: For blacklist patterns without underscore, do fuzzy matching
    for pattern in blacklist:
        if "_" in pattern:
            continue  # skip underscore patterns; already checked above
        plen = len(pattern)
        pattern_lower = pattern.lower()
        for i in range(len(text) - plen + 1):
            chunk = text[i:i+plen]
            score = fuzz.ratio(pattern_lower, chunk)
            if score > highest:
                highestchunk = chunk
                highest = score
    return highest, highestchunk


with open('data.json', 'r', encoding="utf-8") as f:
    data = json.load(f)

substitutes = data["substitutes"]
blacklist = data["blacklist"]
whitelist = data["whitelist"]
messageThreshold = data["threshold"]

def findSub(char):
    return substitutes.get(char, char)

def remove_duplicates(s):
    seen = set()
    result = []
    for c in s:
        if c not in seen:
            seen.add(c)
            result.append(c)
    return "".join(result)

def remove_whitelist_words(text, whitelist_patterns):
    for pattern in whitelist_patterns:
        text = text.replace(pattern.lower(), "")
        regex_pattern = pattern.replace("_", ".")
        text = re.sub(regex_pattern, "", text, flags=re.IGNORECASE)
    return text

def filter(message):
    lowered = message.lower()
    highest = 0

    # Step 1: Run blregex on raw message (before whitelist removal)
    score, _, _ = blregex(blacklist, lowered)
    if score > highest:
        highest = score

    # Step 3: Now remove whitelist words for fuzzy matching steps if desired
    cleaned = remove_whitelist_words(lowered, whitelist)
    #print("Cleaned: " + cleaned)
    score, c = qFilter(cleaned)
    if score > highest:
        highest = score

    # Step 4: Fuzzy matching with substitutions, spaces removed, duplicates removed
    cleaned = "".join(findSub(c) for c in cleaned)
    score, c = qFilter(cleaned)
    if score > highest:
        highest = score

    cleaned = cleaned.replace(" ", "")
    score, c = qFilter(cleaned)
    if score > highest:
        highest = score

    cleaned = remove_duplicates(cleaned)
    score, c = qFilter(cleaned)
    if score > highest:
        highest = score

    return highest, c


# Test
tests = [
    "nigga",
    "nigger",
    "n1gger",
    "m1g3333333r5aaaaaaaabcdef",
    "niiiiigggggger",
    "hello my name is keepcrying and i am making a filter for the bronx server",
    "nigegegeger",
    "dirtyniggas",
    "clean message",
    "nger",
    "ntger",
    "ntgr",
    "eviln1g3r67",
    "niger",
    "anger nigger",
    "ning e",
    "nbiger",
    "bigger"
]

for t in tests:
    highest, _ = filter(t)
    print(f"{t:<30}: {highest:.2f}")
