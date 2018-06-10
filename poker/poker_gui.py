#!/usr/bin/env python3.4
# -*- coding: utf-8 -*-
import math
import sys
import os
import time
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

import poker as poker_backend

card_fig_path = os.path.abspath(os.path.join('png'))
card_fig_ext = '.png'

class card(QLabel):
    def __init__(self, parent=None):
        super(QLabel, self).__init__(parent)
        self.card_name = None
        self.card_fig_path = ''
        self.card_geometry = [0, 0, 100, 200]
        self.card_width = 100
        self.card_rotate = 0

    def create_fig_path(self):
        if self.card_name is None:
            self.card_name = 'secret_card'
        self.fig_path = os.path.join(card_fig_path, self.card_name)+card_fig_ext

    def calculate_length(self, x, y, r):

        _rad = math.radians(r)
        _cos = math.cos(_rad)
        _sin = math.sin(_rad)
        pos_x_list = []
        pos_y_list = []
        for x_ori in [0, x]:
            for y_ori in [0, y]:
                pos_x = int(x_ori*_cos-y_ori*_sin)
                pos_y = int(x_ori*_sin + y_ori * _cos)
                pos_x_list.append(pos_x)
                pos_y_list.append(pos_y)

        width = max(pos_x_list)-min(pos_x_list)
        height = max(pos_y_list)-min(pos_y_list)

        return width, height

    def customize(self, x, y, w=100, h=200, r=0, card_name=None):
        self.card_name = card_name
        width, height = self.calculate_length(w, h, r)
        self.card_geometry = [x, y, width, height]
        self.card_width = w
        self.card_rotate = r
        self.set_fig()
        self.set_geometry()

    def set_geometry(self):
        self.setGeometry(*self.card_geometry)

    def set_fig(self):
        self.create_fig_path()
        _pixmap = QPixmap(self.fig_path)
        _pixmap = _pixmap.scaledToWidth(self.card_width)
        transform = QTransform().rotate(self.card_rotate)
        _pixmap = _pixmap.transformed(transform, Qt.SmoothTransformation)
        self.setPixmap(_pixmap)

    def change_fig(self, card_dict):
        card_mark = card_dict['mark']
        card_num = card_dict['num']
        self.card_name = str(card_mark) + '_' + str(card_num)
        self.set_fig()

    def change_fig_name(self, card_name):
        self.card_name = card_name
        self.set_fig()

class play_game(QThread):
    def __init__(self, start_game):
        QThread.__init__(self)
        self.start_game = start_game

    def run(self):
        self.start_game()

