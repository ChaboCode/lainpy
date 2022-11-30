import parser
from backend import execute, execution, clean

def lain_prompt():
    code = input('lain> ')
    parse_tree = parser.parse_stmt(code)
    execute(parse_tree)

def init():
    clean()
    while not execution['exit']:
        lain_prompt()
