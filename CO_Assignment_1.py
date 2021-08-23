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

##################################################Above this nothing was changed
'''
The register only supports whole numbers so all operations leading to negative will be set to 0 and overflow will be actiavted.

'''
sim = []
programCounter = -1
while(True):
    inst = input();
    if(inst=="hlt"):
        break
    elif(inst==" "):
        continue
    else:
        lst.append(inst.split(" "))


for i in range(len(lst)):



    if lst[i][0] == 'mov':
        if (len(lst[i]) != 3):
            print("Wrong syntax used for instructions")
            break
        if lst[i][2][0] == 'R':
            p = 'moveregister'
            registerStorage[binToDec(int(registerValue(lst[i][1])))] = registerStorage[binToDec(int(registerValue(lst[i][2])))]
            ans.append(bin(int(return_key(p)), 5) + "00000" + registerValue(lst[i][1]) + registerValue(lst[i][2]))
        else:
            p = 'moveimmediate'
            if lst[i][2][1] < 0 or lst[i][2][1] > 255:
                print("Illegal Immediate Value")
                break
            if lst[i][2][0] == '$':
                lst[i][2] = lst[i][2][1:]
                registerStorage[int(lst[i][1][1])] = int(lst[i][2])
                ans.append(bin(int(return_key(p)), 5) + registerValue(lst[i][1]) + bin(int(lst[i][2]), 8))
##########################################
        aux = []
        programCounter = programCounter+1
        toAdd = bin(programCounter,8)
        aux.append(str(toAdd))
        registerStorage[7] = 0
        for i in registerStorage:
            aux.append(bin(i, 16))
        sim.append(aux[0]+ " " + aux[1] + " " + aux[2] + " " + aux[3] + " " +aux[4] + " " + aux[5] + " "+ aux[6] + " " + aux[7] + " " + aux[8] )
##########################################

    elif lst[i][0] == 'add':
        if(len(lst[i]) != 4):
            print("Wrong syntax used for instructions")
            break
        registerStorage[binToDec(int(registerValue(lst[i][1])))] = registerStorage[binToDec(int(registerValue(lst[i][2])))] + registerStorage[binToDec(int(registerValue(lst[i][3])))]
        temp = registerStorage[binToDec(int(registerValue(lst[i][1])))]
        if(temp >= (2 ** 7) or temp < -(2 ** 7)):
            ans.append("0000000000001000" )
            break
        p = 'addition'
        ans.append(bin(int(return_key(p)), 5) + "00" + registerValue(lst[i][1]) + registerValue(lst[i][2]) + registerValue(lst[i][3]))
##########################################
        if(registerStorage[binToDec(int(registerValue(lst[i][1])))]  > 2**16-1):
            #This will set the flag since because of the addition the value stored in the destination
            # register is now greater than the permissible value of 2^16-1
            registerStorage[7] = 8
            registerStorage[binToDec(int(registerValue(lst[i][1])))] = 2**16-1
        else:
            registerStorage[7] = 0

        aux = []
        programCounter = programCounter+1
        toAdd = bin(programCounter,8)
        aux.append(str(toAdd))
        for i in registerStorage:
            aux.append(bin(i, 16))
        sim.append(aux[0]+ " " + aux[1] + " " + aux[2] + " " + aux[3] + " " +aux[4] + " " + aux[5] + " "+ aux[6] + " " + aux[7] + " " + aux[8] )
#############################################

    elif lst[i][0] == 'sub':
        if (len(lst[i]) != 4):
            print("Wrong syntax used for instructions")
            break
        registerStorage[binToDec(int(registerValue(lst[i][1])))] = registerStorage[binToDec(int(registerValue(lst[i][2])))] - registerStorage[binToDec(int(registerValue(lst[i][3])))]
        temp = registerStorage[binToDec(int(registerValue(lst[i][1])))]
        if (temp >= (2 ** 7) or temp < -(2 ** 7)):
            ans.append("0000000000001000" )
            break
        p = 'subtraction'
        ans.append(bin(int(return_key(p)), 5) + "00" + registerValue(lst[i][1]) + registerValue(lst[i][2]) + registerValue(lst[i][3]))
