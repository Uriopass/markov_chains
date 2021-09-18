from collections import defaultdict
from itertools import chain, tee, islice
import random

def consume(iterator, n):
    "Advance the iterator n-steps ahead. If n is none, consume entirely."
    # Use functions that consume iterators at C speed.
    if n is None:
        # feed the entire iterator into a zero-length deque
        collections.deque(iterator, maxlen=0)
    else:
        # advance to the empty slice starting at position n
        next(islice(iterator, n, n), None)

def window(iterable, n=2):
    "s -> (s0, ...,s(n-1)), (s1, ...,sn), (s2, ..., s(n+1)), ..."
    iters = tee(iterable, n)
    # Could use enumerate(islice(iters, 1, None), 1) to avoid consume(it, 0), but that's
    # slower for larger window sizes, while saving only small fixed "noop" cost
    for i, it in enumerate(iters):
        consume(it, i)
    return zip(*iters)


def genword(words, TOGEN=1, power=1, noexisting=True):
    word_dic = set(words)


    N = defaultdict(lambda: defaultdict(int))

    WINDOW_SIZE = 2
    ST = tuple(['<start>'] * WINDOW_SIZE)
    END = tuple(['<end>'] * WINDOW_SIZE)

    for word in words:
        if len(word) == 0:
            continue
        word = list(chain(ST, word, END))
        for letter, nex in zip(window(word, WINDOW_SIZE), window(word[1:], WINDOW_SIZE)):
            N[letter][nex] += 1

    V = dict()

    for l,v in N.items():
        ll = []
        s = 0
        for nex,c in sorted(v.items(), key=lambda x: x[1]):
            s += c ** power
            ll.append((nex, s))
        V[l] = (ll, s)
        cur = ST
        w = ''
    #print(V[("<start>", "<start>")])
    for _ in range(TOGEN):
        cur = ST
        w = []
        while True:
            d = V[cur]
            r = random.random() * d[1]
            for nex,cs in d[0]:
                if cs > r:
                    cur = nex
                    break
            if cur == END:
                break
            if cur[0] != '<start>':
                w.append(cur[0])
        if noexisting and tuple(w) in word_dic:
            continue
        yield w

if __name__ == "__main__":
    words = list(x.strip() for x in open("fr.txt", "r").readlines())
    for w in genword(words, 1000):
        if len(w) <= 2 or len(w) >= 20:
            continue
        print("".join(w))
