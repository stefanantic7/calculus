from interpreters import Interpreter
from lexer import Lexer

INFIX, PREFIX, POSTFIX = ('INFIX', 'PREFIX', 'POSTFIX')


class Memory:

    def __init__(self):
        self.map = dict()

    def store(self, key, value):
        self.map[key] = value

    def get(self, key):
        if key not in self.map:
            return None
        return self.map[key]


def main():
    memory = Memory()

    state = INFIX
    while True:
        try:
            text = input(state + ' --> ')
        except KeyboardInterrupt or EOFError:
            break

        if not text:
            continue

        if text.lower() == 'exit' or text.lower() == 'exit()':
            break

        if text.upper() in (INFIX, PREFIX, POSTFIX):
            state = text.upper()
            continue

        lexer = Lexer(text)
        interpreter = Interpreter(lexer, memory)

        result = interpreter.resolve()
        print(result)


if __name__ == "__main__":
    main()
