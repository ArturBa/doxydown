import re

def print_doxydown(data, file_handler):
    print_module(data.module, file_handler)
    print_functions_short(data.function, file_handler)
    print_enums_define(data.enum, file_handler)
    print_enums_define(data.define, file_handler, True)
    print_structures(data.struct, file_handler)
    print_functions(data.function, file_handler)


def print_module(module, file_handler):
    if not module.module:
        return
    file_handler.write(f'## {module.module}\n')

    file_handler.write(f'## Detailed Documentation:\n\n')
    for i in module.description:
        file_handler.write(f'{i}\n\n')

    if len(module.example) != 0:
        file_handler.write(f'*Example:*\n```c\n')
        for i in module.example:
            file_handler.write(f'{i}\n')
        file_handler.write(f'```\n')


def print_functions_short(functions, file_handler):
    if not functions:
        return
    file_handler.write(f'## Functions:\n\n')

    for function in functions:
        link = '#function-' + re.sub("[\(|\)|\*|\&|,|.]", "", function.name.lower().replace(" ", "-"))
        file_handler.write(f'''> [`{function.name}`]({link})\n\n''')

    pass


def print_enums_define(enums_define, file_handler, define = False):
    if not enums_define:
        return

    if define:
        file_handler.write(f'## Defines:\n\n')
    else:
        file_handler.write(f'## Enums:\n\n')

    for enum_define in enums_define:
        if enum_define.name:
            if define:
                file_handler.write(f'#### Define: `{enum_define.name}`\n\n')
            else:
                file_handler.write(f'#### Enum: `{enum_define.name}`\n\n')
        if enum_define.brief:
            file_handler.write(f'**{enum_define.brief}**\n\n')
        if enum_define.description:
            for i in enum_define.description:
                file_handler.write(f'{i}\n\n')
        if enum_define.code:
            file_handler.write(f'```c\n')
            for i in enum_define.code:
                file_handler.write(f'{i}\n')
            file_handler.write(f'```\n')


def print_structures(structs, file_handler):
    if not structs:
        return
    file_handler.write(f'## Structures:\n\n')
    for struct in structs:
        if struct.name:
            file_handler.write(f'#### Struct: `{struct.name}`\n\n')
        if struct.brief:
            file_handler.write(f'**{struct.brief}**\n\n')
        if struct.description:
            for i in struct.description:
                file_handler.write(f'{i}\n\n')
        if struct.code:
            file_handler.write(f'```c\n')
            for i in struct.code:
                file_handler.write(f'{i}\n')
            file_handler.write(f'```\n')


def print_functions(functions, file_handler):
    if not functions:
        return
    file_handler.write(f'## Functions Documentation:\n\n')
    for function in functions:
        if function.name:
            file_handler.write(f'#### Function: `{function.name}`\n\n')
            file_handler.write(f'```c\n')
            file_handler.write(f'{function.name}\n')
            file_handler.write(f'```\n')
        if function.brief:
            file_handler.write(f'**{function.brief}**\n\n')
        if function.description:
            for i in function.description:
                file_handler.write(f'{i}\n\n')
        if function.attentions:
            file_handler.write(f'##### Attention:\n')
            for i in function.attentions:
                if isinstance(i, list):
                    for j in i:
                        file_handler.write(f'{j}\n')
                else:
                    file_handler.write(f'{i}\n')
            file_handler.write(f'\n')
        if function.params:
            file_handler.write(f'*Parameters:*\n\n')
            for i in function.params:
                buffer = i.split(maxsplit=1)
                if not buffer[1]:
                    buffer[1] = " "
                buffer = '`' + buffer[0] + '` ' + buffer[1]
                file_handler.write(f'- {buffer}\n\n')
        if function.returns:
            file_handler.write(f'*Return:*\n\n')
            for i in function.returns:
                file_handler.write(f'- {i}\n\n')

