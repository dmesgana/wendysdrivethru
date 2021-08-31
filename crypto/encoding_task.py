import json, base64, Crypto.Util.number, codecs

#ROT13
string = "dhvpx oebja sbk"

def decode_rot13(string):
    return codecs.decode(string, "rot13")
#print("rot13: " + decode_rot13(string))

#ASCII
list = [99, 114, 121, 112, 116, 111, 123, 65, 83, 67, 73, 73, 95, 112, 114, 49, 110, 116, 52, 98, 108, 51, 125]

def decode_ASCII(list):
    finale = ""
    for i in list:
        finale += chr(i)
    return finale
#print("ASCII: " + decode_ASCII(list))

#HEX
hex_boi = "63727970746f7b596f755f77696c6c5f62655f776f726b696e675f776974685f6865785f737472696e67735f615f6c6f747d"

def decode_HEX(hex_boi):
    result = bytearray.fromhex(hex_boi).decode("utf-8")
    return result
#print("HEX: ", end="")
#print(decode_HEX(hex_boi))

#BASE64
base_boosted = "72bca9b68fc16ac7beeb8f849dca1d8a783e8acf9679bf9269f7bf"

def decode_base64(base_boosted):
    yah = base64.b64decode(base_boosted).decode("utf-8")
    return yah
#print("BASE64: ", end="")
#print(decode_base64(base_boosted))

#BYTES AND BIG INTEGERS
bites = "11515195063862318899931685488813747395775516287289682636499965282714637259206269"

def decode_LNG(bites):
    input = int(bites, 16)
    city = Crypto.Util.number.long_to_bytes(input).decode("utf-8")
    return city
#print(decode_LNG(bites))