import re

class Compiler:
    def __init__(self):
        self.RESULT = []
        self.tokens = []
        self.index = 0
        self.CURRENT = None

    def Token(self, input_string):
        self.tokens = re.findall(r'\w+|[\+\-\*/\[\]\(\)=]', input_string)
        self.index = 0
        if len(self.tokens) > 0:
            self.CURRENT = self.tokens[self.index]

    def advance(self, expected_token):
        if self.CURRENT == expected_token:
            self.index += 1
            if self.index < len(self.tokens):
                self.CURRENT = self.tokens[self.index]
            else:
                self.CURRENT = None
        else:
            raise Exception(f'Error: Expected {expected_token}')

    def number(self):
        value = int(self.CURRENT)
        self.RESULT.append(f'LIT {value}')
        self.advance(self.CURRENT)

    def variable(self):
        value = self.CURRENT
        self.RESULT.append(f'LIT {value}')
        self.advance(self.CURRENT)
        if self.CURRENT == '[':
            self.advance('[')
            self.expr()
            self.advance(']')
            self.RESULT.append('ADD')
            self.RESULT.append('LOAD')
        else:
            self.RESULT.append('LOAD')

    def factor(self):
        if re.match(r'\d+', self.CURRENT):
            self.number()
        elif re.match(r'\w+', self.CURRENT):
            self.variable()
        else:
            raise Exception('Error: Invalid token')

    def term(self):
        self.factor()
        while self.CURRENT in ['*', '/']:
            op = self.CURRENT
            self.advance(op)
            self.factor()
            if op == '*':
                self.RESULT.append('MUL')
            elif op == '/':
                self.RESULT.append('DIV')

    def expr(self):
        if self.CURRENT == '-':
            self.advance('-')
            if re.match(r'\d+', self.CURRENT):
                value = int(self.CURRENT)
                value *= -1
                value = str(value)
                value.replace('-', '')
                value = '-' + value
                value = int(value)
                value = str(value)
                value.replace('--', '')

                self.RESULT.append(f'LIT {value}')
                self.advance(self.CURRENT)
            else:
                self.term()
                self.RESULT.append('NEG')
        else:
            self.term()
        while self.CURRENT in ['+', '-']:
            op = self.CURRENT
            self.advance(op)
            self.term()
            if op == '+':
                self.RESULT.append('ADD')
            elif op == '-':
                self.RESULT.append('SUB')

    def assign(self):
        if re.match(r'\w+', self.CURRENT):
            value = self.CURRENT
            self.advance(self.CURRENT)
            if self.CURRENT == '[':
                self.advance('[')
                self.expr()
                self.advance(']')
                self.RESULT.append('ADD')
            else:
                self.RESULT.append(f'LIT {value}')
            self.advance('=')
            self.expr()
            self.RESULT.append('STORE')
        else:
            raise Exception('Error: Invalid token ')

    def compile(self, input_string):
         self.Token(input_string)
         while self.CURRENT is not None:
            self.assign()

def main():
    compiler = Compiler()
    input_string = 'A=B+3*C'
    compiler.compile(input_string)
    output_string = " ".join(compiler.RESULT)
    print(output_string)

if __name__ == '__main__':
    main()
