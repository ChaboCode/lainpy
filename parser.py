LEX_SKIP = 0
LEX_OPERATOR = 1
LEX_IDENTIFIER = 2
LEX_NUMBER = 3
LEX_KEYWORD = 4

keywords = ['print', 'do', 'end', 'if', 'else', 'while', 'exit']

def lex_hint(char):
    operations = ['+', '-', '*', '/']

    if char == ' ':
        return LEX_SKIP
    elif char in operations:
        return LEX_OPERATOR
    elif char.isalpha():
        return LEX_IDENTIFIER
    else:
        return LEX_NUMBER

# ##################
#      v
# idtf 352
# number = 352
# position = 3
#         v
# idtf 352
####################

def lex_number(code):
    number = 0
    position = 0
    for char in code:
        if char == ' ':
            break
        number += int(char) * pow(10, position)
        position += 1
    return (LEX_NUMBER, number, position)

# ##################
# v     
# idtf 352
# identifier = idtf
# position = 4
#     v
# idtf 352
####################

def lex_identifier(code):
    identifier = ''
    position = 0
    for char in code:
        if char == ' ':
            break
        identifier += char
        position += 1
    if identifier in keywords:
        return (LEX_KEYWORD, identifier, position)
    return (LEX_IDENTIFIER, identifier, position)

def lex_operator(code):
    return (LEX_OPERATOR, code[0], 1)

def lex(code):
    hint = lex_hint(code[0])
    if hint == LEX_OPERATOR:
        return lex_operator(code)
    elif hint == LEX_IDENTIFIER:
        return lex_identifier(code)
    elif hint == LEX_NUMBER:
        return lex_number(code)
    elif hint == LEX_SKIP:
        return (LEX_SKIP, 0, 1)

def parse_stmt(code):
    position = 0
    parse_tree = []
    while True:
        (lexeme, value, move_position) = lex(code[position:])
        if lexeme == LEX_SKIP:
            position += move_position
            continue

        parse_tree.append((lexeme, value))
        position += move_position
        if position >= len(code):
            break
    
    return parse_tree

def XD():
    print("Xia xheng hao xung yuo bing xhiling")