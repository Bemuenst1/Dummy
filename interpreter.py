class Interpreter:
    def __init__(self, ast, options):
        self.ast = ast

        self.variables = {}
        self.results = []

        self.options = options
    
    def inform(self, message):
        if not self.options.get('quiet'):
            print(f"{message}")
    
    def interpret(self):
        self.inform("[INTERPRETER:] ---------------------------------------")
        self.visit(self.ast)
        self.inform("------------------------------------------------------")
        self.inform(f"[INTERPRETER:] Variables: {self.variables}")
        self.inform(f"[INTERPRETER:] Results: {self.results}")
        self.inform("\n")
    
    def visit(self, node):
        method_name = f'visit_{node["type"]}'
        visitor = getattr(self, method_name)
        return visitor(node)
    
    def generic_visitor(self, node):
        raise Exception(f"[INTERPRETER]: No visit_{node['type']} method")
    
    def visit_prog(self, node):
        for statement in node['statements']:
            self.visit(statement)

    def visit_assignment(self, node):
        var_name = node['identifier']
        value = self.visit(node['expression'])
        self.variables[var_name] = value
        self.inform(f"{var_name} = {value}")
    
    def visit_expression(self, node):
        result = self.visit(node['expression'])
        self.results.append(result)
        self.inform(f"{result}")
        return result
    
    def visit_add_expression(self, node):
        left = self.visit(node['left'])
        for right in node['right']:
            operator = right['operator']
            right = self.visit(right['right'])
            if operator == '+':
                left += right
            elif operator == '-':
                left -= right
        return left
    
    def visit_mul_expression(self, node):
        left = self.visit(node['left'])
        for right in node['right']:
            operator = right['operator']
            right = self.visit(right['right'])
            if operator == '*':
                left *= right
            elif operator == '/':
                left /= right
        return left
    
    def visit_number(self, node):
        return int(node['value'])
    
    def visit_identifier(self, node):
        var_name = node['value']
        if var_name in self.variables:
            return self.variables[var_name]
        else:
            raise Exception(f"[INTERPRETER]: Undefined variable {var_name}")