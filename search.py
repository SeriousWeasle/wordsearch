import requests, time
from lxml import html

wordlist_url_base = "http://woordenlijst.eu/woorden_beginnend_met.php?current="
has_letters = []

allowed_letters = input("Allowed letters: ")
flags = input("check repeat/length/indexes?: ")
for i, f in enumerate(flags):
    if f == "1":
        if i == 0:
            check_repeat = True
        if i == 1:
            check_length = True
        if i == 2:
            check_indexes = True
    else:
        if i == 0:
            check_repeat = False
        if i == 1:
            check_length = False
        if i == 2:
            check_indexes = False

if check_length:
    length = int(input("word length: "))

if check_indexes:
    pairstring = input("specify pairs (letter, idx): ")
    pairs = int(len(pairstring)/2)
    for n in range(pairs):
        pair = []
        pair.append(pairstring[(n*2)])
        pair.append(int(pairstring[(n*2) + 1]))
        has_letters.append(pair)

st = time.time()

def isAllowed(w):
    if check_length:
        if len(w) != length:
            return False
    if not check_repeat:
        for l in w:
            if l.lower() not in allowed_letters:
                return False
    
    if  check_repeat:
        used = []
        for l in w:
            if l.lower() not in used and l.lower() in allowed_letters:
                used.append(l.lower())
            else: return False

    if check_indexes:
        for pair in has_letters:
            if len(w) < pair[1]:
                return False
            if w[pair[1] - 1].lower() != pair[0]:
                return False

    return True
searchTime = 0
for l in allowed_letters:
    wordlist_url = wordlist_url_base + l
    sst = time.time()
    wordlist_page = requests.get(wordlist_url)
    est = time.time()
    searchTime += (est - sst)
    tree_page_wordlist = html.fromstring(wordlist_page.content)
    tree_page_words = tree_page_wordlist.xpath("//a/text()")
    current_words = []
    for w in tree_page_words:
        if w[0] == l or w[0] == l.upper():
            if isAllowed(w):
                current_words.append(w)
    print(current_words)

et = time.time()

print("Completed search in", round(et - st, 2), "seconds.\nWait time:", round(searchTime, 2), "seconds\nSearch time:", round(et-st-searchTime,2), "seconds")
