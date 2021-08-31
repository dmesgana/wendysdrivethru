import Crypto.Util.number, binascii
#xor
string = "label"
full = ""
for x in string:
    dec = ord(x)
    dec ^= 13
    #print(chr(dec), end='')

#key flag xor
key1 = int("a6c8b6733c9b22de7bc0253266a3867df55acde8635e19c73313", 16)
key2_enc = int("37dcb292030faa90d07eec17e3b1c6d8daf94c35d4c9191a5e1e", 16)
key3_enc = int("c1545756687e7573db23aa1c3452a098b71a7fbf0fddddde5fc1", 16)
flag_enc = int("04ee9855208a2cd59091d04767ae47963170d1660df7f56f5faf", 16)

key2 = key1^key2_enc
key3 = key2^key3_enc
flag = flag_enc^key1^key2^key3

#fav bit

fav = int("73626960647f6b206821204f21254f7d694f7624662065622127234f726927756d", 16)
prp = int("101010101010101010101010101010101010101010101010101010101010101010", 16)
prep = prp^fav
#print(Crypto.Util.number.long_to_bytes(prep))

#not mine (someone on the website 'StormXploit')
string = binascii.unhexlify("73626960647f6b206821204f21254f7d694f7624662065622127234f726927756d")

def decode_xor(string, x):
    l = [c for c in string]
    for i in range(x):
         f = [chr(n^i) for n in l]
         a = "".join(f)
         if a.startswith("crypto"):
            print(a)
            break

flag2 = binascii.unhexlify("0e0b213f26041e480b26217f27342e175d0e070a3c5b103e2526217f27342e175d0e077e263451150104")
key = "myXORkey"
y = [ord(d) for d in key]
w = [c for c in flag2]

def decode_hex(w):
    s = ""
    for z in range(len(w)):
        s = s + chr(w[z]^y[z%7])
    return s