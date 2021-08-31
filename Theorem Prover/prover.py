#Theorem Prover (md5jd)
import sys
#data structures for variables, facts, and rules
#variables - A-Z, a-z
r_var = {}
l_var = {}
#facts - true/false
facts = {}
#rules - (->)
rules = {}

spec = ["(", ")", "!", "&", "|"]
dualspec = [")&", ")|", "!!", "&!", "|!", "(!", "))", "!(", "&(", "|(", "(("]

CtoW = {"(": "(", ")": ") ", "&": "AND ", "|": "OR ", "!": "NOT "}

#helpers
def varDef(variable):
    if variable in r_var:
        return r_var[variable][1:-1]
    elif variable in l_var:
        return l_var[variable][1:-1]
    else:
        print("sad :(")
        return

def checkVars(variable):
    if variable in r_var or variable in l_var:
        return True
    return False

def removeLearned():
    for x in l_var:
        if x in facts:
            del facts[x]
    return

def ruleParse(rule):
    var = ""
    for x in rule:
        if x in spec and not(len(var) == 0):
            if not (checkVars(var)):
                return False
            var = ""
        elif x in spec:
            continue
        else:
            var += x
    if not(len(var) == 0):
        if not(checkVars(var)):
            return False
    return True

def isValid(expr):
    if len(expr) == 0:
        return False
    if expr[0] == "&" or expr[0] == "|" or expr[0] == ")":
        return False
    if expr[-1] == "!" or expr[-1] == "&" or expr[-1] == "|" or expr[-1] == "(":
        return False
    count = 0
    tspec = ""
    for x in expr:
        if x in spec:
            tspec += x
            if len(tspec) == 2:
                if tspec not in dualspec:
                    return False
                tspec = tspec[1:]
        else:
            tspec = ""
        if x == "(":
            count += 1
        if x == ")":
            count -= 1
        if count < 0:
            return False
    if count > 0:
        return False
    return True

def tokenize(expression):
    expr = []
    for x in expression:
        if len(x) > 1:
            for a in x:
                expr.append(a)
                continue
        expr.append(x)
    return expr

def lastOp(expr):
    count = 0
    for i in range(len(expr)):
        if count == 0:
            if expr[i] == "|":
                return expr[i], i
        if expr[i] == ")":
            count -= 1
        if expr[i] == "(":
            count += 1
    count = 0
    for i in range(len(expr)):
        if count == 0:
            if expr[i] == "&":
                return expr[i], i
        if expr[i] == ")":
            count -= 1
        if expr[i] == "(":
            count += 1
    count = 0
    for i in range(len(expr)):
        if count == 0:
            if expr[i] == "!":
                return expr[i], i
        if expr[i] == ")":
            count -= 1
        if expr[i] == "(":
            count += 1
    return None, None

def ruleDump(expr):
    rule_str = ""
    for e in expr:
        if e not in spec:
            rule_str += varDef(e)
            rule_str += " "
        else:
            if e == ")":
                rule_str = rule_str[:-1]
            rule_str += CtoW[e]
    return rule_str[:-1]

def whyQuery(expression):
    expr = tokenize(expression)
#Base Cases
    if len(expr) < 2:
        if len(expr) == 0:
            return
        var = expr[0]
        count = 0
        if var in r_var:
            if facts[var]:
                print("I KNOW THAT", ruleDump(var))
                return
            else:
                print("I KNOW IT IS NOT TRUE THAT", ruleDump(var))
                return
        if var in rules:
            for n in rules[var]:
                if Query(n):
                    whyQuery(n)
                    print("BECAUSE", ruleDump(n),"I KNOW THAT", ruleDump(var))
                    return
        if var in rules: # none of the rules are true
            for n in rules[var]:
                count += 1
                whyQuery(n)
                print("BECAUSE IT IS NOT TRUE THAT", ruleDump(n), "I CANNOT PROVE", ruleDump(var))
        if count == 0:
            print("I KNOW IT IS NOT TRUE THAT", ruleDump(var))
        return

    if isValid(expr[1:-1]):
        op, ind = lastOp(expr[1:-1])
        qLeft = expr[1:ind+1]
        qRight = expr[ind+2:-1]
        left = expr[:ind+1]
        right = expr[ind+2:]

    else:
        op, ind = lastOp(expr)
        left = expr[:ind]
        right = expr[ind+1:]
        qLeft = expr[:ind]
        qRight = expr[ind+1:]

