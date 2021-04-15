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


def binaryToNumber(input, type):
    '''
    Converts a given 16-bit binary string
    to correct decimal value according to the type
    '''
    outDecimal = 0
    if type == Type.UNSIGNED:
        for i in range(0, len(input)):
            if input[i] == '1':
                outDecimal = outDecimal + pow(2, 16 - (i + 1))
    elif type == Type.SIGNED:
        if input[0] == '1':
            binaryAbsolute = twosComplement(input)
            outDecimal = binaryToNumber(binaryAbsolute, Type.UNSIGNED) * -1
        else:
            outDecimal = binaryToNumber(input, Type.UNSIGNED)
    else:
        raise NotImplementedError("Number type was wrong or not implemented.")
    return outDecimal


def numberToBinary(input, type, padding=True):
    '''
    Converts a given string, representing a decimal number
    to correct binary value according to the type 
    '''
    outBits = ''
    if type == Type.UNSIGNED:
        number = int(input[:-1] if input[-1] == 'u' else input)
        while number > 0:
            if number % 2 == 0:
                outBits = '0' + outBits
            else:
                outBits = '1' + outBits
            number = int(number / 2)
        # Padding
        while padding and len(outBits) < 16:
            outBits = '0' + outBits
    elif type == Type.SIGNED:
        number = int(input)
        magnitude = numberToBinary((input[1:] if input[0] == '-' else input), Type.UNSIGNED)
        outBits = twosComplement(magnitude)
    else:
        number = float(input)
        if number < 0:
            outBits += '1'
        else:
            outBits += '0'
        number = abs(number)
        wholePart = int(number)
        fractionPart = number - wholePart
        wholeBinary = numberToBinary(str(wholePart), Type.UNSIGNED, False)
        fractionBinary = ""
        result = fractionPart
        while result != 1: # TODO: FIX INFINITE LOOP!
            result = result * 2
            if result < 1.0:
                fractionBinary += "0"
            else:
                fractionBinary += "1"
                if result == 1:
                    break
                result = result - int(result)
        print(wholeBinary)
        print(fractionBinary)
    return outBits


def twosComplement(binary):
    outstr = ''
    for c in binary:
        if c == '0':
            outstr += '1'
        else:
            outstr += '0'
    number = binaryToNumber(outstr, Type.UNSIGNED)
    number += 1
    outstr = numberToBinary(str(number), Type.UNSIGNED)
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
    return int(floating_size)


def getTypeOfInput(line):
    '''
    For a single input line determine
    whether if the number is unsigned or
    floating point number etc.
    Returns the type as a Type enum
    '''
    if 'u' in line:  # Number is unsigned
        return Type.UNSIGNED
    elif '.' in line:  # Number is floating point
        return Type.FLOATING
    elif '-' in line:  # Number is negative signed
        return Type.SIGNED
    else:  # Number is positive signed
        return Type.SIGNED


def getNumberOfExponentBits(floating_size):
    '''
    Returns the number of exponent bits
    based on the floating point size
    '''
    if floating_size == 1:
        return 3
    elif floating_size == 2:
        return 8
    elif floating_size == 3:
        return 10
    else:
        return 12


def main():
    print('Byte ordering: ', end='')
    ordering = str(input())
    if ordering not in possible_orderings:
        print('Invalid byte ordering! ')
        exit(0)

    print('Floating point size: ', end='')
    floating_size_text = str(input())  # '2 bytes'
    floating_size = getFloatingSize(floating_size_text)  # int: 2

    if floating_size not in [1, 2, 3, 4]:
        print('Floating point size is not valid')
        exit(-1)

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

    assert set(output) == set(correctoutput), "Output was:\n" + str(output) + "\nShould be:\n" + str(
        correctoutput) + "."
    # End test


if __name__ == "__main__":
    main()
