#!/usr/bin/env python3.4
# -*- coding: utf-8 -*-


import com_henrik
import com_kaz

import random


num_convert = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K',
               'A']
mark_convert = ['herz', 'caro', 'peak', 'kreuz']


def load_card():
    card_set = []
    for i in range(len(num_convert)):
        for i2 in range(len(mark_convert)):
            card_set.append({'num':i, 'mark':i2})
    return card_set


def choose_card(card, choosed_num):
    max_num = len(card)
    result = []
    while True:
        random_num = random.randint(0, max_num-1)

        result_temp = result[:]
        result_temp.append(random_num)
        result_temp_without_duplication = list(set(result_temp))

        if len(result_temp) == len(result_temp_without_duplication):
            result.append(random_num)

        if len(result) == choosed_num:
            break

    choose_card_list = []
    for i in result:
        choose_card_list.append(card[i])

    return choose_card_list


def check_pair(selected_card):
    num_list = []
    for i in selected_card:
        num_list.append(i['num'])

    count_list = []
    for i in num_list:
        count = 0
        for i2 in num_list:
            if i == i2:
                count = count + 1
        count_list.append(count)

    sorted_count_list = sorted(count_list)

    if sorted_count_list == [1,1,1,1,1]:
        patern = 'no pair'
    elif sorted_count_list == [1,1,1,2,2]:
        patern = 'one pair'
    elif sorted_count_list == [1,2,2,2,2]:
        patern = 'two pair'
    elif sorted_count_list == [2,2,3,3,3]:
        patern = 'full house'
    elif sorted_count_list == [1,1,3,3,3]:
        patern = 'three of a kind'
    elif sorted_count_list == [1,4,4,4,4]:
        patern = 'four of a kind'
    high_num = 0
    max_num = sorted_count_list[-1]
    for i in range(len(count_list)):
        if max_num == count_list[i]:
            if high_num < num_list[i]:
                high_num = num_list[i]

    return patern, high_num


def check_mark(selected_card):
    mark_list = []
    for i in selected_card:
        mark_list.append(i['mark'])

    count_list = []
    for i in mark_list:
        count = 0
        for i2 in mark_list:
            if i == i2:
                count = count + 1
        count_list.append(count)

    sorted_count_list = sorted(count_list)

    patern = 'no flush'
    if sorted_count_list == [5,5,5,5,5]:
        patern = 'flush'

    return patern



def check_streat(selected_card):
    num_list = []
    for i in selected_card:
        num_list.append(i['num'])

    sorted_num_list= sorted(num_list)

    streat = 'no streat'
    for i in range(10):
        streat_patern = []
        for i2 in range(5):
            streat_patern.append(i2+i)
        if streat_patern == sorted_num_list:
            streat = 'streat'

    return streat


def check_best(pair, mark, streat):
    best = 'high_card'
    rank = 0
    # straight_flush
    if mark == 'flush' and streat == 'streat':
        best = 'straight_flush'
        rank = 8
    elif pair == 'four of a kind':
        best = 'four of a kind'
        rank = 7
    elif pair == 'full house':
        best = 'full house'
        rank = 6
    elif mark == 'flush':
        best = 'flush'
        rank = 5
    elif streat == 'streat':
        best = 'streat'
        rank = 4
    elif pair == 'three of a kind':
        best = 'three of a kind'
        rank =3
    elif pair == 'two pair':
        best = 'two pair'
        rank = 2
    elif pair == 'one pair':
        best = 'one pair'
        rank = 1

    return best, rank


def decide_strong(selected_card):
    pair, pair_high = check_pair(selected_card)
    mark = check_mark(selected_card)
    streat = check_streat(selected_card)
    best, rank = check_best(pair, mark, streat)
    return best, rank, pair_high


def player_selected_card(play_num):
    card = load_card()

    one_person = 2
    player_card = one_person*play_num
    common_card = 5
    total_num = player_card + common_card

    selected_card = choose_card(card, total_num)
    selected_card_list = []
    for i in range(play_num):
        player_card_list = []
        for i2 in range(one_person):
            card_pos = i * one_person + i2
            player_card_list.append(selected_card[card_pos])
        selected_card_list.append(player_card_list)

    common_card_list = selected_card[player_card : total_num]

    return selected_card_list, common_card_list


def rank_player(selected_card_list):
    player_best_list = []
    for i in selected_card_list:
        if i != False:
            best, rank, pair_high = decide_strong(i)
        else:
            best, rank, pair_high = False, -1, -1

        player_best_list.append([best, rank, pair_high])

    player_best_list_no_duplicate = []
    for i in player_best_list:
        if not i in player_best_list_no_duplicate:
            player_best_list_no_duplicate.append(i)

    sorted_player_best_list = sorted(player_best_list_no_duplicate,
                                     key = lambda x: (x[1], x[2]),
                                     reverse=True)

    rank_player_list = []
    for i in player_best_list:
        num = 0
        for i2 in sorted_player_best_list:
            if i == i2:
                rank_player_list.append(num)
            num = num + 1

    return rank_player_list


