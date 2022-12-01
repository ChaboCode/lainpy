import parser
from backend import execute, execution, clean

def lain_file(file):
    lines = file.readlines()
    counter = 0
    for line in lines:
        counter += 1
        parse_tree = parser.parse_stmt(line)
        error = execute(parse_tree)
        if error:
            print('    LAIN PROMPT FAILED AT FILE ' + file.name)

def lain_prompt():
    code = input('lain> ')
    parse_tree = parser.parse_stmt(code)
    execute(parse_tree)

def init():
    clean()
    while not execution['exit']:
        lain_prompt()