#AND
    if op == "&":
        if Query(qLeft) and Query(qRight):
            whyQuery(qLeft)
            whyQuery(qRight)
            print("I THUS KNOW THAT", ruleDump(left), "AND", ruleDump(right))
            return
        else:
            if not Query(qLeft):
                whyQuery(qLeft)
                print("THUS I CANNOT PROVE", ruleDump(left), "AND", ruleDump(right))
                return
            else:
                whyQuery(qRight)
                print("THUS I CANNOT PROVE", ruleDump(left), "AND", ruleDump(right))
                return
#OR
    if op == "|":
        if Query(qLeft) or Query(qRight): #if the or is true --> print 1
            if Query(qLeft):
                whyQuery(qLeft)
            else:
                whyQuery(qRight)
            print("I THUS KNOW THAT", ruleDump(left), "OR", ruleDump(right))
            return
        else:# --> if the or is false print both
            whyQuery(qLeft)
            whyQuery(qRight)
            print("THUS I CANNOT PROVE", ruleDump(left), "OR", ruleDump(right))
            return
#NOT
    if op == "!":
        if not Query(qLeft[1:]+qRight):
            whyQuery(qLeft[1:]+qRight)
            print("I THUS KNOW THAT NOT", ruleDump(left[1:]+right))
        else:
            whyQuery(qLeft[1:]+qRight)
            print("THUS I CANNOT PROVE NOT", ruleDump(left[1:]+right))



#Teach, List, Learn, Query, Why
def ListKnown():
    print("Root Variables:\n\t")
    for i in r_var:
        print(i, "=", r_var[i])
        print("\n\t")
    print("Learned Variables:\n\t")
    for j in l_var:
        print(j, "=", l_var[j])
        print("\n\t")
    print("Facts:\n\t")
    for k in facts:
        print(k)
        print("\n\t")
    print("Rules:\n\t")
    for l in rules:
        print(rules[l], "->", l)
        print("\n\t")
    return

def Teach(expr):
    if expr[0] == "-R":
        var = expr[1]
        sen = expr[3]
        expr = expr[4:]
        for x in expr:
            sen += " "
            sen += x
        r_var[var] = sen
        facts[var] = False
    elif expr[0] == "-L":
        var = expr[1]
        sen = expr[3]
        expr = expr[4:]
        for x in expr:
            sen += " "
            sen += x
        l_var[var] = sen
    else:
        if expr[1] == "=":
            if expr[0] in r_var:
                if expr[2] == "true":
                    facts[expr[0]] = True
                    removeLearned()
                elif expr[2] == "false":
                    facts[expr[0]] = False
                    removeLearned()
                else:
                    print("not true or false??")
                    return
            else:
                print("variable not in root variable list")
                return
        elif expr[1] == "->":
            if expr[2] in l_var:
                if ruleParse(expr[0]):
                    if expr[2] in rules:
                        rules[expr[2]].append(expr[0])
                    else:
                        rules[expr[2]] = [expr[0]]
                return
        else:
            print("something is wrong")
            return
    return

def Learn():
    for var in l_var:
        if var in rules:
            for rule in rules[var]:
                if Query(rule):
                    facts[var] = True
                    break
                else:
                    facts[var] = False
    return

def Query(expression):
    expr = tokenize(expression)
    if len(expr) < 2:
        var = expr[0]
        if var in facts:
            return facts[var]
        if var in rules:
            for n in rules[var]:
                if Query(n):
                    return True
        return False

    if isValid(expr[1:-1]):
        return Query(expr[1:-1])

    op, ind = lastOp(expr)
    if op == "&":
        return Query(expr[0:ind]) and Query(expr[ind+1:])
    if op == "|":
        return Query(expr[0:ind]) or Query(expr[ind+1:])
    if op == "!":
        return not Query(expr[1:])

def Why(expr):
    if Query(expr):
        print("true")
    else:
        print("false")
    return whyQuery(expr)

def run(expression):
    expr = expression.split()
    if expr[0] == "List":
        return ListKnown()
    elif expr[0] == "Teach":
        return Teach(expr[1:])
    elif expr[0] == "Learn":
        return Learn()
    elif expr[0] == "Query":
        if Query(expr[1:]):
            print("true")
        else:
            print("false")
        return
    elif expr[0] == "Why":
        return Why(expr[1:])
    else:
        print("error bad input")
        return

#MAIN (i guess)
try:
    line = input("")
    while line != "0" or None:
        run(line)
        line = input("")
        #print(r_var, l_var)
        #print(rules, facts)
    exit()
except EOFError:
    print("end")