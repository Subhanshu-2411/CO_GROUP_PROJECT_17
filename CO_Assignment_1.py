
import sys

def bin(value, noOfDigits = 16):  # returns the binary value of the number

    i = 1 << noOfDigits - 1  # Also takes the no of digit to be displayed for representation and default is 32
    x = ""
    while (i > 0):
        if ((value & i) != 0):
            x += "1"
        else:
            x += "0"
        i = i // 2
    return x

def registerValue(a):
    if a == 'R0':
        a = '000'
    elif a == 'R1':
        a = '001'
    elif a == 'R2':
        a = '010'
    elif a == 'R3':
        a = '011'
    elif a == 'R4':
        a = '100'
    elif a == 'R5':
        a = '101'
    elif a == 'R6':
        a = '110'
    elif a == 'FLAGS':
        a = '111'
    else:
        pass

    return a

functionOpcode = {'0': 'addition',
                  '1': 'subtraction',
                  '2': 'moveimmediate',
                  '3': 'moveregister',
                  '4': 'load',
                  '5': 'store',
                  '6': 'multiply',
                  '7': 'divide',
                  '8': 'rightshift',
                  '9': 'leftshift',
                  '10': 'exclusiveor',
                  '11': 'or',
                  '12': 'and',
                  '13': 'invert',
                  '14': 'compare',
                  '15': 'unconcditionaljump',
                  '16': 'jumpiflessthan',
                  '17': 'jumpifgreaterthan',
                  '18': 'jumpifequal',
                  '19': 'halt'}

def return_key(val):
    for key, value in functionOpcode.items():
        if value == val:
            return key
    return -1

def binToDec(x):
    num = 0
    i = 0
    while (x > 0):
        y = x % 10
        if (y == 1):
            num += pow(2, i)
        i = i + 1
        x = (x - y) / 10
    return num

def RegisterError(i):
    print(f"Typos in Register Name                                # line {i}")

def UndefinedVariables(i):
    print(f"Variable used is not defined                          # line {i}")

def UndefinedLabels(i):
    print(f"Label used is not defined                             # line {i}")

def FlagError(i):
    print(f"Illegal use of Flag Register                          # line {i}")

def ImmediateValueError(i):
    print(f"Illegal Immediate Value                               # line {i}")

def WrongVariableDeclaration(i):
    print(f"Variable not declared at the begining                 # line {i}")

def MissingHlt(i):
    print(f"Halt Function Missing                                 # line {i}")

def HltNotLast(i):
    print(f"Halt Function is not the Last Function                # line {i}")

def SyntaxError(i):
    print(f"Wrong Syntax used for Instruction                     # line {i}")

def NOT(x):
    y = ""
    for i in x:
        if i == "0":
            y += "1"
        elif i == "1":
            y += "0"
    return int(y)

var = {}     # variable storage list containing variable name and value of the variable (default as = 0)


label = {}   # label function not yet implemented


def checkName(x):

    return x.isalnum()

flag = []
x: str
lst = []
ans = []
registerStorage = [0, 0, 0, 0, 0, 0, 0, 0]

programCounter = -1

def function(i, programCounter):
    if (lst[i][0] == 'add'):
        add(i,programCounter)
    if(lst[i][0] == 'sub'):
        sub(i,programCounter)
    if(lst[i][0] == 'mul'):
        mul(i,programCounter)
    if(lst[i][0] == 'div'):
        div(i,programCounter)
    if(lst[i][0] == 'rs'):
        rs(i,programCounter)
    if(lst[i][0] == 'ls'):
        ls(i,programCounter)
    if(lst[i][0] == 'sub'):
        sub(i,programCounter)
    if(lst[i][0] == 'xor'):
        xor(i,programCounter)
    if(lst[i][0] == 'or'):
        OR(i,programCounter)
    if(lst[i][0] == 'and'):
        AND(i,programCounter)
    if(lst[i][0] == 'not'):
        NOTlabel(i,programCounter)
    if(lst[i][0] == 'cmp'):
        CMP(i,programCounter)
    if(lst[i][0] == 'load'):
        load(i,programCounter)
    if(lst[i][0] == 'store'):
        store(i,programCounter)
    if(lst[i][0] == 'hlt'):
        hlt(i,programCounter)
    Simulator(programCounter,0)
