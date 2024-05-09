import json
import datetime
from conf import CONSTANTS, MONTHS
from models import Transaction


def line() -> None:
    """
    Выводит на экран линию разделитель.
    """
    print('-' * 90)


def check_data() -> str:
    """
    Возвращает значение 'balance'.
    """
    with open('data.json', 'r') as f:
        data = json.load(f)
        balance = data.get('balance')
        return balance


def check_date(date: str) -> bool:
    """
    Проверка даты введенной пользователем
    """
    try:
        date = date.split('-')
    except:
        return False
    if len(date) != 3:
        return False
    for i in date:
        if not i.isdigit():
            return False
    return True


def all_(data) -> None:
    """
    Выводит на экран общую сумму доходов или расходов за выбранный месяц.
    """
    operation = CONSTANTS.get(data).lstrip('all ')
    line()
    month = ''
    while not month.isdigit():
        print('Укажите месяц цифрой от 1 до 12')
        month = input()
    else:
        line()
        all_ops = Transaction.get_all()
        summ_ = sum(tr[1].amount for tr in all_ops if tr[1].date.split('-')[1].lstrip('0') == month and tr[1].category == operation)
        print(f'Все {CONSTANTS.get(operation)} в {MONTHS.get(month)} - {summ_} рублей')
        line()
        input('Нажми Enter для продолжения')


def add(data: str) -> None:
    """
    Добавляет новую транзакцию
    """
    amount, description = ('', '')
    while not amount.isdigit() and not description.isalpha():
        print('Укажите сумму цифрой, описание текстом')
        amount, description = input('Сумма, описание: ').split(', ')
    else:
        t = Transaction(
            date=datetime.datetime.now().strftime('%d-%m-%Y'),
            category=CONSTANTS.get(data),
            amount=amount,
            description=description
        )
        t.save()


def change() -> None:
    """
    Функция для изменения транзакции
    """
    print('\nКакую транзакцию вы хотите изменить?')
    tr = None
    while not tr:
        in_data = input('Укажите категорию, id, дату, сумму, описание:\n')
        category, i, date, amount, description = in_data.split()
        tr = Transaction.get(category, i, date, amount, description)
    else:
        print('Вы можете изменить сумму и/или описание')
        amount_ = int(input('Укажите сумму\n'))
        description_ = input('Укажите описание\n')
        tr = Transaction(
            date=date,
            category=category,
            amount=amount_,
            description=description_
        )
        tr.save_with_change(int(i), int(amount))


def search() -> None:
    """
    Запускает один из вариантов поиска
    """
    with open('data.json', 'r') as f:
        data = json.load(f)
    answ = ''
    while answ not in ['1', '2', '3']:
        answ = input(
        'Выберете поле по которому хотите вести поиск:\n'
        '1 - Категория\n'
        '2 - Дата\n'
        '3 - Сумма\n'
    )
    else:
        line()
        if answ == '1':
            by_category()
        elif answ == '2':
            by_date()
        elif answ == '3':
            by_amount()


def by_category() -> None:
    """
    Поиск транзакций по категории доход или расход
    """
    category = ''
    while category not in ['1', '2']:
        category = input(
        'Укажите категорию:\n'
        '1 - Доходы\n'
        '2 - Расходы\n'
    )
    else:
        all_ops = Transaction.get_all()
        all_ops = [tr for tr in all_ops if CONSTANTS.get(category) == tr[1].category]
        print(('\t'*2).join(['Категория', 'id', 'Дата', 'сумма', 'описание']))
        line()
        for i, tr in all_ops:
            print(('\t'*2).join([tr.category, str(i), tr.date, str(tr.amount), tr.description]))
        inp = input('Для изменения транзакций нажмите 1 для продолжения нажмите любую клавишу')
        if inp == '1':
            change()


def by_date() -> None:
    """
    Поиск транзакции по дате
    """
    date = ''
    while not check_date(date):
        date = input('Укажите дату в формате ДД-ММ-ГГГГ\n')
    else:
        all_ops = Transaction.get_all()
        all_ops = [tr for tr in all_ops if date == tr[1].date]
        print(('\t'*2).join(['Категория', 'id', 'Дата', 'сумма', 'описание']))
        line()
        for i, tr in all_ops:
            print('\t\t'.join([tr.category, str(i), tr.date, str(tr.amount), tr.description]))
        inp = input('Для изменения транзакций нажмите 1 для продолжения нажмите любую клавишу')
        if inp == '1':
            change()


def by_amount() -> None:
    """
    Поиск транзакции по сумме
    """
    amount = ''
    while not amount.isdigit():
        print('Укажите сумму цыфрами')
        amount = input('Сумма\n')
    else:
        all_ops = Transaction.get_all()
        all_ops = [tr for tr in all_ops if amount == str(tr[1].amount)]
        print(('\t'*2).join(['Категория', 'id', 'Дата', 'сумма', 'описание']))
        line()
        for i, tr in all_ops:
            print(('\t'*2).join([tr.category, str(i), tr.date, str(tr.amount), tr.description]))
        inp = input('Для изменения транзакций нажмите 1 для продолжения нажмите любую клавишу')
        if inp == '1':
            change()
