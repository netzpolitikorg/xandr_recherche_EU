import re
from unidecode import unidecode

# all of these characters have been found to separate words. In regEx searches, this set replaces space characters 
word_separator = r"[\ \-–_\|\,]{1,4}"


def list_to_regex(lst):
    """Convert a list of strings into a regEx that matches either of the strings. All space characters
    are replaced by a list of possible word-separators.

    Arguments:
        lst -- list of raw-formatted strings

    Returns:
        compiled regular expression
    """
    lst = [el.replace(" ", word_separator) for el in lst]
    return re.compile("|".join(lst), re.IGNORECASE)


separator_hierarchy = [
    re.compile(r">|:+| \- | – |\_|\[|\]|\(|\)|\||\,"),  # > : :: - – _ ( ) [ ] | ,
    re.compile(r"/|–|\-"), # / - – only use this, if all others fail. It otherwise causes quite a few false positive splits.
    # r" ", # <space> kind of debatable if this should be used as a last resort... i'm gonna go with no.
]

useless_segments_re = list_to_regex([r"\[null\]",               # [null]
                                     r"\Atest",                 # starts with 'test'
                                     r"[^a-z]+test\Z",          # ends with 'test'
                                     r" test ",                 # 'test' not encompassed in a word
                                     r"\A[a-z0-9]{0,6}\Z",      # very short segment names
                                     r"automation\d{5,10}"])    # don't know what it is but it's useless


def clean_segment_name(name: str):
    """Cleans a string, i.e. strips spaces and quotation marks, replaces non-unicode characters and converts to lowercase.

    Arguments:
        name -- unformatted segment name

    Returns:
        cleaned segment name
    """
    name = str(name).strip().lower()

    # sometimes segment names are enquoted...
    if name[0] == name[-1] == '"':
        name = name[1:-1]

    return unidecode(name)  # remove diactrics and other non-unicode characters


def itemize_segment_name(name: str):
    """Splits a string along a set of possible separators, and cleans up the resulting list

    Arguments:
        name -- segment name to be itemized

    Returns:
        list of strings
    """
    for sep_re in separator_hierarchy:
        items = re.split(sep_re, name)

        if len(items) > 1:
            break

    items = [i.strip() for i in items]  # strip all entries
    items = list(filter(None, items))  # remove empty entries

    return items
