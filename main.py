from utils import check_data, add, all_, search, line


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
            add(data)
        elif data in ['3', '4']:
            all_(data)
        elif data == '5':
            search()
        else:
            print('Вы должны указать номер операции')


if __name__ == '__main__':
    run()
