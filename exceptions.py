class TokenNotMatchedException(Exception):
    def __init__(self, given_type, current_token):
        # Call the base class constructor with the parameters it needs
        super().__init__('The given type ({}) is not matched with current type: ({}).'.format(given_type, current_token))


class WrongTokenException(Exception):
    def __init__(self, token):
        # Call the base class constructor with the parameters it needs
        super().__init__('Wrong token: {}:'.format(token))


class WrongCharacterException(Exception):
    def __init__(self, char):
        # Call the base class constructor with the parameters it needs
        super().__init__('Wrong character: '+char)
