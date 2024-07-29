REG_MAP = ['t0', 't1', 't2', 't3', 't4', 't5', 't6', 's0', 's1', 's2', 's3', 's4', 's5', 's6', 's7', 's8', 's9', 's10', 's11', 'a0', 'a1', 'a2', 'a3', 'a4', 'a5', 'a6', 'a7']

class Codegenerator:
    def __init__(self, ast, options):
        self.ast = ast

        self.variables = {}
        self.reg_index = 0

        self.output = []
        
        self.options = options

    def inform(self, message):
        if not self.options.get('quiet'):
            print(f"{message}")
    
    def allocate_register(self):
        if self.reg_index >= len(REG_MAP):
            raise Exception("[CODEGEN:] Out of registers")
        reg_name = REG_MAP[self.reg_index]
        self.reg_index += 1
        return reg_name

    def free_register(self):
        if self.reg_index > 0:
            self.reg_index -= 1

    def generate(self):
        self.visit(self.ast)
        self.output.extend(('li a7, 10', 'ecall'))  # System call to exit the program

        self.inform("[CODEGEN:] -------------------------------------------")
        for line in self.output:
            self.inform(line)
        self.inform("------------------------------------------------------")
        self.inform(f"[CODEGEN:] Variables: {self.variables}")
        self.inform("\n")
        return self.output

    def visit(self, node):
        method_name = f'visit_{node["type"]}'
        visitor = getattr(self, method_name, self.generic_visitor)
        return visitor(node)
    
    def generic_visitor(self, node):
        raise Exception(f"[CODEGEN]: No visit_{node['type']} method")
    
    def visit_prog(self, node):
        self.output.extend(('# Compiled by Dummy', '# Benjamin Münstermann - 2024'))

        if self.options.get('output'):
            self.output.extend(('.data', 'newline: .asciz "\\n"'))

        self.output.extend(('.text', '.globl main', 'main:'))

        for statement in node['statements']:
            self.visit(statement)
    
    def visit_assignment(self, node):
        var_name = node['identifier']
        reg_name = self.allocate_register()
        self.variables[var_name] = reg_name
        value_reg = self.visit(node['expression'])
        self.output.append(f"mv {reg_name}, {value_reg}")
        self.free_register()

        if self.options.get('output', True):
            self.output.extend((f"mv a0, {value_reg}", 'li a7, 1', 'ecall', 'la a0, newline', 'li a7, 4', 'ecall')) 

    def visit_expression(self, node):
        expr_reg = self.visit(node['expression'])

        if self.options.get('output', True):
            self.output.extend((f"mv a0, {expr_reg}", 'li a7, 1', 'ecall', 'la a0, newline', 'li a7, 4', 'ecall'))
    
    def visit_add_expression(self, node):
        left_reg = self.visit(node['left'])
        for right_node in node['right']:
            operator = right_node['operator']
            right_reg = self.visit(right_node['right'])
            if operator == '+':
                self.output.append(f"add {left_reg}, {left_reg}, {right_reg}")
            elif operator == '-':
                self.output.append(f"sub {left_reg}, {left_reg}, {right_reg}")
            self.free_register()
        return left_reg
    
    def visit_mul_expression(self, node):
        left_reg = self.visit(node['left'])
        for right_node in node['right']:
            operator = right_node['operator']
            right_reg = self.visit(right_node['right'])
            if operator == '*':
                self.output.append(f"mul {left_reg}, {left_reg}, {right_reg}")
            elif operator == '/':
                self.output.append(f"div {left_reg}, {left_reg}, {right_reg}")
            self.free_register()
        return left_reg
    
    def visit_number(self, node):
        reg_name = self.allocate_register()
        self.output.append(f"li {reg_name}, {node['value']}")
        return reg_name
    
    def visit_identifier(self, node):
        var_name = node['value']
        if var_name in self.variables:
            return self.variables[var_name]
        else:
            raise Exception(f"[CODEGEN]: Undefined variable {var_name}")