def add(i,programCounter):
    a = binToDec(int(registerValue(lst[i][1])))
    b = binToDec(int(registerValue(lst[i][2])))
    c = binToDec(int(registerValue(lst[i][3])))
    registerStorage[a] = registerStorage[b] + registerStorage[c]
    temp = registerStorage[a]
    p = 'addition'
    ans.append(bin(int(return_key(p)), 5)+"00"+registerValue(lst[i][1])+registerValue(lst[i][2])+registerValue(lst[i][3]))
    if (registerStorage[a] > 2 ** 16 - 1):
        # This will set the flag since because of the addition the value stored in the destination
        # register is now greater than the permissible value of 2^16-1
        registerStorage[7] = 8
        registerStorage[binToDec(int(registerValue(lst[i][1])))] = 2 ** 16 - 1
    else:
        registerStorage[7] = 0
    programCounter = programCounter + 1
    Simulator(programCounter, 0)
def sub(i,programCounter):
    a = binToDec(int(registerValue(lst[i][1])))
    b = binToDec(int(registerValue(lst[i][2])))
    c = binToDec(int(registerValue(lst[i][3])))
    registerStorage[a] = registerStorage[b] - registerStorage[c]
    p = 'subtraction'
    ans.append(bin(int(return_key(p)), 5) + "00" + registerValue(lst[i][1]) + registerValue(lst[i][2]) + registerValue(lst[i][3]))
    if (registerStorage[binToDec(int(registerValue(lst[i][1])))] < 0):
        # This will set the flag since because of the subtraction the value stored in the destination
        # register is now negative
        registerStorage[7] = 8
        registerStorage[binToDec(int(registerValue(lst[i][1])))] = 0
    else:
        registerStorage[7] = 0
    programCounter = programCounter + 1
    Simulator(programCounter, 0)
def mul(i,programCounter):
    a = binToDec(int(registerValue(lst[i][1])))
    b = binToDec(int(registerValue(lst[i][2])))
    c = binToDec(int(registerValue(lst[i][3])))
    registerStorage[a] = registerStorage[b] * registerStorage[c]
    p = 'multiply'
    ans.append(bin(int(return_key(p)), 5) + "00" + registerValue(lst[i][1]) + registerValue(lst[i][2]) + registerValue(lst[i][3]))
    if (registerStorage[binToDec(int(registerValue(lst[i][1])))] > 2 ** 16 - 1):
        # This will set the flag since because of the multiplication the value stored in the destination
        # register is now greater than the permissible value of 2^16-1
        registerStorage[7] = 8
        registerStorage[binToDec(int(registerValue(lst[i][1])))] = 2 ** 16 - 1
    else:
        registerStorage[7] = 0
    programCounter = programCounter + 1
    Simulator(programCounter, 0)
def div(i,programCounter):
    registerStorage[0] = registerStorage[binToDec(int(registerValue(lst[i][1])))] // registerStorage[binToDec(int(registerValue(lst[i][2])))]
    registerStorage[1] = registerStorage[binToDec(int(registerValue(lst[i][1])))] % registerStorage[binToDec(int(registerValue(lst[i][2])))]
    p = 'divide'
    ans.append(bin(int(return_key(p)), 5) + "00000" + registerValue(lst[i][1]) + registerValue(lst[i][2]))
    programCounter = programCounter + 1
    Simulator(programCounter, 0)
def rs(i,programCounter):
    p = 'rightshift'
    x = binToDec(int(registerValue(lst[i][1])))
    registerStorage[x] = registerStorage[x] >> lst[i][2]
    ans.append(bin(int(return_key(p)), 5) + registerValue(lst[i][1]) + bin(int(lst[i][2]), 8))
    programCounter = programCounter + 1
    Simulator(programCounter, 0)
