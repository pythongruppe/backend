from enum import Enum


# values from boliga.dk
class PropertyType(Enum):
    VILLA = 1
    RÆKKEHUS = 2
    EJERLEJLIGHED = 3
    FRITIDSHUS = 4
    ANDELSBOLIG = 5
    LANDEJENDOM = 6
    HELGÅRSGRUND = 7
    FRITIDSGRUND = 8
    VILLALEHLIGHED = 9
    ANDET = 10
    FRITIDSBOLIG = 11

    def __str__(self):
        return super(PropertyType, self).__str__()[13:]

def to_code(string):
    for enum in PropertyType:
        if string.lower() in str(enum).lower():
            return enum

    return list([e for e in PropertyType])[-1]


def from_code(code):
    for enum in PropertyType:
        if int(code) == enum.value:
            return enum

    return list([e for e in PropertyType])[-1]