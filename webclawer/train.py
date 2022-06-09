import re
from time import time

class train(object):
    def __init__(self, category_and_number, departure_time, arrival_time,
                 travel_time, adult_price, child_price, old_price):
        self.category = self.set_category(category_and_number)
        self.number = self.set_number(category_and_number)
        self.departure_time = departure_time
        self.arrival_time = arrival_time
        self.travel_time = travel_time
        self.adult_price = self.set_money(adult_price)
        self.child_price = self.set_money(child_price)
        self.old_price = self.set_money(old_price)

    def set_category(self, category_and_number):
        delim = ' '
        return re.split(delim, category_and_number)[0]

    def set_number(self, category_and_number):
        delim = ' '
        return re.split(delim, category_and_number)[1]

    def set_money(self, money):
        delim = ' '
        return int(re.split(delim, money)[1])
    
class trainUtil(object):
    @staticmethod
    def is_train_list_empty(train_list):
        return len(train_list) == 0

    @staticmethod
    def print_train_list_title():
        print('| %10s | %5s | %7s | %7s | %10s | % 5s | %5s | %5s' %
                ('車種', '車次', '出發時間', '抵達時間', '行駛時間', '全票', '孩童票', '敬老票'))

    @staticmethod
    def print_first_train(train_list):
        if (trainUtil.is_train_list_empty(train_list)):
            return
        trainUtil.print_train_list_title()
        
        t = train_list[0]
        print('-' * 50, end='')
        print()
        print('| %10s | %5s | %7s | %7s | %10s | % 5d | %5d | %5d' %
                    (t.category, t.number, t.departure_time, t.arrival_time,
                    t.travel_time, t.adult_price, t.child_price, t.old_price))
        
    @staticmethod
    def print_train_list(train_list):
        if (trainUtil.is_train_list_empty(train_list)):
            return
        
        trainUtil.print_train_list_title()
    
        for t in train_list:
            print('-' * 50, end='')
            print()
            print('| %10s | %5s | %7s | %7s | %10s | % 5d | %5d | %5d' %
                (t.category, t.number, t.departure_time, t.arrival_time,
                t.travel_time, t.adult_price, t.child_price, t.old_price))

