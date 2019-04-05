from interpreters import Interpreter
from lexer import Lexer


def main():
    while True:
        try:
            text = input('INFIX'+' --> ')
        except EOFError:
            break

        if not text:
            continue

        if text == 'exit':
            break

        lexer = Lexer(text)
        interpreter = Interpreter(lexer)

        result = interpreter.resolve()
        print(result)


if __name__ == "__main__":
    main()