def ls(i,programCounter):
    p = 'leftshift'
    x = binToDec(int(registerValue(lst[i][1])))
    registerStorage[x] = registerStorage[x] << lst[i][2]
    ans.append(bin(int(return_key(p)), 5) + registerValue(lst[i][1]) + bin(int(lst[i][2]), 8))
    programCounter = programCounter + 1
    Simulator(programCounter, 0)
def xor(i,programCounter):
    a = binToDec(int(registerValue(lst[i][1])))
    b = binToDec(int(registerValue(lst[i][2])))
    c = binToDec(int(registerValue(lst[i][3])))
    registerStorage[a] = registerStorage[b] ^ registerStorage[c]
    p = 'exclusiveor'
    ans.append(bin(int(return_key(p)), 5) + "00" + registerValue(lst[i][1]) + registerValue(lst[i][2]) + registerValue(
        lst[i][3]))
    programCounter = programCounter + 1
    Simulator(programCounter, 0)
def OR(i,programCounter):
    a = binToDec(int(registerValue(lst[i][1])))
    b = binToDec(int(registerValue(lst[i][2])))
    c = binToDec(int(registerValue(lst[i][3])))
    registerStorage[a] = registerStorage[b] + registerStorage[c]
    p = 'or'
    ans.append(bin(int(return_key(p)), 5) + "00" + registerValue(lst[i][1]) + registerValue(lst[i][2]) + registerValue(
        lst[i][3]))
    programCounter = programCounter + 1
    Simulator(programCounter, 0)
def AND(i,programCounter):
    a = binToDec(int(registerValue(lst[i][1])))
    b = binToDec(int(registerValue(lst[i][2])))
    c = binToDec(int(registerValue(lst[i][3])))
    registerStorage[a] = registerStorage[b] & registerStorage[c]
    p = 'and'
    ans.append(bin(int(return_key(p)), 5) + "00" + registerValue(lst[i][1]) + registerValue(lst[i][2]) + registerValue(lst[i][3]))
    programCounter = programCounter + 1
    Simulator(programCounter, 0)
def NOTlabel(i,programCounter):
    p = 'invert'
    registerStorage[int(binToDec(int(registerValue(lst[i][1]))))] = NOT(str(bin(registerStorage[binToDec(int(registerValue(lst[i][2])))])))
    ans.append(bin(int(return_key("")), 5) + "00000" + registerValue(lst[i][1]) + registerValue(lst[i][2]))
    programCounter = programCounter + 1
    Simulator(programCounter, 0)
def CMP(i,programCounter):
    if registerStorage[binToDec(int(registerValue(lst[i][1])))] > registerStorage[
        binToDec(int(registerValue(lst[i][2])))]:
        flag = 2
    elif registerStorage[binToDec(int(registerValue(lst[i][1])))] < registerStorage[
        binToDec(int(registerValue(lst[i][2])))]:
        flag = 4
    elif registerStorage[binToDec(int(registerValue(lst[i][1])))] == registerStorage[
        binToDec(int(registerValue(lst[i][2])))]:
        flag = 1
    ans.append(bin(int(return_key('compare')), 5) + "00000" + registerValue(lst[i][1]) + registerValue(lst[i][2]))
    programCounter = programCounter + 1
    Simulator(programCounter, flag)
def load(i,programCounter):
    variables = var.keys()
    p = 'load'
    if (lst[i][2] in variables):
        registerStorage[binToDec(int(registerValue(lst[i][1])))] = var[lst[i][2]]
    else:
        print("General syntax error on line number  " + str(i + 1))
    ans.append(bin(int(return_key(p)), 5) + registerValue(lst[i][1]) + bin(i + 1, 8))
    programCounter = programCounter + 1
    Simulator(programCounter, 0)
def store(i,programCounter):
    variables = var.keys()
    p = 'store'
    if (lst[i][2] in variables):
        var[lst[i][2]] = registerStorage[binToDec(int(registerValue(lst[i][1])))]
    else:
        print("General syntax error on line number  " + str(i + 1))
    ans.append(bin(int(return_key(p)), 5) + registerValue(lst[i][1]) + bin(i + 1, 8))
    programCounter = programCounter + 1
    Simulator(programCounter, 0)
