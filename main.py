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
    return map(lambda l: l.strip(), lines)


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
    floating_size_text = str(input())  # '2 bytes'
    floating_size = getFloatingSize(floating_size_text)  # int: 2

    lines = readInputFile()
    print('lines is ', lines)


if __name__ == "__main__":
    main()