class poker_gui(QMainWindow):
    def __init__(self, parent=None):
        super(QMainWindow, self).__init__(parent)

        self.user_val = None
        self.human_number = 1
        self.computer_number = 3
        self.player_num = self.human_number + self.computer_number
        self.gui_item_list = []
        self.initUI()
        self.repare_game()
        self.timer = QTimer()
        self.timer.timeout.connect(self.item_update)
        self.timer.start(0.1)

        self.play_game = play_game(self.start_game)
        self.play_game.start()

    def closeEvent(self, event):
        self.play_game.quit()
        self.timer.stop()

    def initUI(self):
        mw_w = 1800
        mw_h = 900


        fig_path = os.path.join(card_fig_path, 'poker_hintergrund'+card_fig_ext)
        oImage = QImage(fig_path)
        sImage = oImage.scaled(QSize(mw_w, mw_h))
        palette = QPalette()
        palette.setBrush(10, QBrush(sImage))
        self.setPalette(palette)

        x_pos = int(mw_w/2-100*5/2)
        y_pos = int(mw_h/2-200/2)

        self.common_cards = []
        for i in range(5):
            new_card = card(self)
            new_card.customize(x_pos+100*i, y_pos, 100, 200, 0)
            self.common_cards.append(new_card)
            self.gui_item_list.append(new_card)

        self.common_score_0 = QLineEdit(self)
        self.common_score_0.setText('bet')
        self.common_score_0.setReadOnly(True)
        self.common_score_0.setGeometry(905, 300, 150, 70)
        self.common_score_0.setAlignment(Qt.AlignRight)
        font = self.common_score_0.font()
        font.setPointSize(20)
        self.common_score_0.setFont(font)
        self.gui_item_list.append(self.common_score_0)

        self.common_score_1 = QLineEdit(self)
        self.common_score_1.setText('amount')
        self.common_score_1.setReadOnly(True)
        self.common_score_1.setGeometry(745, 300, 150, 70)
        self.common_score_1.setAlignment(Qt.AlignRight)
        font = self.common_score_1.font()
        font.setPointSize(20)
        self.common_score_1.setFont(font)
        self.gui_item_list.append(self.common_score_1)


        self.common_score_2_0 = QLabel(self)
        self.common_score_2_0.setText('max')
        self.common_score_2_0.setGeometry(970, 530, 120, 50)
        self.common_score_2_0.setAlignment(Qt.AlignRight)
        font = self.common_score_2_0.font()
        font.setPointSize(16)
        self.common_score_2_0.setFont(font)
        self.gui_item_list.append(self.common_score_2_0)


        self.common_score_2_1 = QLabel(self)
        self.common_score_2_1.setText('min')
        self.common_score_2_1.setGeometry(840, 530, 120, 50)
        self.common_score_2_1.setAlignment(Qt.AlignRight)
        font = self.common_score_2_1.font()
        font.setPointSize(16)
        self.common_score_2_1.setFont(font)
        self.gui_item_list.append(self.common_score_2_1)

        self.common_score_2_2 = QLineEdit(self)
        self.common_score_2_2.setText('3?')
        self.common_score_2_2.setReadOnly(True)
        self.common_score_2_2.setGeometry(710, 560, 120, 50)
        self.common_score_2_2.setAlignment(Qt.AlignRight)
        font = self.common_score_2_2.font()
        font.setPointSize(16)
        self.common_score_2_2.setFont(font)
        self.common_score_2_2.hide()
        self.gui_item_list.append(self.common_score_2_2)


        self.common_score_2_3 = QLineEdit(self)
        self.common_score_2_3.setText('1?')
        self.common_score_2_3.setReadOnly(True)
        self.common_score_2_3.setGeometry(970, 560, 120, 50)
        self.common_score_2_3.setAlignment(Qt.AlignRight)
        font = self.common_score_2_3.font()
        font.setPointSize(16)
        self.common_score_2_3.setFont(font)
        self.gui_item_list.append(self.common_score_2_3)


        self.common_score_2_4 = QLineEdit(self)
        self.common_score_2_4.setText('2?')
        self.common_score_2_4.setReadOnly(True)
        self.common_score_2_4.setGeometry(840, 560, 120, 50)
        self.common_score_2_4.setAlignment(Qt.AlignRight)
        font = self.common_score_2_4.font()
        font.setPointSize(16)
        self.common_score_2_4.setFont(font)
        self.gui_item_list.append(self.common_score_2_4)


        self.player_cards = []
        for i in range(self.player_num):
            player_card = []
            for i2 in range(2):
                new_card = card(self)
                player_card.append(new_card)
                self.gui_item_list.append(new_card)
            self.player_cards.append(player_card)
        self.player_cards[0][0].customize(800, 700, 100, 200, 0)
        self.player_cards[0][1].customize(900, 700, 100, 200, 0)

        self.player_cards[1][0].customize(1600, 350, 100, 200, 270)
        self.player_cards[1][1].customize(1600, 450, 100, 200, 270)

        self.player_cards[2][0].customize(800, 10, 100, 200, 180)
        self.player_cards[2][1].customize(900, 10, 100, 200, 180)

        self.player_cards[3][0].customize(100, 350, 100, 200, 90)
        self.player_cards[3][1].customize(100, 450, 100, 200, 90)


        self.player_scores = []
        for i in range(self.player_num):
            player_score = QLineEdit(self)
            player_score.setText('0')
            player_score.setAlignment(Qt.AlignRight)
            player_score.setReadOnly(True)
            font = player_score.font()
            font.setPointSize(16)
            player_score.setFont(font)
            self.player_scores.append(player_score)

        self.player_scores[0].setGeometry(650, 755, 150, 35)
        self.player_scores[1].setGeometry(1505, 415, 95, 35)
        self.player_scores[2].setGeometry(1080, 65, 120, 35)
        self.player_scores[3].setGeometry(330, 415, 130, 35)
        self.gui_item_list.append(player_score)

        self.player_names = []
        for i in range(self.player_num):
            player_name = QLabel(self)
            font = player_name.font()
            font.setPointSize(16)
            player_name.setFont(font)
            self.player_names.append(player_name)

        self.player_names[0].setText('player_zero')
        self.player_names[0].setGeometry(805, 690, 150, 35)
        self.player_names[0].setAlignment(Qt.AlignRight)
        self.player_names[1].setText('player_one')
        self.player_names[1].setGeometry(1500, 315, 200, 35)
        self.player_names[1].setAlignment(Qt.AlignRight)
        self.player_names[2].setText('player_two')
        self.player_names[2].setGeometry(800, 0, 200, 35)
        self.player_names[2].setAlignment(Qt.AlignLeft)
        self.player_names[3].setText('player_three')
        self.player_names[3].setGeometry(100, 315, 150, 35)
        self.player_names[3].setAlignment(Qt.AlignRight)
        self.gui_item_list.append(player_name)

        self.player_besten_liste = []
        for i in range(self.player_num):
            player_besten = QLabel(self)
            player_besten.setText('')
            font = player_besten.font()
            font.setPointSize(16)
            player_besten.setFont(font)
            self.player_besten_liste.append(player_besten)

        self.player_besten_liste[0].setGeometry(550, 840, 250, 35)
        self.player_besten_liste[0].setAlignment(Qt.AlignRight)
        self.player_besten_liste[1].setGeometry(1350, 505, 250, 35)
        self.player_besten_liste[1].setAlignment(Qt.AlignRight)
        self.player_besten_liste[2].setGeometry(1000, 150, 250, 35)
        self.player_besten_liste[2].setAlignment(Qt.AlignLeft)
        self.player_besten_liste[3].setGeometry(250, 505, 250, 35)
        self.player_besten_liste[3].setAlignment(Qt.AlignLeft)
        self.gui_item_list.append(player_besten)

        self.player_results = []
        for i in range(self.player_num):
            player_result = QLabel(self)
            player_result.setText('0')
            font = player_result.font()
            font.setPointSize(16)
            player_result.setFont(font)
            self.player_results.append(player_result)

        self.player_results[0].setGeometry(650, 795, 150, 35)
        self.player_results[0].setAlignment(Qt.AlignRight)
        self.player_results[1].setGeometry(1450, 460, 150, 35)
        self.player_results[1].setAlignment(Qt.AlignRight)
        self.player_results[2].setGeometry(1000, 120, 150, 35)
        self.player_results[2].setAlignment(Qt.AlignLeft)
        self.player_results[3].setGeometry(250, 460, 150, 35)
        self.player_results[3].setAlignment(Qt.AlignLeft)
        self.gui_item_list.append(player_result)

        self.player_0_score_0 = QLabel(self)
        self.player_0_score_0.setText('Amount'+':')
        self.player_0_score_0.setGeometry(650, 720, 150, 35)
        self.player_0_score_0.setAlignment(Qt.AlignRight)
        font = self.player_0_score_0.font()
        font.setPointSize(16)
        self.player_0_score_0.setFont(font)
        self.gui_item_list.append(self.player_0_score_0)

        self.player_0_check_0 =  QPushButton('Check', self)
        self.player_0_check_0.setGeometry(1000, 720, 80, 40)
        self.player_0_check_0.clicked.connect(self.player_0_check)
        self.gui_item_list.append(self.player_0_check_0)

        self.player_0_check_1 = QLineEdit(self)
        self.player_0_check_1.setText('0')
        self.player_0_check_1.setReadOnly(True)
        self.player_0_check_1.setGeometry(1080, 720, 80, 40)
        self.player_0_check_1.setAlignment(Qt.AlignRight)
        font = self.player_0_check_1.font()
        font.setPointSize(15)
        self.player_0_check_1.setFont(font)
        self.player_0_check_1.hide()
        self.gui_item_list.append(self.player_0_check_1)

        self.player_0_call_0 =  QPushButton('Call', self)
        self.player_0_call_0.setGeometry(1000, 760, 80, 40)
        self.player_0_call_0.clicked.connect(self.player_0_call)
        self.gui_item_list.append(self.player_0_call_0)

        self.player_0_call_1 = QLineEdit(self)
        self.player_0_call_1.setText('0')
        self.player_0_call_1.setReadOnly(True)
        self.player_0_call_1.setGeometry(1080, 760, 80, 40)
        self.player_0_call_1.setAlignment(Qt.AlignRight)
        font = self.player_0_call_1.font()
        font.setPointSize(15)
        self.player_0_call_1.setFont(font)
        self.player_0_call_1.hide()
        self.gui_item_list.append(self.player_0_call_1)

        self.player_0_raise_0 =  QPushButton('Raise', self)
        self.player_0_raise_0.setGeometry(1000, 800, 80, 40)
        self.player_0_raise_0.clicked.connect(self.player_0_raise)
        self.gui_item_list.append(self.player_0_raise_0)

        self.player_0_raise_1 = QSpinBox(self)
        self.player_0_raise_1.setGeometry(1080, 800, 80, 40)
        self.player_0_raise_1.setAlignment(Qt.AlignRight)
        font = self.player_0_raise_1.font()
        font.setPointSize(13)
        self.player_0_raise_1.setFont(font)
        self.player_0_raise_1.setSingleStep(100)
        self.gui_item_list.append(self.player_0_raise_1)

        self.player_0_fold =  QPushButton('Fold', self)
        self.player_0_fold.setGeometry(1000, 840, 80, 40)
        self.player_0_fold.clicked.connect(self.player_fold)
        self.gui_item_list.append(self.player_0_fold)

        self.player_2_score_0 = QLabel(self)
        self.player_2_score_0.setText('Amount'+':')
        self.player_2_score_0.setGeometry(930, 70, 150, 35)
        self.player_2_score_0.setAlignment(Qt.AlignRight)
        font = self.player_2_score_0.font()
        font.setPointSize(16)
        self.player_2_score_0.setFont(font)
        self.gui_item_list.append(self.player_2_score_0)

        self.player_3_score_0 = QLabel(self)
        self.player_3_score_0.setText('Amount'+':')
        self.player_3_score_0.setGeometry(235, 420, 95, 35)
        self.player_3_score_0.setAlignment(Qt.AlignRight)
        font = self.player_3_score_0.font()
        font.setPointSize(16)
        self.player_3_score_0.setFont(font)
        self.gui_item_list.append(self.player_3_score_0)

        self.player_1_score_0 = QLabel(self)
        self.player_1_score_0.setText('Amount '+':')
        self.player_1_score_0.setGeometry(1350, 415, 150, 35)
        self.player_1_score_0.setAlignment(Qt.AlignRight)
        font = self.player_1_score_0.font()
        font.setPointSize(16)
        self.player_1_score_0.setFont(font)
        self.gui_item_list.append(self.player_1_score_0)


        self.layout = QVBoxLayout(self)
        for i in range(5):
            self.layout.addWidget(self.common_cards[i])

        self.layout.addWidget(self.common_score_0)
        self.layout.addWidget(self.common_score_1)
        self.layout.addWidget(self.common_score_2_0)
        self.layout.addWidget(self.common_score_2_1)
        self.layout.addWidget(self.common_score_2_2)
        self.layout.addWidget(self.common_score_2_3)
        self.layout.addWidget(self.common_score_2_4)

        self.layout.addWidget(self.player_cards[0][0])
        self.layout.addWidget(self.player_cards[0][1])

        self.layout.addWidget(self.player_0_check_0)
        self.layout.addWidget(self.player_0_check_1)
        self.layout.addWidget(self.player_0_call_0)
        self.layout.addWidget(self.player_0_call_1)
        self.layout.addWidget(self.player_0_raise_0)
        self.layout.addWidget(self.player_0_raise_1)
        self.layout.addWidget(self.player_0_fold)

        self.layout.addWidget(self.player_besten_liste[0])
        self.layout.addWidget(self.player_besten_liste[1])
        self.layout.addWidget(self.player_besten_liste[2])
        self.layout.addWidget(self.player_besten_liste[3])

        self.layout.addWidget(self.player_results[0])
        self.layout.addWidget(self.player_results[1])
        self.layout.addWidget(self.player_results[2])
        self.layout.addWidget(self.player_results[3])

        self.layout.addWidget(self.player_names[0])
        self.layout.addWidget(self.player_names[1])
        self.layout.addWidget(self.player_names[2])
        self.layout.addWidget(self.player_names[3])

        self.layout.addWidget(self.player_scores[0])
        self.layout.addWidget(self.player_scores[1])
        self.layout.addWidget(self.player_scores[2])
        self.layout.addWidget(self.player_scores[3])


        self.layout.addWidget(self.player_cards[1][0])
        self.layout.addWidget(self.player_cards[1][1])

        self.layout.addWidget(self.player_cards[2][0])
        self.layout.addWidget(self.player_cards[2][1])
        self.layout.addWidget(self.player_cards[3][0])
        self.layout.addWidget(self.player_cards[3][1])
        self.setLayout(self.layout)

        self.setGeometry(50, 50, mw_w, mw_h)
        self.setWindowTitle('Poker')
        self.show()

    def item_update(self):