##########################################
        if (registerStorage[binToDec(int(registerValue(lst[i][1])))] < 0):
            # This will set the flag since because of the subtraction the value stored in the destination
            # register is now negative
            registerStorage[7] = 8
            registerStorage[binToDec(int(registerValue(lst[i][1])))] = 0
        else:
            registerStorage[7] = 0

        aux = []
        programCounter = programCounter+1
        toAdd = bin(programCounter,8)
        aux.append(str(toAdd))
        for i in registerStorage:
            aux.append(bin(i, 16))
        sim.append(aux[0]+ " " + aux[1] + " " + aux[2] + " " + aux[3] + " " +aux[4] + " " + aux[5] + " "+ aux[6] + " " + aux[7] + " " + aux[8] )
##########################################

    elif lst[i][0] == 'mul':
        if (len(lst[i]) != 4):
            print("Wrong syntax used for instructions")
            break
        registerStorage[binToDec(int(registerValue(lst[i][1])))] = registerStorage[binToDec(int(registerValue(lst[i][2])))] * registerStorage[binToDec(int(registerValue(lst[i][3])))]
        temp = registerStorage[binToDec(int(registerValue(lst[i][1])))]
        if (temp >= (2 ** 7) or temp < -(2 ** 7)):
            ans.append("0000000000001000" )
            break
        p = 'multiply'
        ans.append(bin(int(return_key(p)), 5) + "00" + registerValue(lst[i][1]) + registerValue(lst[i][2]) + registerValue(lst[i][3]))
##########################################
        if (registerStorage[binToDec(int(registerValue(lst[i][1])))] > 2**16-1):
            # This will set the flag since because of the multiplication the value stored in the destination
            # register is now greater than the permissible value of 2^16-1
            registerStorage[7] = 8
            registerStorage[binToDec(int(registerValue(lst[i][1])))] = 2**16-1
        else:
            registerStorage[7] = 0

        aux = []
        programCounter = programCounter+1
        toAdd = bin(programCounter,8)
        aux.append(str(toAdd))
        for i in registerStorage:
            aux.append(bin(i, 16))
        sim.append(aux[0]+ " " + aux[1] + " " + aux[2] + " " + aux[3] + " " +aux[4] + " " + aux[5] + " "+ aux[6] + " " + aux[7] + " " + aux[8] )
##########################################

    elif lst[i][0] == 'div':
        # General Syntax Error for any no. != 0
        # second register should not be zero, R0 and R1 should not be initialised, quotient in R0 and remainder in R1
        if (len(lst[i]) != 3):
            print("Wrong syntax used for instructions")
            break
        if lst[i][1] == 'R1' or lst[i][1] == 'R0' or lst[i][2] == 'R1' or lst[i][2] == 'R0':
            print("Wrong syntax used for instructions")
            break
        elif int(lst[i][2]) == 0:
            print("Zero Division Error")
            break
        registerStorage[0] = binToDec(int(registerValue(lst[i][1]))) // binToDec(int(registerValue(lst[i][2])))
        registerStorage[1] = binToDec(int(registerValue(lst[i][1]))) % binToDec(int(registerValue(lst[i][2])))
        p = 'divide'
        ans.append(bin(int(return_key(p)), 5) + "00000" + registerValue(lst[i][1]) + registerValue(lst[i][2]))
##########################################
        aux = []
        programCounter = programCounter+1
        toAdd = bin(programCounter,8)
        aux.append(str(toAdd))
        registerStorage[7] = 0
        for i in registerStorage:
            aux.append(bin(i, 16))
        sim.append(aux[0]+ " " + aux[1] + " " + aux[2] + " " + aux[3] + " " +aux[4] + " " + aux[5] + " "+ aux[6] + " " + aux[7] + " " + aux[8] )
##########################################

    elif lst[i][0] == 'rs':
        if (len(lst[i]) != 3):
            print("Wrong syntax used for instructions")
            break
        p = 'rightshift'
        lst[i][2] = lst[i][2][1:]
        if lst[i][2]<0 or lst[i][2]>255:
            print("Illegal Immediate Value")
            break
        registerStorage[binToDec(int(registerValue(lst[i][1])))] //= int(lst[i][2])
        ans.append(bin(int(return_key(p)), 5) + registerValue(lst[i][1]) + bin(int(lst[i][2]), 8))
