from random import randint
import datetime


class ImportNameError(Exception):
    pass


class PaySystemError(Exception):
    pass


pay_system_number = {'visa': '4', 'mastercard': '5', 'mir': '2'}  # префиксы платёжных систем
individual_bank_number = '739'  # индивидуальный номер банка, как опознательный знак, что эта карта была выдана данным банком

random_number = ''

TRANSLATE = {'Ь': '', 'ь': '', 'Ъ': '', 'ъ': '', 'А': 'A', 'а': 'a', 'Б': 'B', 'б': 'b', 'В': 'V', 'в': 'v',
             'Г': 'G', 'г': 'g', 'Д': 'D', 'д': 'd', 'Е': 'E', 'е': 'e', 'Ё': 'E', 'ё': 'e', 'Ж': 'Zh', 'ж': 'zh',
             'З': 'Z', 'з': 'z', 'И': 'I', 'и': 'i', 'Й': 'I', 'й': 'i', 'К': 'K', 'к': 'k', 'Л': 'L', 'л': 'l',
             'М': 'M', 'м': 'm', 'Н': 'N', 'н': 'n', 'О': 'O', 'о': 'o', 'П': 'P', 'п': 'p', 'Р': 'R', 'р': 'r',
             'С': 'S', 'с': 's', 'Т': 'T', 'т': 't', 'У': 'U', 'у': 'u', 'Ф': 'F', 'ф': 'f', 'Х': 'Kh', 'х': 'kh',
             'Ц': 'Tc', 'ц': 'tc', 'Ч': 'Ch', 'ч': 'ch', 'Ш': 'Sh', 'ш': 'sh', 'Щ': 'Shch', 'щ': 'shch', 'Ы': 'Y',
             'ы': 'y', 'Э': 'E', 'э': 'e', 'Ю': 'Iu', 'ю': 'iu', 'Я': 'Ia', 'я': 'ia', ' ': ' '}

ALPHABET = [' ', '', 'Ь', 'ь', 'Ъ', 'ъ', 'А', 'а', 'Б', 'б', 'В', 'в', 'Г', 'г', 'Д', 'д', 'Е', 'е', 'Ё', 'ё',
            'Ж', 'ж', 'З', 'з', 'И', 'и', 'Й', 'й', 'К', 'к', 'Л', 'л', 'М', 'м', 'Н', 'н', 'О', 'о',
            'П', 'п', 'Р', 'р', 'С', 'с', 'Т', 'т', 'У', 'у', 'Ф', 'ф', 'Х', 'х', 'Ц', 'ц', 'Ч', 'ч',
            'Ш', 'ш', 'Щ', 'щ', 'Ы', 'ы', 'Э', 'э', 'Ю', 'ю', 'Я', 'я']


def generate_random_number(pay_system):
    global random_number
    randnums = ""
    random_number = ""

    # В данной функции выполняется рандомная генерация номера карты, далее этот номер проверяется по алгоритму ниже
    for _ in range(11):
        randnums += str(randint(0, 9))

    random_number += pay_system_number[pay_system] + individual_bank_number + randnums


# Здесь выполняется алгоритм Луна, чтобы понять логику его действия рекомендуется ознакомиться с работой алгоритма
# https://ru.wikipedia.org/wiki/%D0%90%D0%BB%D0%B3%D0%BE%D1%80%D0%B8%D1%82%D0%BC_%D0%9B%D1%83%D0%BD%D0%B0
def luhn_algorithm(pay_system) -> str:
    generate_random_number(pay_system)
    odd_sum = 0
    even_sum = 0

    even_odd_counter = 0
    for i in random_number:
        if not even_odd_counter:
            even_sum += int(i)
            even_odd_counter = 1
        else:
            even_odd_counter = 0
            if int(i) * 2 < 10:
                odd_sum += (int(i) * 2)
            else:
                odd_sum += (int(i) * 2) - 9

    control_sum = even_sum + odd_sum
    # здесь подбирается контрольная цифра карты, которая решит, будет ли карта подходить условиям алгоритма или нет
    if str(control_sum % 10)[-1] != "0":
        valid_credit_card = random_number + str(10 - (control_sum % 10))
    else:
        valid_credit_card = random_number + "0"

    return valid_credit_card


date_now = datetime.date.today()
validity = date_now.replace(year=date_now.year + 6).strftime("%m/%y")  # выделение шести лет на обслуживание карты от сегодняшней даты


# это функция создана для сбора всех сгенерированных данных карты, чтобы не собирать по отдельности
def full_data_of_card(pay_system, name, cvv_code=randint(100, 999)) -> tuple:
    global validity

    card_number = luhn_algorithm(pay_system)
    tr_full_name = translating_name(name).split()
    tr_name = tr_full_name[0]
    tr_surname = tr_full_name[1]

    return card_number, cvv_code, str(validity), tr_name.capitalize(), tr_surname.capitalize()


def translating_name(name) -> str:
    translated_name = ""
    checking_data(name)

    for i in name.lower():
        translated_name += TRANSLATE[i]  # перевод имени с русского на английский (транслитом)

    return translated_name


def checking_data(name):  # проверка введенных данных пользователя на недопустимые символы
    for i in name:
        if i not in ALPHABET:
            raise ImportNameError
