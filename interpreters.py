from enums import TokenType
from exceptions import TokenNotMatchedException, WrongTokenException
from helpers import roman_to_decimal
from lexer import Lexer


class Interpreter:
    def __init__(self, lexer, memory):
        self.lexer = lexer
        self.memory = memory
        self.current_token = self.lexer.get_next_token()

    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            raise TokenNotMatchedException(token_type, self.current_token)

    def factor(self):
        token = self.current_token

        if token.type == TokenType.INTEGER:
            self.eat(TokenType.INTEGER)
            return token.value
        elif token.type == TokenType.LPAREN:
            self.eat(TokenType.LPAREN)
            result = self.resolve()
            self.eat(TokenType.RPAREN)
            return result
        elif token.type == TokenType.WORD:
            self.eat(TokenType.WORD)
            if token.value == 'RIM' and self.current_token.type == TokenType.LPAREN:
                self.eat(TokenType.LPAREN)
                rim = self.current_token
                self.eat(TokenType.WORD)
                self.eat(TokenType.RPAREN)
                return roman_to_decimal(rim.value)
            else:
                var_name = token.value
                if self.current_token.value == '=':
                    self.eat(TokenType.ASSIGN)
                    var_value = self.expr()
                    self.memory.store(var_name, var_value)
                    return var_value
                else:
                    if self.memory.get(var_name) is None:
                        self.memory.store(None)
                    return self.memory.get(var_name)
        else:
            raise WrongTokenException(token)

    def term(self):
        result = self.factor()

        while self.current_token.type in (TokenType.MUL, TokenType.DIV):
            token = self.current_token
            if token.type == TokenType.MUL:
                self.eat(TokenType.MUL)
                result = result * self.factor()
            elif token.type == TokenType.DIV:
                self.eat(TokenType.DIV)
                result = result // self.factor()
            else:
                raise WrongTokenException(token)

        return result

    def expr(self):

        result = self.term()

        while self.current_token.type in (TokenType.PLUS, TokenType.MINUS):
            token = self.current_token
            if token.type == TokenType.PLUS:
                self.eat(TokenType.PLUS)
                result = result + self.term()
            elif token.type == TokenType.MINUS:
                self.eat(TokenType.MINUS)
                result = result - self.term()
            else:
                raise WrongTokenException(token)

        return result

    def resolve(self):
        result = True
        left = self.expr()
        if self.current_token.type in (TokenType.LESS, TokenType.GREATHER, TokenType.EQUAL, TokenType.NOT_EQUAL, TokenType.LESS_EQ, TokenType.GREATHER_EQ):
            right = None
            while self.current_token.type in (TokenType.LESS, TokenType.GREATHER, TokenType.EQUAL, TokenType.NOT_EQUAL, TokenType.LESS_EQ, TokenType.GREATHER_EQ):

                if self.current_token.type == TokenType.LESS:
                    self.eat(TokenType.LESS)
                    right = self.expr()
                    if not (left < right):
                        result = False
                    left = right
                elif self.current_token.type == TokenType.GREATHER:
                    self.eat(TokenType.GREATHER)
                    right = self.expr()
                    if not (left > right):
                        result = False
                    left = right
                elif self.current_token.type == TokenType.EQUAL:
                    self.eat(TokenType.EQUAL)
                    right = self.expr()
                    if not (left == right):
                        result = False
                    left = right
                elif self.current_token.type == TokenType.NOT_EQUAL:
                    self.eat(TokenType.NOT_EQUAL)
                    right = self.expr()
                    if not (left != right):
                        result = False
                    left = right
                elif self.current_token.type == TokenType.LESS_EQ:
                    self.eat(TokenType.LESS_EQ)
                    right = self.expr()
                    if not (left <= right):
                        result = False
                    left = right
                elif self.current_token.type == TokenType.GREATHER_EQ:
                    self.eat(TokenType.GREATHER_EQ)
                    right = self.expr()
                    if not (left >= right):
                        result = False
                    left = right

            return result
        else:
            return left


class PostfixInterpreter:
    def __init__(self, lexer, memory):
        self.lexer = lexer
        self.memory = memory
        self.current_token = self.lexer.get_next_token()

    def eat(self):
        self.current_token = self.lexer.get_next_token()

    def resolve(self):
        output = []

        while self.current_token is not None and self.current_token.type != TokenType.EOF:
            if self.current_token.type == TokenType.WORD:
                token = self.current_token
                if token.value == 'RIM':
                    self.eat()
                    if self.current_token.type == TokenType.LPAREN:
                        self.eat()
                        rim = self.current_token
                        self.eat()
                        self.eat()
                        output.append(roman_to_decimal(rim.value))
                    else:
                        output.append(token.value)
                else:
                    output.append(self.current_token.value)
                    self.eat()
            elif self.current_token.type == TokenType.INTEGER:
                output.append(self.current_token.value)
                self.eat()
            else:
                operand1 = output.pop()
                operand2 = output.pop()
                operator = self.current_token.value
                expression = '(' + str(operand2) + operator + str(operand1) + ')'
                output.append(expression)
                self.eat()

        lexer = Lexer(str(output[0]))
        interpreter = Interpreter(lexer, self.memory)
        return interpreter.resolve()
