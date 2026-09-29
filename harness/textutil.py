"""Tokenising for keyword search: lowercase, drop stopwords, strip common endings."""
import re

STOP = set("""a an the and or but if then than that this these those is are was were be been being am do does did
doing have has had having i me my mine we our you your he she it its they them their what which who whom whose when
where why how to of in on at by for with about against between into through during before after above below from up
down out off over under again further once here there all any both each few more most other some such no nor not
only own same so too very can will just should now also as one""".split())

SUFFIXES = ("ization", "ations", "ation", "ments", "ment", "ingly", "ings", "ing", "ies", "ied", "ed", "es", "ly", "s")


def stem(word):
    for suffix in SUFFIXES:
        if word.endswith(suffix) and len(word) - len(suffix) >= 3:
            word = word[: -len(suffix)]
            if suffix in ("ies", "ied"):
                word += "y"
            break
    return word


def terms(text):
    """Content terms of a text, stemmed. Numbers such as 492.0 are kept whole."""
    raw = re.findall(r"[a-z0-9]+(?:\.[0-9]+)?", text.lower())
    return [stem(t) for t in raw if t not in STOP and len(t) > 1]


def numbers(text):
    """Numbers in a text, normalised (commas removed), for grounding checks."""
    found = re.findall(r"(?<![A-Za-z])\d[\d,]*(?:\.\d+)?", text)
    return {n.replace(",", "").rstrip(".") for n in found}


def word_count(text):
    return len(text.split())
