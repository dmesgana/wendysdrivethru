#!/usr/bin/env python3

import telnetlib
import json
from encoding_task import decode_base64, decode_HEX, decode_rot13, decode_LNG, decode_ASCII

HOST = "socket.cryptohack.org"
PORT = 13377

tn = telnetlib.Telnet(HOST, PORT)


def readline():
    return tn.read_until(b"\n")

def json_recv():
    line = readline()
    return json.loads(line.decode())

def json_send(hsh):
    request = json.dumps(hsh).encode()
    tn.write(request)

def tt_decode(method, string):
    if method == "base64":
        return decode_base64(string)
    elif method == "hex":
        return decode_HEX(string)
    elif method == "rot13":
        return decode_rot13(string)
    elif method == "bigint":
        return decode_LNG(string)
    elif method == "utf-8":
        return decode_ASCII(string)
    else:
        return "??"

def parse_binary(resp, d):
    if d == 0:
        resp1, resp2 = resp.decode("utf-8").strip().split(",", 1)
        resp1 = resp1[10:-1]
        if resp1 == "utf-8":
            resp2 = resp2[12:-2].split(",")
            enc = []
            for i in resp2:
                enc.append(int(i[1:]))
            print(enc)
            return resp1, enc
        else:
            resp2 = resp2[13:-2]
            print(resp2)
            return resp1, resp2
    else:
        resp1 = resp["type"]
        resp2 = resp["encoded"]
        return resp1, resp2



request = {
    "decoded": "yo"
}
response = readline()
d = 0
while True:
    print(response)
    type, encoded = parse_binary(response, d)
    d+=1
    print(type)
    print(encoded)
    decode = tt_decode(type, encoded)
    print(decode)
    request["decoded"] = decode
    json_send(request)
    response = json_recv()
