from enum import Enum
class Type(Enum):
    UNSIGNED = 0
    SIGNED = 1
    FLOATING = 2

LITTLE_ENDIAN = 'Little Endian'
BIG_ENDIAN = 'Big Endian'

possible_orderings = [LITTLE_ENDIAN, BIG_ENDIAN]


def readInputFile():
    file = open('./input.txt', 'r')
    lines = file.readlines()
    return list(map(lambda l: l.strip(), lines))

def numberToBinary(input, type):
    '''
    Converts a given string, representing a number
    to correct binary value according to the type 
    '''
    outBits = ''
    if type == Type.UNSIGNED:
        number = int(input[:-1])
        while number > 0:
            if number % 2 == 0:
                outBits = '0' + outBits
            else:
                outBits = '1' + outBits
            number = int(number / 2)
        # Padding
        while len(outBits) < 16:
            outBits = '0' + outBits
    elif type == Type.SIGNED:
        number = int(input)
        magnitude = numberToBinary((input[1:] if input[0] == '-' else input) + 'u', Type.UNSIGNED)
        outBits = twosComplement(magnitude)
    else:
        raise NotImplementedError("Number type was wrong or not implemented.")
    return outBits

def twosComplement(binary):
    outstr = ''
    for c in binary:
        if c == '0':
            outstr += '1'
        else:
            outstr += '0'
    number = int(outstr, 2)
    number += 1
    outstr = numberToBinary(str(number) + 'u', Type.UNSIGNED)
    return outstr


def handleFloatingPoint(floatingNumber):
    pass

def getFloatingSize(floatingSizeText):
    '''
    Converts raw input string '2 bytes'
    to number '2'
    '''
    floating_size_list = floatingSizeText.split(' ')
    floating_size = floating_size_list[0]
    return floating_size


def getTypeOfInput(line):
    '''
    For a single input line determine
    whether if the number is unsigned or 
    floating point number etc.
    Returns the type as a Type enum
    '''
    if 'u' in line:     # Number is unsigned
        return Type.UNSIGNED
    elif '-' in line:   # Number is negative signed
        return Type.SIGNED
    elif '.' in line:   # Number is floating point
        return Type.FLOATING
    else:               # Number is positive signed
        return Type.SIGNED

def main():
    print('Byte ordering: ', end='')
    ordering = str(input())
    if ordering not in possible_orderings:
        print('Invalid byte ordering! ')
        exit(0)

    print('Floating point size: ', end='')
	# C:TODO Validate input?
    floating_size_text = str(input())  # '2 bytes'
    floating_size = getFloatingSize(floating_size_text)  # int: 2

    lines = readInputFile()
    output = []
    print('lines is ', lines)
    for line in lines:
        output.append(numberToBinary(line, getTypeOfInput(line)))
    
    # Start test
    outputfile = open('./sample-output.txt', 'r')
    correctoutput = outputfile.readlines()
    correctoutput = list(map(lambda l: l.strip(), correctoutput))
    outputfile.close()

    assert set(output) == set(correctoutput), "Output was:\n" + str(output) + "\nShould be:\n" + str(correctoutput) + "."
    # End test


if __name__ == "__main__":
    main()
