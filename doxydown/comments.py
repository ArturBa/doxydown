from doxydown.classes import *
import logging
import re  # regex


def handle_comment(file_lines, comment_range):
    if 'module' in file_lines[1]:
        return_type = Class.Module
        value = module_comment(file_lines, comment_range)
    elif '#define' in file_lines[comment_range+1]:
        return_type = Class.Define
        value = define_comment(file_lines, comment_range)
    elif re.search(r'[a-zA-Z0-9]+ [a-zA-Z0-9|_]+\(', file_lines[comment_range+1]):
        return_type = Class.Function
        value = function_comment(file_lines, comment_range)
    elif 'enum' in file_lines[comment_range+1]:
        return_type = Class.Enum
        value = enum_comment(file_lines, comment_range)
    elif 'struct' in file_lines[comment_range + 1]:
        return_type = Class.Struct
        value = struct_comment(file_lines, comment_range)
    else:
        return Class.Non, None
    return return_type, value


def function_comment(file_lines, comment_range):
    function = Function()
    function.name = file_lines[comment_range+1][:file_lines[comment_range+1].find(')')+1].strip()
    function.brief = handle_key_word(file_lines, comment_range, 'brief')
    function.attentions = handle_attentions(file_lines, comment_range)
    function.params = handle_multiple_key_word(file_lines, comment_range, 'param')
    function.returns, returns_line = handle_returns(file_lines, comment_range)
    function.description = handle_description(file_lines, returns_line)

    return function


def enum_comment(file_lines, comment_range):
    """
        Handles Enum comments for doxygen style documentation
        :param file_lines: src input
        :param comment_range: number of commented lines
        :return: Enum class
    """
    enum = Enum()
    enum.brief = handle_key_word(file_lines, comment_range, 'brief')
    enum.description = handle_description(file_lines, comment_range)
    enum.name = handle_key_word(file_lines, comment_range, 'enum')
    enum.code = handle_code(file_lines, comment_range)
    return enum


def module_comment(file_lines, comment_range):
    module = Module()
    module.module = handle_key_word(file_lines, comment_range, 'module')

    example_line = 0
    for i in range(len(file_lines[:comment_range])):
        if '@example' in file_lines[i]:
            example_line = i
            break

    module.description = handle_description(file_lines, example_line)
    module.example = handle_description(file_lines[example_line+1:], comment_range-example_line-1)
    return module


def struct_comment(file_lines, comment_range):
    struct = Struct()
    struct.name = handle_key_word(file_lines, comment_range, 'struct')
    struct.brief = handle_key_word(file_lines, comment_range, 'brief')
    struct.description = handle_description(file_lines, comment_range)
    struct.code = handle_code(file_lines, comment_range)
    return struct


def define_comment(file_lines, comment_range):
    i = 1
    define = Define()
    define.brief = handle_key_word(file_lines, comment_range, 'brief')
    define.name = handle_key_word(file_lines, comment_range, 'def')
    define.description = handle_description(file_lines, comment_range)
    while comment_range+i < len(file_lines):
        if '#define' in file_lines[comment_range+i]:
            if '{' in file_lines[comment_range+1]:
                define.code = handle_code(file_lines, comment_range)
                break
            else:
                define.code.append(file_lines[comment_range+i].strip())
                i += 1
        else:
            break

    return define


def handle_code(file_lines, comment_range):
    buffer = []
    bracket = 1
    i = 2
    buffer.append(file_lines[comment_range + 1].strip())
    while bracket != 0:
        line = file_lines[comment_range + i]
        buffer.append(line[:-1])
        if '{' in line:
            bracket += 1
        if '}' in line:
            bracket -= 1
        i += 1
    return buffer


def handle_key_word(file_lines, comment_range, key_word):
    key_word = '@' + key_word + ' '
    for i in file_lines[:comment_range]:
        if i.find(key_word) != -1:
            return i[i.find(key_word) + len(key_word):].strip()
    return None


def handle_multiple_key_word(file_lines, comment_range, key_word):
    key_word = '@' + key_word + ' '
    buffer = []
    for i in file_lines[:comment_range]:
        if i.find(key_word) != -1:
            buffer.append(i[i.find(key_word) + len(key_word):].strip())
    return buffer


def handle_description(file_lines, comment_range):
    description = []
    for line in file_lines[1:comment_range]:
        if '@' not in line:
            description.append(line[line.find('*')+1:].strip())
    return description


def handle_returns(file_lines, comment_range):
    key_word = '@return'
    returns = []
    returns_line = 0
    for i in range(len(file_lines[:comment_range])):
        if file_lines[i].find(key_word) != -1:
            returns_line = i
            break
    if returns_line == 0:
        return None, 0
    returns = handle_description(file_lines[returns_line:], comment_range-returns_line)
    if file_lines[returns_line][file_lines[returns_line].find(key_word)+len(key_word): -1]:
        returns.insert(0, file_lines[returns_line][file_lines[returns_line].find(key_word)+len(key_word): -1])
    i = 0
    del_empty = []
    for line in returns:
        try:
            line = line[re.search(r'\w', line).span()[0]:]
            returns[i] = line
        except:
            logging.debug(f'Problem with {i} element of return list: {returns}')
            del_empty.append(i)
        i += 1
    for i in del_empty:
        del returns[i]
    return returns, returns_line


def find_next_at(file_lines, comment_range):
    for i in range(len(file_lines[:comment_range])):
        if 0 == i:
            continue
        if '@' in file_lines[i]:
            return i
    return 0


def handle_attentions(file_lines, comment_range):
    key_word = '@attention'
    attention_line = 0
    for i in range(len(file_lines[:comment_range])):
        if file_lines[i].find(key_word) != -1:
            attention_line = i
            break
    next_at = find_next_at(file_lines[attention_line:], comment_range)
    if next_at == 0:
        next_at = comment_range
    attentions = handle_description(file_lines[attention_line:], next_at)
    if file_lines[attention_line][file_lines[attention_line].find(key_word)+len(key_word):-1]:
        attentions.insert(0, file_lines[attention_line][file_lines[attention_line].find(key_word)+len(key_word):-1].strip())
    if file_lines[attention_line+next_at].find(key_word) != -1:
        attentions.append(handle_attentions(file_lines[next_at+attention_line:], comment_range-next_at-attention_line))
    return attentions
