from enum import Enum


class Language(Enum):
    C = 0


class Class(Enum):
    Function = 0,
    Enum = 1,
    Define = 2,
    Struct = 3,
    Module = 4,
    Non = -1


class Regex:
    start = ""
    mid = ""
    end = ""

    def __init__(self, language):
        if language == Language.C:
            self.start = r'\/\*[\*|!]'
            self.end = r' \*\/'


class Function:
    name = ""
    brief = ""
    description = []
    attentions = []
    params = []
    returns = []


class Enum:
    name = ""
    brief = ""
    description = []
    code = []


class Define:
    name = ""
    brief = ""
    description = []
    code = []

    def __init__(self):
        self.name = ""
        self.brief = ""
        self.description = []
        self.code = []


class Struct:
    name = ""
    brief = ""
    description = []
    code = []


class Module:
    module = ""
    description = []
    example = []


class Main:
    module = Module()
    function = []
    enum = []
    define = []
    struct = []
