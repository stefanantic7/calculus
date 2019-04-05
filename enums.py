from enum import Enum


class TokenType(Enum):
    WORD, ASSIGN, INTEGER, PLUS, MINUS, MUL, DIV, EOF, RPAREN, LPAREN, LESS, GREATHER, EQUAL, NOT_EQUAL, LESS_EQ, GREATHER_EQ = (
        'WORD', 'ASSIGN', 'INTEGER', 'PLUS', 'MINUS', 'MUL', 'DIV', 'EOF', 'RPAREN', 'LPAREN', 'LESS', 'GREATHER',
        'EQUAL', 'NOT_EQUAL',
        'LESS_EQ', 'GREATHER_EQ'
    )
