
alphabet = [letter for letter in 'abcdefghijklmnopqrstuvwxyz']
fibonacci = [1, 2]
for i in range(2, 30):
    fibonacci.append(fibonacci[i - 2] + fibonacci[i - 1])

def fibCypher(key, msg):
    enc = []
    key_ind = alphabet.index(key) + 1
    for char in range(len(msg)):
        enc.append(str(ord(alphabet[(key_ind + fibonacci[char]) % 26 - 1]) + ord(msg[char])))
    return ' '.join(enc)

print(fibCypher('h', 'ACSL c2'))

x = 0

for a in range(1, 11):
    for b in range(1, a + 1):
        if a % b == 0: x += 1

print(x)