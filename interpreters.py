from enums import TokenType
from exceptions import TokenNotMatchedException, WrongTokenException
from helpers import roman_to_decimal


class Interpreter:
    def __init__(self, lexer):
        self.lexer = lexer
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
                #TODO: Parse variable
                pass
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
