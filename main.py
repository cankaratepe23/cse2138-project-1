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


def roundUp(mantissa):
    newMantissa = ''
    lastIndexCopied = len(mantissa)
    for i in reversed(range(len(mantissa))):
        lastIndexCopied = i
        if mantissa[i] == '1':
            newMantissa += '0'
        elif mantissa[i] == '0':
            newMantissa += '1'
            break
    return mantissa[:lastIndexCopied] + newMantissa[::-1]


def handleFractionLength(mantissa, fractionLength):
    if fractionLength > len(mantissa):
        while fractionLength > len(mantissa):
            mantissa += '0'
        return mantissa

    remainingBitsIndex = fractionLength - len(mantissa)
    remainingBits = mantissa[remainingBitsIndex:]
    newMantissa = mantissa[:remainingBitsIndex]
    if remainingBits[0] == '1' and remainingBits[1:].find('1') != -1:
        newMantissa = roundUp(newMantissa)
    return newMantissa


def shiftFloatingPoint(mantissa, E):
    currentIndex = mantissa.find('.')
    mantissa = mantissa.replace('.', '')
    newIndex = 0
    if E <= 0:
        newIndex = currentIndex + abs(E)
    else:
        newIndex = currentIndex - abs(E)

    return mantissa[:newIndex] + "." + mantissa[newIndex:]


def numberToBinary(input, type, floating_size=4, padding=16):
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
        while padding > 0 and len(outBits) < padding:
            outBits = '0' + outBits
    elif type == Type.SIGNED:
        number = int(input)
        magnitude = numberToBinary((input[1:] if input[0] == '-' else input), Type.UNSIGNED, padding=padding)
        outBits = twosComplement(magnitude, padding)
    else:
        number = float(input)
        if number < 0:
            outBits += '1'
        else:
            outBits += '0'
        numberOfExponentBits = getNumberOfExponentBits(floating_size)
        numberOfMantissaBits = (floating_size * 8) - numberOfExponentBits - 1
        number = abs(number)
        wholePart = int(number)
        fractionPart = number - wholePart
        wholeBinary = numberToBinary(str(wholePart), Type.UNSIGNED, padding=0)
        fractionBinary = ""
        result = fractionPart
        while result != 1 and result != 0:  # TODO: FIX INFINITE LOOP!
            result = result * 2
            if result < 1.0:
                fractionBinary += "0"
            else:
                fractionBinary += "1"
                if result == 1:
                    break
                result = result - int(result)

        mantissa = wholeBinary + '.' + fractionBinary
        E = mantissa.find('.') - 1 if mantissa[0] == '1' else -1 * (mantissa.find('1') - 1)
        mantissa = shiftFloatingPoint(mantissa, E)
        mantissa = handleFractionLength(mantissa[2:], numberOfMantissaBits)

        exp = E + pow(2, numberOfExponentBits - 1) - 1
        expInBinary = numberToBinary(str(exp), Type.UNSIGNED, padding=numberOfExponentBits)

        outBits += expInBinary + mantissa
        print(wholeBinary)
        print(fractionBinary)
    return outBits


def twosComplement(binary, padding):
    outstr = ''
    for c in binary:
        if c == '0':
            outstr += '1'
        else:
            outstr += '0'
    number = binaryToNumber(outstr, Type.UNSIGNED)
    number += 1
    outstr = numberToBinary(str(number), Type.UNSIGNED, padding=padding)
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
    bitsDictionary = {
        1: 3,
        2: 8,
        3: 10,
    }

    if 0 < floating_size < 3:
        return bitsDictionary[floating_size]
    else:
        return 12

def nibbleToHexDigit(nibble):
    number = binaryToNumber(("0"*12) + nibble, Type.UNSIGNED)
    if number < 10:
        return str(number)
    else:
        hexDigitDict = {
            10: "A",
            11: "B",
            12: "C",
            13: "D",
            14: "E",
            15: "F"
        }
        return hexDigitDict[number]


def convertBinaryToHex(input, endianness):
    if (endianness not in possible_orderings):
        raise AttributeError(str(endianness) + " is not a valid endianness.")
    hexDigits = list()
    bytesList = list()
    while len(input) % 4 != 0:
        input = "0" + input
    for i in range(0, len(input), 4):
        hexDigits.append(nibbleToHexDigit(input[i : i + 4]))

    digitsLen = len(hexDigits)
    if endianness == LITTLE_ENDIAN:
        for i in range(0, digitsLen, 2):
            bytesList.insert(0, hexDigits[i] + hexDigits[i+1])
    else:
        for i in range(0, digitsLen, 2):
            bytesList.append(hexDigits[i] + hexDigits[i+1])

    return " ".join(bytesList)


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
        output.append(numberToBinary(line, getTypeOfInput(line), floating_size))

    # Start test
    outputfile = open('./sample-output.txt', 'r')
    correctoutput = outputfile.readlines()
    correctoutput = list(map(lambda l: l.strip(), correctoutput))
    outputfile.close()

    hex_outputs = []

    for out in output:
        result = convertBinaryToHex(out,ordering)
        hex_outputs.append(result)

    assert set(hex_outputs) == set(correctoutput), "Output was:\n" + str(hex_outputs) + "\nShould be:\n" + str(
        correctoutput) + "."
    # End test


if __name__ == "__main__":
    main()