##########################################
        aux = []
        programCounter = programCounter+1
        toAdd = bin(programCounter,8)
        aux.append(str(toAdd))
        registerStorage[7] = 0
        for i in registerStorage:
            aux.append(bin(i, 16))
        sim.append(aux[0]+ " " + aux[1] + " " + aux[2] + " " + aux[3] + " " +aux[4] + " " + aux[5] + " "+ aux[6] + " " + aux[7] + " " + aux[8] )
##########################################

    elif lst[i][0] == 'ls':
        if (len(lst[i]) != 3):
            print("Wrong syntax used for instructions")
            break
        p = 'leftshift'
        lst[i][2] = lst[i][2][1:]
        if lst[i][2] <0 or lst[i][2]>255:
            print("Illegal Immediate Value")
            break
        registerStorage[binToDec(int(registerValue(lst[i][1])))] *= int(lst[i][2])
        ans.append(bin(int(return_key(p)), 5) + registerValue(lst[i][1]) + bin(int(lst[i][2]), 8))
##########################################
        aux = []
        programCounter = programCounter+1
        toAdd = bin(programCounter,8)
        aux.append(str(toAdd))
        registerStorage[7] = 0
        for i in registerStorage:
            aux.append(bin(i, 16))
        sim.append(aux[0]+ " " + aux[1] + " " + aux[2] + " " + aux[3] + " " +aux[4] + " " + aux[5] + " "+ aux[6] + " " + aux[7] + " " + aux[8] )
##########################################

    elif lst[i][0] == 'xor':
        if (len(lst[i]) != 4):
            print("Wrong syntax used for instructions")
            break
        registerStorage[int(binToDec(registerValue(lst[i][1])))] = registerStorage[int(binToDec(registerValue(lst[i][2])))] ^ registerStorage[int(binToDec(registerValue(lst[i][3])))]
        p = 'exclusiveor'
        ans.append(bin(int(return_key(p)), 5) + "00" + registerValue(lst[i][1]) + registerValue(lst[i][2]) + registerValue(lst[i][3]))
##########################################
        aux = []
        programCounter = programCounter+1
        toAdd = bin(programCounter,8)
        aux.append(str(toAdd))
        registerStorage[7] = 0
        for i in registerStorage:
            aux.append(bin(i, 16))
        sim.append(aux[0]+ " " + aux[1] + " " + aux[2] + " " + aux[3] + " " +aux[4] + " " + aux[5] + " "+ aux[6] + " " + aux[7] + " " + aux[8] )
##########################################

    elif lst[i][0] == 'or':
        if (len(lst[i]) != 4):
            print("Wrong syntax used for instructions")
            break
        registerStorage[int(binToDec(registerValue(lst[i][1])))] = registerStorage[int(binToDec(registerValue(lst[i][2])))] | registerStorage[int(binToDec(registerValue(lst[i][3])))]
        p = 'or'
        ans.append(bin(int(return_key(p)), 5) + "00" + registerValue(lst[i][1]) + registerValue(lst[i][2]) + registerValue(lst[i][3]))
##########################################
        aux = []
        programCounter = programCounter+1
        toAdd = bin(programCounter,8)
        aux.append(str(toAdd))
        registerStorage[7] = 0
        for i in registerStorage:
            aux.append(bin(i, 16))
        sim.append(aux[0]+ " " + aux[1] + " " + aux[2] + " " + aux[3] + " " +aux[4] + " " + aux[5] + " "+ aux[6] + " " + aux[7] + " " + aux[8] )
##########################################

    elif lst[i][0] == 'and':
        if (len(lst[i]) != 4):
            print("Wrong syntax used for instructions")
            break
        registerStorage[int(binToDec(registerValue(lst[i][1])))] = registerStorage[int(binToDec(registerValue(lst[i][2])))] & registerStorage[int(binToDec(registerValue(lst[i][3])))]
        p = 'and'
        ans.append(bin(int(return_key(p)), 5) + "00" + registerValue(lst[i][1]) + registerValue(lst[i][2]) + registerValue(lst[i][3]))
