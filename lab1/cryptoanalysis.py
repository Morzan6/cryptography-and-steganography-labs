from simple_substitution_cipher import SimpleSubstitutionCipher

from affine_cipher import AffineCipher
from recursive_affine_cipher import RecursiveAffineCipher
from collections import Counter

default_freq = {
    "E": 12.0,
    "T": 9.10,
    "A": 8.12,
    "O": 7.68,
    "I": 7.31,
    "N": 6.95,
    "S": 6.28,
    "R": 6.02,
    "H": 5.92,
    "D": 4.32,
    "L": 3.98,
    "U": 2.88,
    "C": 2.71,
    "M": 2.61,
    "F": 2.30,
    "Y": 2.11,
    "W": 2.09,
    "G": 2.03,
    "P": 1.82,
    "B": 1.49,
    "V": 1.11,
    "K": 0.69,
    "X": 0.17,
    "Q": 0.11,
    "J": 0.10,
    "Z": 0.07,
}

# Encrypt
plaintext = "Many of the Ents are younger than I am, by many lives of trees. They are all roused now, and their mind is all on one thing breaking Isengard. But they will start thinking again before long they will cool down a little. But let them march now and sing. We have a long way to go, and there is time ahead for thought. It is something to have started".upper()
print(plaintext.upper())
key = "QWERYUTIOPASDFGHJKLXZCVBNM"
cipher = SimpleSubstitutionCipher(key=key)
ciphertext = cipher.encrypt(plaintext=plaintext)
print(ciphertext)
# Count letter frequensy of cleared ciphertext, if letter not found set as 0.0
freq = {k: 0.0 for k, _ in default_freq.items()}
ciphertext_cleared = ciphertext.replace(",", "").replace(".", "").replace(" ", "")
for letter, count in Counter(ciphertext_cleared).items():
    freq[letter] = count / len(ciphertext_cleared) * 100

# Sort frequensies to map in to each other
freq = sorted(freq.items(), reverse=True, key=lambda x: x[1])
default_freq = sorted(default_freq.items(), reverse=True, key=lambda x: x[1])

# Make csv table of frequensies, and generate pairs of substitution predictions
table = []
pairs = []
for (letter_in_text, freq_in_text), (letter, freq_by_default) in zip(
    freq, default_freq
):
    table.append(
        ";".join(
            [
                letter,
                "{:.2f}".format(freq_by_default),
                letter_in_text,
                "{:.2f}".format(freq_in_text),
            ]
        )
        + "\n"
    )
    pairs.append((letter, letter_in_text))
with open("freq_analysis.csv", "w") as f:
    f.writelines(table)

# Sort predicted substitution pairs and predict key
pairs = sorted(pairs, key=lambda x: x[0])
predict_key = "".join([j for _, j in pairs])
print(predict_key)
# Try to decrypt using predicted key
cipher = SimpleSubstitutionCipher(key=predict_key)
predict_plaintext = cipher.decrypt(ciphertext=ciphertext)
print(predict_plaintext)
