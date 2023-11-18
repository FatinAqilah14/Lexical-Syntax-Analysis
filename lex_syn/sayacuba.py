# import RegEx, or Regular Expression (a sequence of characters that forms a search pattern)
import re
# import keyword of Python to check whether the code fits to be categorized as keywords or not
import keyword
# import the sys module to access system-related functions and variables
import sys


# Define classes for different types of AST nodes
class AssignmentNode:
    def __init__(self, identifier, expression):
        self.identifier = identifier
        self.expression = expression

    def __str__(self):
        return f"AssignmentNode: {self.identifier} = {self.expression}"


class ExpressionNode:
    def __init__(self, operator, left, right):
        self.operator = operator
        self.left = left
        self.right = right

    def __str__(self):
        return f"ExpressionNode: {self.left} {self.operator} {self.right}"


class TermNode:
    def __init__(self, operator, left, right):
        self.operator = operator
        self.left = left
        self.right = right

    def __str__(self):
        return f"TermNode: {self.left} {self.operator} {self.right}"


class FactorNode:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return f"FactorNode: {self.value}"


# Lexical Analysis Part ====================

# regular expressions for different token types
identifier_re = re.compile(r'[a-zA-Z_][a-zA-Z0-9_]*(?![\w\d])')
integer_literal_re = re.compile(r'\b\d+\b')
float_literal_re = re.compile(r'\b\d+\.\d*\b')
string_literal_re = re.compile(r'("(?:\\.[^\"\n]|[^"\n])*")|\'(?:\\.[^\'\n]|[^\'\n])*\'\s*(?!=)|\'("(?:\\.|[^"\n])*"|\'(?:\\.|[^"\n])*\')(?!\w)')
punctuation_re = re.compile(r'[\[\]\{\}\(\),\'\:\"]')
add_re = re.compile(r'\+')
mult_re = re.compile(r'\*')
assignment_re = re.compile(r'(?<!\=)=')
semicolon_re = re.compile(r';')
subt_re = re.compile(r'-')
division_re = re.compile(r'/')
modulus_re = re.compile(r'%')
exp_re = re.compile(r'\*\*')
floorDiv_re = re.compile(r'\/\/')
comparison_re = re.compile(r'!=|>|<|>=|<=|==|<>')
comment_re = re.compile(r'(#.*|"""(?:[^"]|\n)*""")')

# try to match each token type
def tokenize(source_code):
    tokens = []

    # skip comments
    source_code = re.sub(comment_re, '', source_code)

    # identify string literals first
    for match in string_literal_re.finditer(source_code):
        string_literal_value = match.group()[1:-1].strip()
        tokens.append((string_literal_value, 'string_literal'))
        source_code = source_code[:match.start()] + source_code[match.end():]

    # identify other token types
    for match in identifier_re.finditer(source_code):
        identifier = match.group()
        if keyword.iskeyword(identifier):
            tokens.append((identifier, 'keyword'))
        else:
            # check if the identifier is part of a string literal
            for string_literal_token in tokens:
                if string_literal_token[0] == 'string_literal' and identifier.startswith(string_literal_token[1]):
                    continue  # skip identifiers that are part of string literals
            tokens.append((identifier, 'identifier'))

    # to find match for punctuation
    for match in punctuation_re.finditer(source_code):
        tokens.append((match.group(), 'punctuation'))

    # to find match for integer
    for match in integer_literal_re.finditer(source_code):
        tokens.append((match.group(), 'integer_literal'))

    # to find match for float
    for match in float_literal_re.finditer(source_code):
        tokens.append((match.group(), 'float_literal'))

    # to find match for add operation
    for match in add_re.finditer(source_code):
        tokens.append((match.group(), 'add_op'))

    # to find match for multiplication operation
    for match in mult_re.finditer(source_code):
        tokens.append((match.group(), 'mult_op'))

    # to find match for subtraction operation
    for match in subt_re.finditer(source_code):
        tokens.append((match.group(), 'subtraction_op'))

    # to find match for division operation
    for match in division_re.finditer(source_code):
        tokens.append((match.group(), 'division_op'))

    # to find match for modulus operation
    for match in modulus_re.finditer(source_code):
        tokens.append((match.group(), 'modulus_op'))

    # to find match for exponent operation
    for match in exp_re.finditer(source_code):
        tokens.append((match.group(), 'exponent_op'))

    # to find match for floor division operation
    for match in floorDiv_re.finditer(source_code):
        tokens.append((match.group(), 'floorDivision_op'))

    # to find match for comparison operation
    for match in comparison_re.finditer(source_code):
        tokens.append((match.group(), 'comparison_op'))

    # to find match for assignment sign
    for match in assignment_re.finditer(source_code):
        tokens.append((match.group(), 'assignment_sign'))

    # to find match for semicolon
    for match in semicolon_re.finditer(source_code):
        tokens.append((match.group(), 'semicolon'))

    return tokens


# Syntax Analysis Part ====================

# Retrieve the next token
def next_token():
    global current_token
    if current_token < len(tokens):
        current_token += 1
        return tokens[current_token - 1]
    return None


# Match a specific token type
def match(token_type):
    if current_token < len(tokens) and tokens[current_token][1] == token_type:
        return next_token()
    return None


# Define the grammar rules for the entire p rogram
def parse_program():
    ast = []
    while current_token < len(tokens):
        statement = parse_statement()
        if statement:
            ast.append(statement)
    return ast


# Define the grammar rules for statements
def parse_statement():
    identifier = match('identifier')
    if identifier:
        assignment_sign = match('assignment_sign')
        if assignment_sign:
            expression = parse_expression()
            match('semicolon')
            return AssignmentNode(identifier[0], expression)
    return None


# Define the grammar rules for expressions
def parse_expression():
    term = parse_term()
    while current_token < len(tokens) and tokens[current_token][1] in ['add_op', 'subtraction_op']:
        operator = next_token()
        term = ExpressionNode(operator[0], term, parse_term())
    return term


# Define the grammar rules for terms
def parse_term():
    factor = parse_factor()
    while current_token < len(tokens) and tokens[current_token][1] in ['mult_op', 'division_op', 'modulus_op', 'exponent_op', 'floorDivision_op']:
        operator = next_token()
        factor = TermNode(operator[0], factor, parse_factor())
    return factor


# Define the grammar rules for factors
def parse_factor():
    token = next_token()
    if token and token[1] in ['identifier', 'integer_literal', 'float_literal', 'string_literal']:
        return FactorNode(token)
    elif token and token[1] == 'punctuation' and token[0] == '(':
        expression = parse_expression()
        match('punctuation')
        return expression
    else:
        print(f"Syntax error at token: {token}")
        return None


# Main Function ====================
def main():
    global current_token
    # Example source code
    source_code = """
    x = 10
    y = 5
    result = x + y * (3 ** 2) / 4
    """

    print("\n------------------------")
    print("The token(s) based on the code: ")
    # tokenize the input source code
    global tokens
    tokens = tokenize(source_code)

    for token in tokens:
        print(token)

    print("------------------------")

    # Set the tokens for parsing
    # current_token = 0

    # Parse the program and generate the AST
    ast = parse_program()

    for node in ast:
        print(node)


    print("\n------------------------")
    print("The Abstract Syntax Tree (AST): ")
    for node in ast:
        print(node)
    print("------------------------")


if __name__ == '__main__':
    main()
