import random
import string


class LengthError(Exception):
    pass


class LetterError(Exception):
    pass


class DigitError(Exception):
    pass


def check_login(login):
    for i in login:
        flag = False

        for j in string.ascii_letters + string.digits:
            if i == j:
                flag = True
                break

        if not flag:
            raise LetterError

    if len(login) < 4:
        raise LengthError


def check_password(password):
    password_lower = password.lower()

    if len(password_lower) < 8:
        raise LengthError

    if not (any(map(str.isupper, password)) and any(map(str.islower, password))):
        raise LetterError

    if not (any(map(str.isdigit, password))):
        raise DigitError

    for i in password:
        flag = False

        for j in string.ascii_letters + string.digits + string.punctuation:
            if i == j:
                flag = True
                break

        if not flag:
            raise LetterError

    return 'ok'


def generate(n):
    password = (''.join(random.choices(list(set(string.ascii_letters + string.digits + '$%!@') -
                                                    {'I', 'l', '1', 'o', 'O', '0'}), k=n)))

    while True:
        try:
            check_password(password)
            return password
        except Exception:
            password = (''.join(random.choices(list(set(string.ascii_letters + string.digits + '$%!@') -
                                                    {'I', 'l', '1', 'o', 'O', '0'}), k=n)))