def strongest_card(player_card, common_card_list):

    all_card = player_card + common_card_list

    combination_card_list = []
    total_num = len(all_card)
    for i in range(total_num):
        for i2 in range(i+1, total_num):
            for i3 in range(i2+1, total_num):
                for i4 in range(i3+1, total_num):
                    for i5 in range(i4+1, total_num):
                        combination_card_list.append(
                            [all_card[i], all_card[i2], all_card[i3],
                             all_card[i4], all_card[i5]])


    rank_player_list = rank_player(combination_card_list)

    strongest_player_card = []
    num = 0
    for i in rank_player_list:
        if rank_player_list[num] == 0:
            strongest_player_card = combination_card_list[num]
        num += 1

    return strongest_player_card


def all_player(selected_card_list, common_card_list):
##    import pprint
    strongest_player_list = []
    besten_liste = []
    for i in selected_card_list:
        if i != False:
            strongest_player_card = strongest_card(i, common_card_list)
            strongest_player_list.append(strongest_player_card)
            besten_liste.append(decide_strong(strongest_player_card))
        else:
            strongest_player_list.append(False)
            besten_liste.append(('Fold', -1, -1))

##    pprint.pprint(strongest_player_list)
##    pprint.pprint(besten_liste)

    rank_player_list = rank_player(strongest_player_list)
##    pprint.pprint(rank_player_list)

    return strongest_player_list, besten_liste, rank_player_list


def input_integer(display):
    while True:
        _input = input(display)
        try:
            int_input = int(_input)
            print('int')
            return int_input
        except:
            print('not int')
            pass


def convert_display(card_dict_list):
    card_str_list = []
    for card_dict in card_dict_list:
        num = num_convert[card_dict['num']]
        mark = mark_convert[card_dict['mark']]
        card_str_list.append(num + '_' + mark)

    return card_str_list


def user_choise(player_name, selected_card, open_common_card, min_bet,
                max_bet, check_bet, complay):
    if complay is False:
        # human part
        fold_comment = '  (-1 -> Fold)'
        min_max_comment = str(min_bet) + '-' + str(max_bet) + fold_comment
        same_value_comment = str(min_bet) + fold_comment
        if check_bet == True and min_bet != max_bet:
            bet_comment = 'bet: ' + '0 or ' + min_max_comment
        elif min_bet != max_bet:
            bet_comment = 'bet: ' + min_max_comment
        elif check_bet == True:
            bet_comment = 'bet: ' + '0 or ' + same_value_comment
        else:
            bet_comment = 'bet: ' + same_value_comment
        while True:
            _input = input('player ' + str(player_name)+': \n' +
                           '\n' +
                           str(convert_display(selected_card)) + '\n' +
                           '\n' +
                           str(convert_display(open_common_card)) + '\n' +
                           '\n' +
                           bet_comment)
            try:
                int_input = int(_input)
                if int_input == -1 or \
                   min_bet <= int_input <= max_bet or \
                   check_bet == True and int_input == 0:
                    return int_input
            except:
                print('not int')
                pass
    else:
        # com part
        complay.my_card = selected_card
        complay.common_card = open_common_card
        amount = complay.decide_amount(min_bet, max_bet, check_bet)
        return  amount


def stand_player(selected_card_list):
    stand_player_list = []
    for i in range(len(selected_card_list)):
        if selected_card_list[i] != False:
            stand_player_list.append(i)
    return stand_player_list


def play_game(selected_card_list, open_common_card, mem_bet, start_player,
              player_class_list, _user_choise):
    check_bet = True
    player_number = len(selected_card_list)
    raise_player = []
    for i in range(player_number):
        raise_player.append(False)

    start_pos = start_player

    stand_player_list = stand_player(selected_card_list)
    pos_before_start_player = stand_player_list[
        stand_player_list.index(start_player)-1]

    for i in stand_player_list:
        raise_player[i] = True

    pos_last_player = player_number - 1

    if pos_last_player == -1:
        pos_last_player = player_number -1


    bet_amount = []
    for i in range(player_number):
        bet_amount.append(0)

    while True:
        contnue_game = True
        for i in range(start_pos, player_number):
            stand_player_list = stand_player(selected_card_list)
            if len(stand_player_list) == 1:
                contnue_game = False
                break

            if selected_card_list[i] == False:
                continue

            if raise_player[i] == True:
                max_bet = mem_bet * 3
            else:
                max_bet = mem_bet

            player_class = player_class_list[i]
            if player_class is False:
                complay = False
            else:
                complay = player_class

            bet_num = _user_choise(i, selected_card_list[i], open_common_card,
                                  mem_bet, max_bet, check_bet, complay)

            if bet_num == -1:
                selected_card_list[i] = False
                raise_player[i] = False

            if bet_num >= 1:
                if mem_bet ==bet_num and check_bet == False:
                    raise_player[i] = False
                mem_bet = bet_num
                check_bet = False


                bet_amount[i] = bet_num

            elif check_bet == True and bet_num <= 0 and \
                 i == pos_before_start_player:
                for i2 in range(player_number):
                    raise_player[i2] = False


                player_list = []
                for i2 in range(start_player, player_number):
                    player_list.append(i2)
                for i2 in range(0, start_player):
                    player_list.append(i2)
                for i2 in player_list:
                    if selected_card_list[i2] !=False:
                        raise_player[i2] = True
                        break

            if raise_player.count(True) == 1:
                pos_last_raise = raise_player.index(True)

                pos_last_player = stand_player_list[
                    stand_player_list.index(pos_last_raise)-1]

                if pos_last_player == -1:
                    pos_last_player = player_number - 1
                if i == pos_last_player:
                    contnue_game = False
                    break
        if contnue_game == False:
            break
        start_pos = 0

    if raise_player.count(True) == 1:
        pos_last_raise = raise_player.index(True)

    return selected_card_list, mem_bet, pos_last_raise, bet_amount


