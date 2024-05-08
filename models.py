import json
import datetime
from dataclasses import dataclass

CONSTANTS = {
    '1': 'income',
    '2': 'outcome',
    '3': 'all income',
    '4': 'all outcome',
    '5': 'Найти транзакцию',
    '6': 'exit',
    'income': 'доходы',
    'outcome': 'расходы'
}

MONTHS = {
    '1': 'январе',
    '2': 'феврале',
    '3': 'марте',
    '4': 'апреле',
    '5': 'мае',
    '6': 'июне',
    '7': 'июле',
    '8': 'августе',
    '9': 'сентябре',
    '10': 'октябре',
    '11': 'ноябре',
    '12': 'декабре'
}


@dataclass
class Transaction:
    date: str
    category: str
    amount: int
    description: str

    def save(self) -> None:
        """
        Сохраняет данные трацзакции в файл.
        """
        month = self.date.split('-')[1].lstrip('0')
        with open('data.json', 'r') as f:
            data = json.load(f)
        if self.category == 'income':
            data['balance'] += self.amount
        else:
            data['balance'] -= self.amount
        if self.date not in data.get(self.category).get(month).keys():
            data.get(self.category).get(month)[self.date] = [
                {
                    "amount": self.amount,
                    "description": self.description
                }
            ]
        else:
            data.get(self.category).get(month).get(self.date).append(
                {
                    "amount": self.amount,
                    "description": self.description
                }
            )
        with open('data.json', 'w') as f:
            f.write(json.dumps(data))

    def save_with_change(self, data: dict, i: int, pre_amount: int) -> None:
        """
        Сохраняет изменения записанной транзакции.
        """
        if self.category == 'income':
            data['balance'] -= pre_amount
            data['balance'] += self.amount
        else:
            data['balance'] += pre_amount
            data['balance'] -= self.amount
        month = self.date.split('-')[1].lstrip('0')
        data.get(self.category).get(month).get(self.date)[i]['amount'] = self.amount
        data.get(self.category).get(month).get(self.date)[i]['description'] = self.description
        with open('data.json', 'w') as f:
            f.write(json.dumps(data))

    @staticmethod
    def get_all() -> list:
        tran_list = []
        with open('data.json', 'r') as f:
            data = json.load(f)
        for operation in data:
            if isinstance(data.get(operation), dict):
                for days in data.get(operation).values():
                    for day in days:
                        for i in days.get(day):
                            tran_list.append(
                                Transaction(
                                    date=day,
                                    category=operation,
                                    amount=i.get('amount'),
                                    description=i.get('description')
                                )
                            )

        return tran_list


def line() -> None:
    """
    Выводит на экран линию разделитель.
    """
    print('-' * 30)


def all_(operation) -> None:
    """
    Выводит на экран общую сумму доходов или расходов за выбранный месяц.
    """
    operation = operation.lstrip('all ')
    line()
    print('Укажите месяц цифрой')
    month = input()
    while not month.isdigit():
        print('Используйте цифры от 1 до 12')
        month = input()
    else:

        line()
        all_ops = Transaction.get_all()
        summ_ = sum(tr.amount for tr in all_ops if tr.date.split('-')[1].lstrip('0') == month and tr.category == operation)
        print(f'Все {CONSTANTS.get(operation)} в {MONTHS.get(month)} - {summ_} рублей')
        line()
        input('Нажми Enter для продолжения')


def check_data() -> str:
    """
    Возвращает значение 'balance'.
    """
    with open('data.json', 'r') as f:
        data = json.load(f)
        balance = data.get('balance')
        return balance


def change(data: dict):
    print('\nКакую транзакцию вы хотите изменить?')
    in_data = input('Укажите категорию, id, дату, сумму, описание:\n')
    category, i, date, amount, description = in_data.split(' ')
    print('Вы можете изменить сумму и/или описание')
    amount_ = int(input('Укажите сумму\n'))
    description_ = input('Укажите описание\n')
    tr = Transaction(
        date=date,
        category=category,
        amount=amount_,
        description=description_
    )
    tr.save_with_change(data, int(i), int(amount))


def by_category(data: dict):
    category = input(
        'Укажите категорию:\n'
        '1 - Доходы\n'
        '2 - Расходы\n'
    )
    while category not in ['1', '2']:
        print('Используйте 1 или 2')
    else:
        all_ops = Transaction.get_all()
        all_ops = [tr for tr in all_ops if CONSTANTS.get(category) == tr.category]
        print('Категория id  Дата  сумма  описание')
        line()
        for i, tr in enumerate(all_ops):
            print(tr.category, i, tr.date, tr.amount, tr.description)
        change(data)


def by_date(data: dict):
    date = input('Укажите дату в формате ДД-ММ-ГГГГ\n')
    print('Категория id  Дата  сумма  описание')
    line()
    for h, i in data.items():
        if isinstance(i, dict):
            for j in i.values():
                for day in j:
                    if day == date:
                        for k, tr in enumerate(j.get(day)):
                            print(h, k, day, *tr.values())
    change(data)


def by_amount(data):
    amount = int(input('Укажите сумму транзакции\n'))
    print('Категория id  Дата  сумма  описание')
    line()
    for h, i in data.items():
        if isinstance(i, dict):
            for j in i.values():
                for day in j:
                    for k, tr in enumerate(j.get(day)):
                        if tr.get('amount') == amount:
                            print(h, k, day, *tr.values())
    change(data)


def search():
    with open('data.json', 'r') as f:
        data = json.load(f)
    answ = input(
        'Выберете поле по которому хотите вести поиск:\n'
        '1 - Категория\n'
        '2 - Дата\n'
        '3 - Сумма\n'
    )
    if answ == '1':
        by_category(data)
    elif answ == '2':
        by_date(data)
    elif answ == '3':
        by_amount(data)


def run() -> None:
    """
    Запуск программы. Выводит на экран результаты выбранных операций.
    """
    while True:
        balance = check_data()
        line()
        print("Ваш баланс {}".format(balance))
        line()
        print(
            'Какую операцию вы хотите выполнить?\n\n'
            '1 - Пополнить\n'
            '2 - Списать\n'
            '3 - Доходы за месяц\n'
            '4 - Расходы за месяц\n'
            '5 - Найти транзакцию\n'
            '6 - Выход\n'
        )
        data = input()
        if data == '6':
            break
        if data in ['1', '2']:
            amount, description = input('Сумма, описание: ').split(', ')
            t = Transaction(
                date=datetime.datetime.now().strftime('%d-%m-%Y'),
                category=CONSTANTS.get(data),
                amount=int(amount),
                description=description
            )
            t.save()
        elif data in ['3', '4']:
            all_(CONSTANTS.get(data))
        elif data == '5':
            search()
        else:
            print('Вы должны указать номер операции')


if __name__ == '__main__':
    run()
