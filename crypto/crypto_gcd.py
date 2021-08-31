def gcd(a, b):
    if a == b:
        print(a)
        return
    if a > b:
        a = a - b
        gcd(a, b)
    elif b > a:
        b = b - a
        gcd(a, b)
    else:
        print("something's going wrong")
        return

def extnd_gcd(a,b):
    if a == 0:
        return b, 0, 1
    gcd, x1, y1 = extnd_gcd(b%a, a)
    x = y1 - (b//a) * x1
    y = x1
    return gcd, x, y

p = 26513
q = 32321

print(extnd_gcd(p, q))