def create_game(human_number, computer_number):
    hum_list = []
    for i in range(human_number):
        hum_list.append(False)

    com_list = []
    for i in range(computer_number):
        if i == 0:
            com = com_kaz.kaz_com()
        elif i == 1:
            com = com_henrik.henrik_com()
        else:
            com = com_henrik.just_call()
        com_list.append(com)

    player_class_list = hum_list + com_list

##    import pprint
##    pprint.pprint(player_class_list)

    player_number = human_number + computer_number

    selected_card_list, common_card_list = player_selected_card(player_number)

    return selected_card_list, common_card_list, player_class_list, \
           player_number


def start_game(selected_card_list, common_card_list, player_class_list, _user_choise):
    mem_bet = 100
    start_player = 0
    bet_amount_list =[]
    for open_common_card in [[], common_card_list[0:3], common_card_list[0:4],
                             common_card_list]:
        selected_card_list, mem_bet, start_player, bet_amount = play_game(
            selected_card_list, open_common_card, mem_bet, start_player,
            player_class_list, _user_choise)

##        print(bet_amount)
        bet_amount_list.append(bet_amount)

    return bet_amount_list


def calculate_balance(player_number, bet_amount_list):
    player_payment = []
    for i in range(player_number):
        player_payment.append(0)
    total_amount = 0
    for i in bet_amount_list:
        for i2 in range(player_number):
            player_payment[i2] += i[i2]
            total_amount += i[i2]
    return player_payment, total_amount


def show_detail(selected_card_list, common_card_list, total_amount, player_payment, player_number):
    stand_player_list = stand_player(selected_card_list)

    winner_list = []
    winner_card = 'secret'
    strongest_player_list, besten_liste, rank_player_list = all_player(
        selected_card_list, common_card_list)
    if len(stand_player_list) >= 2:
        for i in range(len(rank_player_list)):
            if rank_player_list[i] == 0:
                winner_list.append(i)
        winner_card = besten_liste[winner_list[0]]
    elif len(stand_player_list) == 1:
        winner_list.append(stand_player_list[0])

    winner_amount = int(total_amount/len(winner_list))

    get_money = []
    for i in range(player_number):
        get_money.append(0)
        if i in winner_list:
            get_money[i] += winner_amount

    balance_list = []
    for i in range(player_number):
        balance = get_money[i] - player_payment[i]
        balance_list.append(balance)

    return winner_list, winner_card, winner_amount, balance_list, besten_liste


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



if __name__ == '__main__':
    human_number = input_integer('player_number')
    computer_number = input_integer('computer_number')
##    human_number = 1
##    computer_number = 2
##
##    player_total_amount = []
##    player_total_win = []
##    for i in range(human_number+computer_number):
##        player_total_amount.append(0)
##        player_total_win.append(0)

##    for i in range(1000):
##        if i % 1000 == 0:
##            print(i)

    selected_card_list, common_card_list, player_class_list, player_number = \
            create_game(human_number, computer_number)

    bet_amount_list = start_game(selected_card_list, common_card_list,
                                 player_class_list, user_choise)


    player_payment, total_amount = calculate_balance(player_number,
                                                         bet_amount_list)

    winner_list, winner_card, winner_amount, balance_list, besten_liste = show_detail(
            selected_card_list, common_card_list, total_amount, player_payment, player_number)


    print(player_payment)
    print(total_amount)
    print()

    print()
    print()
    print(besten_liste)
    print(str(winner_list)+ 'winner!!!')
    print('winner card' + str(winner_card))
    print('winner_amount:' + str(winner_amount))
    print('balance:')
    for i in range(player_number):
        print('   player ' +str(i)+': '+str(balance_list[i]))

##        for i in range(player_number):
##            print(balance_list[i])
##            player_total_amount[i] += balance_list[i]
##
##        score = int(1/len(winner_list)*100)/100
##        for i in winner_list:
##            player_total_win[i] += score

##    print()
##    print(player_total_amount)
##    print(player_total_win)




