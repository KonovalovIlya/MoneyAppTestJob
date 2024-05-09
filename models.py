import json
from dataclasses import dataclass


@dataclass
class Transaction:
    date: str
    category: str
    amount: str
    description: str

    def save(self) -> None:
        """
        Сохраняет данные трацзакции в файл.
        """
        self.amount = int(self.amount)
        month = self.date.split('-')[1].lstrip('0')
        with open('data.json', 'r') as f:
            data = json.load(f)
        if ' ' in self.description:
            self.description = '_'.join(self.description.split())
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

    def save_with_change(self, i: int, pre_amount: int) -> None:
        """
        Сохраняет изменения записанной транзакции.
        """
        with open('data.json', 'r') as f:
            data = json.load(f)
        if self.category == 'income':
            data['balance'] -= pre_amount
            data['balance'] += self.amount
        else:
            data['balance'] += pre_amount
            data['balance'] -= self.amount
        if ' ' in self.description:
            self.description = '_'.join(self.description.split())
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
                        for j, i in enumerate(days.get(day)):
                            tran_list.append(
                                (
                                    j,
                                    Transaction(
                                        date=day,
                                        category=operation,
                                        amount=i.get('amount'),
                                        description=i.get('description')
                                    )
                                )
                            )

        return tran_list

    @staticmethod
    def get(category, i, date, amount, description):
        with open('data.json', 'r') as f:
            data = json.load(f)
        try:
            a, d = data.get(category).get(date.split('-')[1].lstrip('0')).get(date)[int(i)].values()
            if a == int(amount) and d == description:
                tr = Transaction(
                    category=category,
                    date=date,
                    amount=amount,
                    description=description
                )
                return tr
            else:
                return None
        except:
            return None
