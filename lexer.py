import re

# Tokens
NUMBER = r"\d+"
IDENTIFIER = r"[a-zA-Z_]\w*"
OPERATOR = r"[+,\-,*,/]"

TOKENS = [
    ('NUMBER', NUMBER),
    ('IDENTIFIER', IDENTIFIER),
    ('OPERATOR', OPERATOR),
    ('EQUALS', r"="),
    ('PAREN', r"[()]"),
    ('SEMICOLON', r";"),
    ('SKIP', r"[ \t\n\r]+"),
    ('ANY', r"."),
]

class Lexer:
    def __init__(self, source_string, options):
        self.source_string = source_string
    
        self.tokens = []

        self.options = options
    
    def inform(self, message):
        if not self.options.get('quiet'):
            print(f"[LEXER]: {message}")

    def lex(self):
        token_regex = '|'.join(f'(?P<{pair[0]}>{pair[1]})' for pair in TOKENS)

        for token in re.finditer(token_regex, self.source_string):
            token_type = token.lastgroup
            token_value = token.group(token_type)

            if token_type == 'SKIP':
                continue
            elif token_type == 'NUMBER':
                self.tokens.append(('NUMBER', token_value))
            elif token_type == 'IDENTIFIER':
                self.tokens.append(('IDENTIFIER', token_value))
            elif token_type == 'EQUALS':
                self.tokens.append(('EQUALS', token_value))
            elif token_type == 'OPERATOR':
                self.tokens.append(('OPERATOR', token_value))
            elif token_type == 'PAREN':
                self.tokens.append(('PAREN', token_value))
            elif token_type == 'SEMICOLON':
                self.tokens.append(('SEMICOLON', token_value))
            elif token_type == 'ANY':
                self.inform("Invalid token: ", token_value)
                return None
        
        return self.tokens