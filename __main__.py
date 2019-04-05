from interpreters import Interpreter
from lexer import Lexer

INFIX, PREFIX, POSTFIX = ('INFIX', 'PREFIX', 'POSTFIX')


def main():
    state = INFIX
    while True:
        text = input(state+' --> ')

        if not text:
            continue

        if text.lower() == 'exit' or text.lower() == 'exit()':
            break

        if text.upper() in (INFIX, PREFIX, POSTFIX):
            state = text.upper()
            continue

        lexer = Lexer(text)
        interpreter = Interpreter(lexer)

        result = interpreter.resolve()
        print(result)


if __name__ == "__main__":
    main()