##########################################
        aux = []
        programCounter = programCounter+1
        toAdd = bin(programCounter,8)
        aux.append(str(toAdd))
        registerStorage[7] = 0
        for i in registerStorage:
            aux.append(bin(i, 16))
        sim.append(aux[0]+ " " + aux[1] + " " + aux[2] + " " + aux[3] + " " +aux[4] + " " + aux[5] + " "+ aux[6] + " " + aux[7] + " " + aux[8] )
##########################################

    elif lst[i][0] == 'not':
        if (len(lst[i]) != 3):
            print("Wrong syntax used for instructions")
            break
        p = 'invert'
        registerStorage[int(binToDec(registerValue(lst[i][1])))] = NOT(str(registerStorage[int(binToDec(registerValue(lst[i][2])))]))
        ans.apoend(bin(int(return_key(p)), 5) + "00000" + registerValue(lst[i][1]) + registerValue(lst[i][2]))
##########################################
        aux = []
        programCounter = programCounter+1
        toAdd = bin(programCounter,8)
        aux.append(str(toAdd))
        registerStorage[7] = 0
        for i in registerStorage:
            aux.append(bin(i, 16))
        sim.append(aux[0]+ " " + aux[1] + " " + aux[2] + " " + aux[3] + " " +aux[4] + " " + aux[5] + " "+ aux[6] + " " + aux[7] + " " + aux[8] )
##########################################

    elif lst[i][0] == 'cmp':
        if (len(lst[i]) != 3):
            print("Wrong syntax used for instructions")
            break

##########################################
        if registerStorage[binToDec(int(registerValue(lst[i][1])))] > registerStorage[binToDec(int(registerValue(lst[i][2])))]:
            registerStorage[7] = 2
        elif registerStorage[binToDec(int(registerValue(lst[i][1])))] < registerStorage[binToDec(int(registerValue(lst[i][2])))]:
            registerStorage[7] = 4
        elif registerStorage[binToDec(int(registerValue(lst[i][1])))] == registerStorage[binToDec(int(registerValue(lst[i][2])))]:
            registerStorage[7] = 1

        aux = []
        programCounter = programCounter+1
        toAdd = bin(programCounter,8)
        aux.append(str(toAdd))
        for i in registerStorage:
            aux.append(bin(i, 16))
        sim.append(aux[0]+ " " + aux[1] + " " + aux[2] + " " + aux[3] + " " +aux[4] + " " + aux[5] + " "+ aux[6] + " " + aux[7] + " " + aux[8] )

 ##########################################

    elif lst[i][0] == 'jmp':
        if (len(lst[i]) != 2):
            print("Wrong syntax used for instructions")
            break
        p = 'unconditionaljump'
        i = binToDec(int(lst[i][1]))
        ans.append(bin(int(return_key(p)), 5) + "000" + lst[i][1])

##########################################
        aux = []
        programCounter = programCounter + 1
        toAdd = bin(programCounter, 8)
        aux.append(str(toAdd))
        registerStorage[7] = 0
        for i in registerStorage:
            aux.append(bin(i, 16))
        sim.append(
            aux[0] + " " + aux[1] + " " + aux[2] + " " + aux[3] + " " + aux[4] + " " + aux[5] + " " + aux[6] + " " +
            aux[7] + " " + aux[8])
##########################################

    elif lst[i][0] == 'jlt':
        if (len(lst[i]) != 2):
            print("Wrong syntax used for instructions")
            break
        p = "jumpiflessthan"
        for j in flag:
            if j == "0000000000000100":
                i = binToDec(int(lst[i][1]))
        ans.append(bin(int(return_key(p)), 5) + "000" + lst[i][1])

##########################################
        aux = []
        programCounter = programCounter + 1
        toAdd = bin(programCounter, 8)
        aux.append(str(toAdd))
        registerStorage[7] = 0
        for i in registerStorage:
            aux.append(bin(i, 16))
        sim.append(
            aux[0] + " " + aux[1] + " " + aux[2] + " " + aux[3] + " " + aux[4] + " " + aux[5] + " " + aux[6] + " " +
            aux[7] + " " + aux[8])
