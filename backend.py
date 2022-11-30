from parser import LEX_IDENTIFIER, LEX_NUMBER, LEX_OPERATOR, LEX_KEYWORD

NONE = 0
EXPR = 1
NOT_SET = "NOT_SET"

identifiers = {}
execution = {}


def doexit():
    print('Goodbye.')
    execution['exit'] = True


def clean():
    execution['lexeme'] = NONE
    execution['expects'] = EXPR
    execution['fail'] = False
    execution['expressions'] = []
    execution['operator'] = NONE
    execution['val1'] = NOT_SET
    execution['val2'] = NOT_SET
    execution['identifier'] = NONE
    execution['result'] = 0
    execution['keyword'] = NONE
    execution['exit'] = False


def push_expression():
    execution['expressions'].append(
        (execution['operator'], execution['val1'], execution['val2'], execution['keyword']))


def pop_expression():
    (execution['operator'], execution['val1'],
     execution['val2'], execution['keyword']) = execution['expressions'].pop()


def calculation(operator, val1, val2):
    if operator == '+':
        return val1 + val2
    if operator == '-':
        return val1 - val2
    if operator == '*':
        return val1 * val2
    if operator == '/':
        return val1 / val2
    return val1 if not val1 == 0 else val2


def load_identifier(value):
    if execution['lexeme'] == NONE:
        execution['identifier'] = value
        execution['expects'] = EXPR
    elif execution['expects'] == EXPR:
        load_expression(LEX_NUMBER, 'i' + value)  # it's an identifier
    pass


def load_expression(lexeme, value):
    if not execution['expects'] == EXPR:
        print('<<lain ERROR>>> Didn\'t expected an expression')
        execution['fail'] = True

    if lexeme == LEX_OPERATOR:
        if execution['lexeme'] == LEX_OPERATOR:
            push_expression()
        execution['lexeme'] = lexeme
        execution['operator'] = value
        execution['expects'] = EXPR
        return

    if lexeme == LEX_NUMBER:
        if execution['lexeme'] == LEX_OPERATOR or execution['lexeme'] == LEX_IDENTIFIER or execution['lexeme'] == NONE:
            execution['val1'] = value
            execution['lexeme'] = LEX_NUMBER
            execution['expects'] = EXPR
            return

        execution['val2'] = value
        execution['expects'] = EXPR
        execution['lexeme'] = LEX_NUMBER
        result = compute_expr()
        if len(execution['expressions']) > 0:
            pop_expression()
        execution['val1'] = result


def load_keyword(value):
    if not execution['keyword'] == NONE:
        push_expression()
    execution['keyword'] = value
    execution['lexeme'] = LEX_KEYWORD


def compute_expr():
    value1 = execution['val1'] if not execution['val1'] == NOT_SET else 0
    if isinstance(value1, str) and not value1 == NOT_SET:
        if value1[0] == 'i':
            value1 = identifiers[value1[1:]]
    
    value2 = execution['val2'] if not execution['val2'] == NOT_SET else 0
    if isinstance(value2, str) and not value2 == NOT_SET:
        if value2[0] == 'i':
            value2 = identifiers[value2[1:]]

    return calculation(execution['operator'],
                       value1, value2)


def compute_print():
    value = compute_expr()
    print('  > ' + str(value))


def compute_keyword():
    if execution['keyword'] == 'print':
        compute_print()
        return
    if execution['keyword'] == 'exit':
        doexit()
        return


def compute_identifier():
    if not execution['val1'] == NOT_SET:
        identifiers.update({execution['identifier']: execution['val1']})
        return


def compute():
    if not execution['keyword'] == NONE:
        compute_keyword()
        return
    if not execution['identifier'] == NONE:
        compute_identifier()
        return

    compute_print()


def execute(parse_tree):
    print('<<<lain says>>> Exectuing parse tree...')

    clean()

    for item in parse_tree:
        (lexeme, value) = item
        if lexeme == LEX_OPERATOR or lexeme == LEX_NUMBER:
            load_expression(lexeme, value)
        elif lexeme == LEX_IDENTIFIER:
            load_identifier(value)
        elif lexeme == LEX_KEYWORD:
            load_keyword(value)

        if execution['fail']:
            break
    compute()
