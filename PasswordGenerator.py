import random
import string
import sqlite3


# Создаётся несколько классов для вывода ошибок
class LengthError(Exception):
    pass


class LoginError(Exception):
    pass


class LetterError(Exception):
    pass


class DigitError(Exception):
    pass


def check_login(login: str):
    con = sqlite3.connect("bank_info.sqlite")
    cur = con.cursor()
    find_login = cur.execute(f"""SELECT login FROM account_info WHERE login == '{login}'""").fetchone()
    con.close()
    if not (find_login is None):
        raise LoginError
    for i in login:
        flag = False

        # Проверка логина на содержание в нём недопустимых символов
        for j in string.ascii_letters + string.digits:
            if i == j:
                flag = True
                break

        if not flag:
            raise LetterError

    # Проверка на длину логина
    if len(login) < 4:
        raise LengthError


def check_password(password):  # Проверка пароля на правильность
    password_lower = password.lower()

    if len(password_lower) < 8:
        raise LengthError

    if not (any(map(str.isupper, password)) and any(map(str.islower, password))):  # Проверка на содержание заглавных и строчных букв
        raise LetterError

    if not (any(map(str.isdigit, password))):  # Проверка на наличие цифр в пароле
        raise DigitError

    for i in password:
        flag = False

        for j in string.ascii_letters + string.digits + string.punctuation:  # Проверка на правильность символов в пароле
            if i == j:
                flag = True
                break

        if not flag:
            raise LetterError

    return 'ok'


def generate(n):  # Генератор пароля
    password = (''.join(random.choices(list(set(string.ascii_letters + string.digits + '$%!@') -
                                            {'I', 'l', '1', 'o', 'O', '0'}), k=n)))

    # Цикл на случай если сгенерированный пароль не будет подходить условиям, то есть пароль не может быть неподходящим
    while True:
        try:
            check_password(password)
            return password
        except Exception:
            password = (''.join(random.choices(list(set(string.ascii_letters + string.digits + '$%!@') -
                                                    {'I', 'l', '1', 'o', 'O', '0'}), k=n)))
