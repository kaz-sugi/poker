#!/usr/bin/env python3.4
# -*- coding: utf-8 -*-


import random

class henrik_com:
    def __init__(self):
        self.play_order = []
        self.my_card = []
        self.common_card = []
        self.others_behaviour = {}

        self._min_amount = 0
        self._max_amount = 0
        self._check_bet = True

        self._mark_list = []
        self._num_list = []

    def your_card(self, _card):
        self.my_card = _card

    def open_card(self, _card):
        self.common_card = _card

    def minimum_call(self):
        if self.check_bet is True:
            return 0
        else:
            return self.min_amount

    def _reset_list(self, _range):
        _list = []
        for _i in range(_range):
            _list.append(0)
        return _list

    def _reset_mark(self):
        self._mark_list = self._reset_list(4)

    def _collect_mark(self, _card):
        self._reset_mark()
        for i in _card:
            self._mark_list[i['mark']] += 1

    def _reset_num(self):
        self._num_list = self._reset_list(13)

    def _collect_num(self, _card):
        self._reset_num()
        for i in _card:
            self._num_list[i['num']] += 1

    def calculate_my_amount(self, _my_bet, _my_max):
        if self._max_amount <= _my_bet:
            amount = self._max_amount
        elif self._min_amount <= _my_bet <= self._max_amount:
            amount = _my_bet
        else:
            amount = self._min_amount
        if self._min_amount >= _my_max:
            amount = -1
        return amount

    def _check_my_card(self):
        _my_card = self.my_card + self.common_card
        self._collect_mark(_my_card)
        self._collect_num(_my_card)

    def _common_0(self):
        self._check_my_card()
        _my_bet = 0
        _my_max = 1000
        if 2 in self._mark_list or 2 in self._num_list:
            _my_bet = 1000
            _my_max = 3000
        return _my_bet, _my_max

    def _common_3(self):
        self._check_my_card()
        _my_bet = 0
        _my_max = 2000
        if 4 in self._num_list:
            _my_bet = 100000
            _my_max = 300000
        elif 5 in self._mark_list:
            _my_bet = 100000
            _my_max = 300000
        elif 2 in self._num_list and 3 in self._num_list:
            _my_bet = 100000
            _my_max = 300000
        elif 4 in self._mark_list:
            _my_bet = 10000
            _my_max = 30000
        elif self._num_list.count(2) == 2:
            _my_bet = 10000
            _my_max = 30000
        elif 2 in self._num_list:
            _my_bet = 1000
            _my_max = 3000
        return _my_bet, _my_max

    def _common_4(self):
        self._check_my_card()
        _my_bet = 0
        _my_max = 2000
        if 4 in self._num_list:
            _my_bet = 100000
            _my_max = 300000
        elif 5 in self._mark_list:
            _my_bet = 100000
            _my_max = 300000
        elif 2 in self._num_list and 3 in self._num_list:
            _my_bet = 100000
            _my_max = 300000
        elif 4 in self._mark_list:
            _my_bet = 10000
            _my_max = 30000
        elif self._num_list.count(2) == 2:
            _my_bet = 10000
            _my_max = 30000
        elif 2 in self._num_list:
            _my_bet = 1000
            _my_max = 3000
        return _my_bet, _my_max

    def _common_5(self):
        self._check_my_card()
        _my_bet = 0
        _my_max = 2000
        if 4 in self._num_list:
            _my_bet = 100000
            _my_max = 300000
        elif 5 in self._mark_list:
            _my_bet = 100000
            _my_max = 300000
        elif 2 in self._num_list and 3 in self._num_list:
            _my_bet = 100000
            _my_max = 300000
        elif self._num_list.count(2) == 2:
            _my_bet = 10000
            _my_max = 30000
        elif 2 in self._num_list:
            _my_bet = 1000
            _my_max = 3000
        return _my_bet, _my_max


    def decide_amount(self, min_amount, max_amount, check_bet):
        self._min_amount = min_amount
        self._max_amount = max_amount
        self._check_bet = check_bet

        if len(self.common_card) == 0:
            _my_bet, _my_max = self._common_0()
        elif len(self.common_card) == 3:
            _my_bet, _my_max = self._common_3()
        elif len(self.common_card) == 4:
            _my_bet, _my_max = self._common_4()
        elif len(self.common_card) == 5:
            _my_bet, _my_max = self._common_5()
        else:
            _my_bet, _my_max = self._common_0()

        amount = self.calculate_my_amount(_my_bet, _my_max)

        return amount



class just_call:
    def __init__(self):
        self.play_order = []
        self.my_card = []
        self.common_card = []
        self.others_behaviour = {}

    def your_card(self, card):
        self.my_card = card

    def open_card(self, card):
        self.common_card = card

    def decide_amount(self, min_amount, max_amount, check_bet):
        if check_bet is True:
            return 0
        else:
            return min_amount


class random_com:
    def __init__(self):
        self.play_order = []
        self.my_card = []
        self.common_card = []
        self.others_behaviour = {}

    def your_card(self, card):
        self.my_card = card

    def open_card(self, card):
        self.common_card = card

    def cal_posibility(self):
        return

    def decide_amount(self, min_amount, max_amount, check_bet):
        call_ratio = 60
        raise_ratio = 30
        raise2_ratio = 10

        call_num_list = []
        for i in range(0, call_ratio):
            call_num_list.append(i)

        raise_num_list = []
        for i in range(call_ratio, call_ratio+raise_ratio):
            raise_num_list.append(i)

        raise2_num_list = []
        for i in range(call_ratio+raise_ratio, call_ratio+raise_ratio+raise2_ratio):
            raise2_num_list.append(i)

        choise_num = random.randint(0,99)

        if choise_num in call_num_list:
            if check_bet is True:
                return 0
            else:
                return min_amount
        elif choise_num in raise_num_list:
            return min_amount + 100
        elif choise_num in raise2_num_list:
            amount = int(random.randint(min_amount, max_amount))
            return amount



