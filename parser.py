class Parser:
    def __init__(self, tokens, options):
        self.tokens = tokens

        self.current_index = 0
        self.current_token = self.tokens[self.current_index] if self.tokens else None
        
        self.ast = []

        self.options = options
    
    # prog -> stmt_list
    # stmt_list -> stmt stmt_list | epsilon
    # stmt -> expr_stmt | assign_stmt
    # expr_stmt -> add_expr SEMICOLON
    # add_expr -> mul_expr mul_tail
    # mul_tail -> ADD_OP mul_expr | epsilon
    # mul_expr -> factor mul_tail
    # mul_tail -> MUL_OP factor | epsilon
    # factor -> NUMBER | IDENTIFIER | ( expr )
    # assign_stmt -> ID EQUALS expr_stmt SEMICOLON

    def inform(self, message):
        if not self.options.get('quiet'):
            print(f"[PARSER:] {message}")

    def error(self, token, message):
        raise Exception(f"[PARSER:] Error: {message} at {token[1]}\n{self.ast}")

    def consume(self, token_type):
        if self.current_token[0] == token_type:
            self.inform(f"Consumed {self.current_token[1]}")
            self.current_index += 1
            self.current_token = self.tokens[self.current_index] if self.current_index < len(self.tokens) else None
        else:
            self.error(self.current_token, f"Expected {token_type}, got {self.current_token[0]}")

    def parse(self):
        self.ast = self.parse_prog()
        self.inform(f"AST: {self.ast}\n")
        return self.ast
    
    def parse_prog(self):
        if not self.tokens:
            return None
        else:
            return {'type': 'prog', 'statements': self.parse_stmt_list()}
    
    def parse_stmt_list(self):
        nodes = []
        while self.current_token and self.current_index < len(self.tokens):
            nodes.append(self.parse_stmt())
        return nodes
    
    def parse_stmt(self):
        if self.current_token and self.current_token[0] == 'IDENTIFIER' and self.tokens[self.current_index + 1][0] == 'EQUALS':
            return self.parse_assign_stmt()
        else:
            return self.parse_expr_stmt()
    
    def parse_assign_stmt(self):
        if self.current_token[0] == 'IDENTIFIER':
            var_name = self.current_token[1]
            self.consume('IDENTIFIER')
            self.consume('EQUALS')
            expr = self.parse_add_expr()
            self.consume('SEMICOLON')
            return {'type': 'assignment', 'identifier': var_name, 'expression': expr}
        else:
            self.error(self.current_token, "Expected IDENTIFIER")
    
    def parse_expr_stmt(self):
        expr = self.parse_add_expr()
        self.consume('SEMICOLON')
        return {'type': 'expression', 'expression': expr}
    
    def parse_add_expr(self):
        left = self.parse_mul_expr()
        right = self.parse_add_tail()
        if right:
            return {'type': 'add_expression', 'left': left, 'right': right}
        return left
    
    def parse_add_tail(self):
        nodes = []
        while self.current_token and self.current_token[0] == 'OPERATOR' and self.current_token[1] in ['+', '-']:
            op = self.current_token[1]
            self.consume('OPERATOR')
            nodes.append({'type': 'operator', 'operator': op, 'right': self.parse_mul_expr()})
        return nodes
    
    def parse_mul_expr(self):
        left = self.parse_factor()
        right = self.parse_mul_tail()
        if right:
            return {'type': 'mul_expression', 'left': left, 'right': right}
        return left
    
    def parse_mul_tail(self):
        nodes = []
        while self.current_token and self.current_token[0] == 'OPERATOR' and self.current_token[1] in ['*', '/']:
            op = self.current_token[1]
            self.consume('OPERATOR')
            nodes.append({'type': 'operator', 'operator': op, 'right': self.parse_factor()})
        return nodes
    
    def parse_factor(self):
        if self.current_token[0] == 'NUMBER':
            node = {'type': 'number', 'value': self.current_token[1]}
            self.consume('NUMBER')
        elif self.current_token[0] == 'IDENTIFIER':
            node = {'type': 'identifier', 'value': self.current_token[1]}
            self.consume('IDENTIFIER')
        elif self.current_token[0] == 'PAREN' and self.current_token[1] == '(':
            self.consume('PAREN')
            node = self.parse_add_expr()
            if self.current_token[0] == 'PAREN' and self.current_token[1] == ')':
                self.consume('PAREN')
            else:
                self.error(self.current_token, "Missing closing parenthesis")
        else:
            self.error(self.current_token, "Expected NUMBER, IDENTIFIER, or PAREN")
        return node