from collections import Counter


def shannon_fano(symbols, codebook):
    if len(symbols) <= 1:
        return

    total = sum(freq for _, freq in symbols)
    acc = 0
    split = 0

    for i in range(len(symbols)):
        acc += symbols[i][1]
        if acc >= total / 2:
            split = i
            break

    left = symbols[:split + 1]
    right = symbols[split + 1:]

    for ch, _ in left:
        codebook[ch] += "0"
    for ch, _ in right:
        codebook[ch] += "1"

    shannon_fano(left, codebook)
    shannon_fano(right, codebook)


def compress(text):
    freq = Counter(text)
    symbols = sorted(freq.items(), key=lambda x: x[1], reverse=True)

    codebook = {ch: "" for ch, _ in symbols}
    shannon_fano(symbols, codebook)

    encoded = ''.join(codebook[ch] for ch in text)
    return encoded, codebook


def decompress(encoded, codebook):
    reverse = {v: k for k, v in codebook.items()}

    decoded = ""
    temp = ""

    for bit in encoded:
        temp += bit
        if temp in reverse:
            decoded += reverse[temp]
            temp = ""

    return decoded
