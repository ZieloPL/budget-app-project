from itertools import zip_longest
import math as m


class Category:

    def __init__(self, name):
        self.name = name
        self.ledger = []

    def __str__(self):
        result = self.name.center(30, '*') + '\n'
        text = ''

        for i in self.ledger:
            text += i['description'][0:23]
            text += ' ' * (23 - int(len(i['description'])))
            text += f"{i['amount']:.2f}".rjust(7)
            text += '\n'
        text += 'Total: ' + str(self.get_balance())
        return result + text

    def deposit(self, amount, description=''):
        self.ledger.append({'amount': amount, 'description': description})

    def withdraw(self, amount, description=''):
        if self.check_funds(amount):
            self.ledger.append({'amount': -amount, 'description': description})
            return True
        else:
            return False

    def transfer(self, amount, category):
        if self.check_funds(amount):
            self.withdraw(amount, f'Transfer to {category.name}')
            category.deposit(amount, f'Transfer from {self.name}')
            return True
        else:
            return False

    def get_balance(self):
        suma = 0
        for i in self.ledger:
            suma += i['amount']
        return suma

    def check_funds(self, amount):

        if self.get_balance() < amount:
            return False
        else:
            return True


def create_spend_chart(categories):
    suma = 0
    nameList = []
    percList = []
    result = ''

    for category in categories:
        nameList.append(category.name)
        for i in category.ledger:
            suma += abs(i['amount']) if i['amount'] < 0 else 0

    for category in categories:
        sumPer = 0
        for i in category.ledger:
            sumPer += abs(i['amount']) if i['amount'] < 0 else 0
        percentage = m.floor(sumPer / suma * 10)

        percList.append(percentage)

    result += 'Percentage spent by category\n'
    for i in range(100, -10, -10):
        if i < 100:
            result += ' '
        if i < 10:
            result += ' '
        result += str(i) + '|'

        for k, v in enumerate(percList):
            if i <= v * 10:
                result += ' o '
            else:
                result += '   '
            if k + 1 == len(percList):
                result += ' \n'
                break
    result += '    '
    result += '-' * len(nameList) * 3 + '-'
    result += '\n     '

    zippy = list(zip_longest(*nameList, fillvalue=' '))
    for i, j in enumerate(zippy):
        for k, v in enumerate(j):
            if k + 1 == len(j) and v == ' ':
                result += v + '  '
            else:
                result += v + '  '

        if i + 1 != len(zippy):
            result += '\n     '
    return result


food = Category('Food')
food.deposit(1000, 'deposit')
food.withdraw(10.15, 'groceries')
food.withdraw(15.89, 'restaurant and more food for dessert')
clothing = Category('Clothing')
fun = Category('Enterteinment')
auto = Category('Car')
auto.deposit(1000)
auto.withdraw(100, 'Holidays')
fun.deposit(1000)
fun.withdraw(203)
food.transfer(50, clothing)
clothing.deposit(1000, 'deposit')
clothing.withdraw(20, 'jeans')
clothing.withdraw(200, 'hoodie')
print(food)

print(create_spend_chart([food, clothing, fun, auto]))