##########################################

    elif lst[i][0] == 'jgt':
        if (len(lst[i]) != 2):
            print("Wrong syntax used for instructions")
            break
        p = "jumpifgreaterthan"
        for j in flag:
            if j == "0000000000000010":
                i = binToDec(int(lst[i][1]))
        ans.append(bin(int(return_key(p)), 5) + "000" + lst[i][1])

##########################################
        aux = []
        programCounter = programCounter + 1
        toAdd = bin(programCounter, 8)
        aux.append(str(toAdd))
        registerStorage[7] = 0
        for i in registerStorage:
            aux.append(bin(i, 16))
        sim.append(
            aux[0] + " " + aux[1] + " " + aux[2] + " " + aux[3] + " " + aux[4] + " " + aux[5] + " " + aux[6] + " " +
            aux[7] + " " + aux[8])
##########################################

    elif lst[i][0] == 'je':
        if (len(lst[i]) != 2):
            print("Wrong syntax used for instructions")
            break
        p = 'jumpifequal'
        for j in flag:
            if j == "0000000000000001":
                i = binToDec(int(lst[i][1]))
        ans.append(bin(int(return_key(p)), 5) + "000" + lst[i][1])

##########################################
        aux = []
        programCounter = programCounter + 1
        toAdd = bin(programCounter, 8)
        aux.append(str(toAdd))
        registerStorage[7] = 0
        for i in registerStorage:
            aux.append(bin(i, 16))
        sim.append(
            aux[0] + " " + aux[1] + " " + aux[2] + " " + aux[3] + " " + aux[4] + " " + aux[5] + " " + aux[6] + " " +
            aux[7] + " " + aux[8])
##########################################

    elif lst[i][0] == 'st':
        if (len(lst[i]) != 3):
            print("General Syntax Error")
            break
        p = 'store'
        var[lst[i][2]] = registerStorage[binToDec(int(registerValue(lst[i][1])))]
        ans.append(bin(int(return_key(p)), 5) + registerValue(lst[i][1]) + bin(i + 1, 8))

##########################################
        aux = []
        programCounter = programCounter + 1
        toAdd = bin(programCounter, 8)
        aux.append(str(toAdd))
        registerStorage[7] = 0
        for i in registerStorage:
            aux.append(bin(i, 16))
        sim.append(
            aux[0] + " " + aux[1] + " " + aux[2] + " " + aux[3] + " " + aux[4] + " " + aux[5] + " " + aux[6] + " " +
            aux[7] + " " + aux[8])
##########################################


    elif lst[i][0] == 'ld':
        if (len(lst[i]) != 3):
            print("General Syntax Error")
            break
        p = 'load'
        registerStorage[binToDec(int(registerValue(lst[i][1])))] = registerStorage[binToDec(int(registerValue(lst[binToDec(int(lst[i][2]))][1])))]
        ans.append(bin(int(return_key(p)), 5) + registerValue(lst[i][1]) + lst[i][2])

##########################################
        aux = []
        programCounter = programCounter + 1
        toAdd = bin(programCounter, 8)
        aux.append(str(toAdd))
        registerStorage[7] = 0
        for i in registerStorage:
            aux.append(bin(i, 16))
        sim.append(
            aux[0] + " " + aux[1] + " " + aux[2] + " " + aux[3] + " " + aux[4] + " " + aux[5] + " " + aux[6] + " " +
            aux[7] + " " + aux[8])
##########################################

    elif lst[i][0] == 'var':
        if (len(lst[i]) != 2):
            print("Wrong syntax used for instructions")
            break
        if i != 0 and lst[i-1][0] != 'var':
            print("Variables not declared at the beginning")
            break
        if not checkName(lst[i][1]):
            print("Use of undefined variables")
            break
        else:
            if var.values() == lst[i][1]:
                print("Multiple Names for the same Variable")
                break
            var[lst[i][1]] = 0

    elif lst[i][0] == 'hlt':
        ans.append(bin(int(return_key('halt')), 5) + "00000000000")
        break



    else:
        print("Typos in instruction name or register name")
        break

for i in ans:
    print(i)

for i in sim:
    print(i)