##        self.update()
        pass

    def player_0_check(self):
        self.user_val = 0

    def player_0_call(self):
        self.user_val = int(self.player_0_call_1.text())

    def player_0_raise(self):
        self.user_val = int(self.player_0_raise_1.text())

    def player_fold(self):
        self.user_val = -1

    def repare_game(self):

        self.selected_card_list, self.common_card_list, self.player_class_list, self.player_number = \
                poker_backend.create_game(self.human_number, self.computer_number)

        for i in range(5):
            self.common_cards[i].change_fig_name('secret_card')

        for i in range(self.player_num):
            for i2 in range(2):
                self.player_cards[i][i2].change_fig_name('secret_card')

    def user_choise(self, player_name, selected_card, open_common_card,
                    min_bet, max_bet, check_bet, complay):
        self.common_score_0.setText(str(min_bet))       # amount in this turn
        self.common_score_1.setText('0')                # total amount in this game
        self.common_score_2_2.setText(str(check_bet))   # True or False
        self.common_score_2_3.setText(str(max_bet))     # max bet
        self.common_score_2_4.setText(str(min_bet))     # min bet


        for i in range(len(open_common_card)):
            self.common_cards[i].change_fig(open_common_card[i])

        selected_amount = min_bet
        if player_name == 0:
            self.player_0_check_0.setEnabled(False)     # check button. player 0
            self.player_0_call_0.setEnabled(False)      # call button. player 0
            self.player_0_raise_0.setEnabled(False)     # raise button. player 0
            self.player_0_raise_1.setEnabled(False)     # raise value. player 0
            self.player_0_fold.setEnabled(False)        # fold button. player 0
            self.player_0_check_1.setText('0')          # check amount. player 0
            self.player_0_call_1.setText(str(min_bet))  # call amount. player 0
            self.player_0_raise_1.setMinimum(min_bet+1) # raise min. player 0
            self.player_0_raise_1.setMaximum(max_bet)   # raise max. player 0
            self.player_0_raise_1.setValue(max_bet)   # raise def. player 0

            if check_bet:
                self.player_0_check_0.setEnabled(True)     # check button. player 0

            self.player_0_call_0.setEnabled(True)      # call button. player 0

            if min_bet != max_bet:
                self.player_0_raise_0.setEnabled(True)     # raise button. player 0
                self.player_0_raise_1.setEnabled(True)     # raise value. player 0

            self.player_0_fold.setEnabled(True)        # fold button. player


            self.player_names[0].setStyleSheet('color: rgb(153, 0, 204)')
            self.user_val = None
            while self.user_val == None:
                time.sleep(0.1)

            self.player_names[0].setStyleSheet('color: rgb(0,0,0)')

            self.player_0_check_0.setEnabled(False)     # check button. player 0
            self.player_0_call_0.setEnabled(False)      # call button. player 0
            self.player_0_raise_0.setEnabled(False)     # raise button. player 0
            self.player_0_raise_1.setEnabled(False)     # raise value. player 0
            self.player_0_fold.setEnabled(False)        # fold button. player 0

            selected_amount = self.user_val

        else:
            complay.my_card = selected_card
            complay.common_card = open_common_card
            amount = complay.decide_amount(min_bet, max_bet, check_bet)

            if player_name == 1:
                self.player_names[1].setStyleSheet('color: rgb(153, 0, 204)')
            elif player_name == 2:
                self.player_names[2].setStyleSheet('color: rgb(153, 0, 204)')
            elif player_name == 3:
                self.player_names[3].setStyleSheet('color: rgb(153, 0, 204)')


            for _i in range(10):
                time.sleep(0.1)

            if player_name == 1:
                self.player_names[1].setStyleSheet('color: rgb(0,0,0)')
            elif player_name == 2:
                self.player_names[2].setStyleSheet('color: rgb(0,0,0)')
            elif player_name == 3:
                self.player_names[3].setStyleSheet('color: rgb(0,0,0)')


            selected_amount = amount

        if selected_amount == -1:
            for i2 in range(2):
                self.player_cards[player_name][i2].change_fig_name('fold_card')

        self.player_results[player_name].setText(str(selected_amount))

        return selected_amount

    def start_game(self):
        player = 0
        for i2 in range(2):
            self.player_cards[player][i2].change_fig(self.selected_card_list[player][i2])

        bet_amount_list = poker_backend.start_game(
            self.selected_card_list, self.common_card_list,
            self.player_class_list, self.user_choise)

        player_payment, total_amount = poker_backend.calculate_balance(
            self.player_number,bet_amount_list)

        winner_list, winner_card, winner_amount, balance_list, besten_liste = \
            poker_backend.show_detail(
                self.selected_card_list, self.common_card_list, total_amount,
                player_payment, self.player_number)

        print(player_payment)
        print(total_amount)
        print(self.selected_card_list)
        print()

        print()
        print(str(winner_list)+ 'winner!!!')
        print('winner card' + str(winner_card))
        print('winner_amount:' + str(winner_amount))
        print('balance:')
        for i in range(self.player_number):
            print('   player ' +str(i)+': '+str(balance_list[i]))

        self.player_scores[0].setText(str(balance_list[0])) # balance player 0
        self.player_scores[1].setText(str(balance_list[1])) # balance player 1
        self.player_scores[2].setText(str(balance_list[2])) # balance player 2
        self.player_scores[3].setText(str(balance_list[3])) # balance player 3


        print('winner_list')
        if 0 in winner_list:
            self.player_besten_liste[0].setStyleSheet('color: rgb(199,143,0)')
        elif 1 in winner_list:
            self.player_besten_liste[1].setStyleSheet('color: rgb(199,143,0)')
        elif 2 in winner_list:
            self.player_besten_liste[2].setStyleSheet('color: rgb(199,143,0')
        elif 3 in winner_list:
            self.player_besten_liste[3].setStyleSheet('color: rgb(199,143,0)')

        fold_count = self.selected_card_list.count(False)

        print('besten_liste')

        for i in range(self.player_num):
            besten_liste_0 = besten_liste[i][0]
            besten_liste_1 = poker_backend.num_convert[besten_liste[i][2]]

            if self.selected_card_list[i] is not False:
                if fold_count+1 < self.player_num:
                    for i2 in range(2):
                        self.player_cards[i][i2].change_fig(self.selected_card_list[i][i2])

                    besten_liste_show = ' ' + str(besten_liste_0) + ' (' +\
                                        str(besten_liste_1) + ') '
                else:
                    besten_liste_show = ' ' + 'Secret!'
            else:
                besten_liste_show =  ' ' + str(besten_liste_0) + ' '

            self.player_besten_liste[i].setText(besten_liste_show)

        print('end')

def main():
    app = QApplication(sys.argv)
    exec = poker_gui()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()