def hlt(i,programCounter):
    ans.append(bin(int(return_key('halt')), 5) + "00000000000")
    programCounter = programCounter + 1
    Simulator(programCounter, 0)
    i = len(lst[i])-1

def Simulator(programCounter,flag):
    aux = []
    toAdd = bin(programCounter, 8)
    aux.append(str(toAdd))
    registerStorage[7] = flag
    for i in registerStorage:
        aux.append(bin(i, 16))
    sim.append(aux[0] + " " + aux[1] + " " + aux[2] + " " + aux[3] + " " + aux[4] + " " + aux[5] + " " + aux[6] + " " + aux[7] + " " + aux[8])


def trimmer(x):
    x = x.rstrip()
    x = x.lstrip()
    for i in range(1,20):
        x = x.replace("  "," ")
    return x
sim = []

while True:
    inst = input()
    if(inst == 'hlt'):
        lst.append(['hlt'])
        break
    elif(inst == ""):
        continue
    else:
        x = trimmer(inst)
        y = trimmer(x)
        lst.append(y.split(" "))

count = 0

a = False

for a in lst:
    if a[0] == lst[-1][0] == 'hlt':
        count += 1

if count == 1:
    global i
    for i in range(len(lst)):
        if 'label' in lst[i][0]:
            key = lst[i][0][:len(lst[i][0]) - 1]
            label[key] = int(i)
            lst[i] = lst[i][1:]
        if lst[i][0] == 'mov':
            if len(lst[i]) != 3:
                SyntaxError(i)
                break
            if lst[i][2][0] == 'R':
                p = 'moveregister'
                registerStorage[binToDec(int(registerValue(lst[i][1])))] = registerStorage[
                    binToDec(int(registerValue(lst[i][2])))]
                ans.append(bin(int(return_key(p)), 5) + "00000" + registerValue(lst[i][1]) + registerValue(lst[i][2]))
            elif lst[i][2] == "FLAGS":
                p = 'moveregister'
                registerStorage[binToDec(int(registerValue(lst[i][1])))] = binToDec(flag[-1])
                ans.append(bin(int(return_key(p)), 5) + "00000" + registerValue(lst[i][1]) + registerValue(lst[i][2]))
            else:
                p = 'moveimmediate'
                if int(lst[i][2][1]) < 0 or int(lst[i][2][1]) > 255:
                    ImmediateValueError(i)
                    break
                if lst[i][2][0] == '$':
                    lst[i][2] = lst[i][2][1:]
                    registerStorage[int(lst[i][1][1])] = int(lst[i][2])
                    ans.append(bin(int(return_key(p)), 5) + registerValue(lst[i][1]) + bin(int(lst[i][2]), 8))
            programCounter = programCounter + 1
            Simulator(programCounter, 0)
        elif lst[i][0] == 'add':
            if (len(lst[i]) != 4):
                SyntaxError(i)
                break
            registerStorage[binToDec(int(registerValue(lst[i][1])))] = registerStorage[binToDec(int(registerValue(lst[i][2])))] + registerStorage[binToDec(int(registerValue(lst[i][3])))]
            temp = registerStorage[binToDec(int(registerValue(lst[i][1])))]
            if (temp >= (2 ** 7) or temp < -(2 ** 7)):
                ans.append("0000000000001000")
                break
            p = 'addition'
            ans.append(
                bin(int(return_key(p)), 5) + "00" + registerValue(lst[i][1]) + registerValue(lst[i][2]) + registerValue(lst[i][3]))
            if (registerStorage[binToDec(int(registerValue(lst[i][1])))] > 2 ** 16 - 1):
                # This will set the flag since because of the addition the value stored in the destination
                # register is now greater than the permissible value of 2^16-1
                registerStorage[7] = 8
                registerStorage[binToDec(int(registerValue(lst[i][1])))] = (2 ** 16) - 1
            else:
                registerStorage[7] = 0
            programCounter = programCounter + 1
            Simulator(programCounter, 0)
        elif lst[i][0] == 'sub':
            if len(lst[i]) != 4:
                SyntaxError(i)
                break
            registerStorage[binToDec(int(registerValue(lst[i][1])))] = registerStorage[
                                                                           binToDec(int(registerValue(lst[i][2])))] - \
                                                                       registerStorage[
                                                                           binToDec(int(registerValue(lst[i][3])))]
            temp = registerStorage[binToDec(int(registerValue(lst[i][1])))]
            if (temp >= (2 ** 7) or temp < -(2 ** 7)):
                ans.append("0000000000001000")
                break
            p = 'subtraction'
            ans.append(
                bin(int(return_key(p)), 5) + "00" + registerValue(lst[i][1]) + registerValue(lst[i][2]) + registerValue(
                    lst[i][3]))
            if (registerStorage[binToDec(int(registerValue(lst[i][1])))] < 0):
                # This will set the flag since because of the subtraction the value stored in the destination
                # register is now negative
                registerStorage[7] = 8
                registerStorage[binToDec(int(registerValue(lst[i][1])))] = 0
            else:
                registerStorage[7] = 0
            programCounter = programCounter + 1
            Simulator(programCounter, 0)
        elif lst[i][0] == 'mul':
            if (len(lst[i]) != 4):
                SyntaxError(i)
                break
            registerStorage[binToDec(int(registerValue(lst[i][1])))] = registerStorage[
                                                                           binToDec(int(registerValue(lst[i][2])))] * \
                                                                       registerStorage[
                                                                           binToDec(int(registerValue(lst[i][3])))]
            temp = registerStorage[binToDec(int(registerValue(lst[i][1])))]
            if (temp >= (2 ** 7) or temp < -(2 ** 7)):
                ans.append("0000000000001000")
                break
            p = 'multiply'
            ans.append(
                bin(int(return_key(p)), 5) + "00" + registerValue(lst[i][1]) + registerValue(lst[i][2]) + registerValue(
                    lst[i][3]))
            if (registerStorage[binToDec(int(registerValue(lst[i][1])))] > 2 ** 16 - 1):
                # This will set the flag since because of the multiplication the value stored in the destination
                # register is now greater than the permissible value of 2^16-1
                registerStorage[7] = 8
                registerStorage[binToDec(int(registerValue(lst[i][1])))] = 2 ** 16 - 1
            else:
                registerStorage[7] = 0
            programCounter = programCounter + 1
            Simulator(programCounter, 0)
        elif lst[i][0] == 'div':
            # General Syntax Error for any no. != 0
            # second register should not be zero, R0 and R1 should not be initialised, quotient in R0 and remainder in R1
            if (len(lst[i]) != 3):
                SyntaxError(i)
                break
            if lst[i][1] == 'R1' or lst[i][1] == 'R0' or lst[i][2] == 'R1' or lst[i][2] == 'R0':
                RegisterError(i)
                break
            elif registerStorage[binToDec(int(registerValue(lst[i][2])))] == 0:
                print("Zero Division Error")
                break
            registerStorage[0] = binToDec(int(registerValue(lst[i][1]))) // binToDec(int(registerValue(lst[i][2])))
            registerStorage[1] = binToDec(int(registerValue(lst[i][1]))) % binToDec(int(registerValue(lst[i][2])))
            p = 'divide'
            ans.append(bin(int(return_key(p)), 5) + "00000" + registerValue(lst[i][1]) + registerValue(lst[i][2]))
            programCounter = programCounter + 1
            Simulator(programCounter, 0)
        elif lst[i][0] == 'rs':
            if (len(lst[i]) != 3):
                SyntaxError(i)
                break
            p = 'rightshift'
            lst[i][2] = int(lst[i][2][1:])
            if lst[i][2] < 0 or lst[i][2] > 255:
                ImmediateValueError(i)
                break
            x = binToDec(int(registerValue(lst[i][1])))
            registerStorage[x] = registerStorage[x] >> lst[i][2]
            ans.append(bin(int(return_key(p)), 5) + registerValue(lst[i][1]) + bin(int(lst[i][2]), 8))
            programCounter = programCounter + 1
            Simulator(programCounter, 0)
        elif lst[i][0] == 'ls':
            if (len(lst[i]) != 3):
                SyntaxError(i)
                break
            p = 'leftshift'
            lst[i][2] = int(lst[i][2][1:])
            if lst[i][2] < 0 or lst[i][2] > 255:
                ImmediateValueError(i)
                break
            x = binToDec(int(registerValue(lst[i][1])))
            registerStorage[x] = registerStorage[x] << lst[i][2]
            ans.append(bin(int(return_key(p)), 5) + registerValue(lst[i][1]) + bin(int(lst[i][2]), 8))
            programCounter = programCounter + 1
            Simulator(programCounter, 0)
        elif lst[i][0] == 'xor':
            if (len(lst[i]) != 4):
                SyntaxError(i)
                break
            registerStorage[int(binToDec(int(registerValue(lst[i][1]))))] = registerStorage[int(binToDec(
                int(registerValue(lst[i][2]))))] ^ registerStorage[int(binToDec(int(registerValue(lst[i][3]))))]
            p = 'exclusiveor'
            ans.append(
                bin(int(return_key(p)), 5) + "00" + registerValue(lst[i][1]) + registerValue(lst[i][2]) + registerValue(
                    lst[i][3]))
            programCounter = programCounter + 1
            Simulator(programCounter, 0)
        elif lst[i][0] == 'or':
            if (len(lst[i]) != 4):
                SyntaxError(i)
                break
            registerStorage[int(binToDec(int(registerValue(lst[i][1]))))] = registerStorage[int(binToDec(
                int(registerValue(lst[i][2]))))] + registerStorage[int(binToDec(int(registerValue(lst[i][3]))))]
            p = 'or'
            ans.append(
                bin(int(return_key(p)), 5) + "00" + registerValue(lst[i][1]) + registerValue(lst[i][2]) + registerValue(
                    lst[i][3]))
            programCounter = programCounter + 1
            Simulator(programCounter, 0)
        elif lst[i][0] == 'and':
            if (len(lst[i]) != 4):
                SyntaxError(i)
                break
            registerStorage[int(binToDec(int(registerValue(lst[i][1]))))] = registerStorage[int(binToDec(
                int(registerValue(lst[i][2]))))] & registerStorage[int(binToDec(int(registerValue(lst[i][3]))))]
            p = 'and'
            ans.append(
                bin(int(return_key(p)), 5) + "00" + registerValue(lst[i][1]) + registerValue(lst[i][2]) + registerValue(
                    lst[i][3]))
            programCounter = programCounter + 1
            Simulator(programCounter, 0)
        elif lst[i][0] == 'not':
            if (len(lst[i]) != 3):
                SyntaxError(i)
                break
            p = 'invert'
            registerStorage[int(binToDec(int(registerValue(lst[i][1]))))] = NOT(
                str(bin(registerStorage[binToDec(int(registerValue(lst[i][2])))])))
            ans.append(bin(int(return_key("")), 5) + "00000" + registerValue(lst[i][1]) + registerValue(lst[i][2]))
            programCounter = programCounter + 1
            Simulator(programCounter, 0)
        elif lst[i][0] == 'cmp':
            flag = 0
            if (len(lst[i]) != 3):
                SyntaxError(i)
                break
            if registerStorage[binToDec(int(registerValue(lst[i][1])))] > registerStorage[
                binToDec(int(registerValue(lst[i][2])))]:
                flag = 2
            elif registerStorage[binToDec(int(registerValue(lst[i][1])))] < registerStorage[
                binToDec(int(registerValue(lst[i][2])))]:
                flag = 4
            elif registerStorage[binToDec(int(registerValue(lst[i][1])))] == registerStorage[
                binToDec(int(registerValue(lst[i][2])))]:
                flag = 1
            ans.append(
                bin(int(return_key('compare')), 5) + "00000" + registerValue(lst[i][1]) + registerValue(lst[i][2]))
            programCounter = programCounter + 1
            Simulator(programCounter, flag)
        elif lst[i][0] == 'jmp':
            if (len(lst[i]) != 2):
                SyntaxError(i)
                break
            x = label[lst[i][1]]
            # lst[i][1] is the label to which we have to jump to
            p = 'unconditionaljump'
            #i = binToDec(int(lst[i][1]))
            ans.append(bin(int(return_key(p)), 5) + "000" + bin(int(x), 8))
            programCounter = programCounter + 1
            Simulator(programCounter, 0)
            function(x, programCounter)
        elif lst[i][0] == 'jlt':
            if (len(lst[i]) != 2):
                SyntaxError(i)
                break
            p = "jumpiflessthan"
            x = label[lst[i][1]]
            ans.append(bin(int(return_key(p)), 5) + "000" + bin(int(x),8))
            programCounter = programCounter + 1
            Simulator(programCounter, 0)
            if(flag==4):
                x = label[lst[i][1]]
                function(x, programCounter)
        elif lst[i][0] == 'jgt':
            if (len(lst[i]) != 2):
                SyntaxError(i)
                break
            p = "jumpifgreaterthan"
            x = label[lst[i][1]]
            ans.append(bin(int(return_key(p)), 5) + "000" + bin(int(x),8))
            programCounter = programCounter + 1
            Simulator(programCounter, 0)
            if(flag==2):
                function(x, programCounter)
        elif lst[i][0] == 'je':
            if len(lst[i]) != 2:
                SyntaxError(i)
                break
            p = 'jumpifequal'
            x = label[lst[i][1]]
            ans.append(bin(int(return_key(p)), 5) + "000" + bin(int(x),8))
            programCounter = programCounter + 1
            Simulator(programCounter, 0)
            if(flag==1):
                function(x, programCounter)
        elif lst[i][0] == 'st':
            if binToDec(int(registerValue(lst[i][1]))) == 7:
                FlagError(i)
                break
            if (len(lst[i]) != 3):
                SyntaxError(i)
                break
            variables = var.keys()
            p = 'store'
            if (lst[i][2] in variables):
                var[lst[i][2]] = registerStorage[binToDec(int(registerValue(lst[i][1])))]
            else:
                SyntaxError(i)
            ans.append(bin(int(return_key(p)), 5) + registerValue(lst[i][1]) + bin(i + 1, 8))
            programCounter = programCounter + 1
            Simulator(programCounter, 0)
        elif lst[i][0] == 'ld':
            if binToDec(int(registerValue(lst[i][1]))) == 7:
                FlagError(i)
                break;
            if (len(lst[i]) != 3):
                SyntaxError(i)
                break
            variables = var.keys()
            p = 'load'
            if (lst[i][2] in variables):
                registerStorage[binToDec(int(registerValue(lst[i][1])))] = var[lst[i][2]]
            else:
                SyntaxError(i)
            ans.append(bin(int(return_key(p)), 5) + registerValue(lst[i][1]) + bin(i + 1, 8))
            programCounter = programCounter + 1
            Simulator(programCounter, 0)
        elif lst[i][0] == 'var':# and run == True:
            if (len(lst[i]) != 2):
                SyntaxError(i)
                break
            if i != 0 and lst[i - 1][0] != 'var':
                WrongVariableDeclaration(i)
                break
            if not checkName(lst[i][1]):
                UndefinedVariables(i)
                break
            else:
                if var.values() == lst[i][1]:
                    WrongVariableDeclaration(i)
                    break
                var[lst[i][1]] = 0
        elif lst[i][0] == 'hlt':
            ans.append(bin(int(return_key('halt')), 5) + "00000000000")
            programCounter = programCounter + 1
            Simulator(programCounter, 0)
            break
        else:
            SyntaxError(i)
            break
elif count == 0:
    MissingHlt(len(lst))
else:
    HltNotLast(i)

for i in sim:
    print(i)

for i in ans:
    print(i)
