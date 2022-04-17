import random

import numpy as np

from betting import OpenerBetting, DealerBetting
from colorama import Fore, Back, Style

from data_structures import SimpleAIData, BluffingAIData


class Playable:
    options_normal = ["b", "c", "f"]
    options_on_bet = ["b", "f"]
    default_color = "\033[0;0m"

    def __init__(self, name="No Name", initial_balance=10000, relative_balance=0, betting_amount=1,
                 use_relative_balance=True, text_color=Style.RESET_ALL):
        self.text_color = text_color
        self.name = name

        self.card = None
        self.betting_amount = betting_amount
        self.balance_history = []
        self.options = self.options_normal

        self.balance = initial_balance
        self.initial_balance = initial_balance
        self.relative_balance = relative_balance
        self.use_relative_balance = use_relative_balance

    def set_text_color(self, new_color):
        self.text_color = new_color

    def get_balance(self):
        if self.use_relative_balance:
            return self.relative_balance
        return self.balance

    def check_balance(self):
        if self.use_relative_balance:
            return True
        return self.balance - self.betting_amount >= 0

    def bet(self):
        if self.use_relative_balance:
            self.relative_balance -= self.betting_amount
            return self.betting_amount

        if self.check_balance():
            self.balance -= self.betting_amount
            return self.betting_amount
        return 0

    def win(self, amount):
        if self.use_relative_balance:
            self.relative_balance += amount
        else:
            self.balance += amount

    def set_card(self, card):
        self.card = card

    def reset(self):
        if self.use_relative_balance:
            self.relative_balance = 0
        else:
            self.balance = self.initial_balance

        self.card = None
        self.balance_history = []

    def record_balance_change(self):
        if self.use_relative_balance:
            self.balance_history.append(self.relative_balance)
        else:
            self.balance_history.append(self.balance)

    def play(self):
        pass

    def play_opener(self, opponent_choice):
        pass

    def play_dealer(self, opponent_choice):
        pass

    def play_opener_choice_on_dealer_bet(self, opponent_choice):
        pass


class Player(Playable):
    def __init__(self, name="No Name", initial_balance=10000, relative_balance=0, betting_amount=1,
                 use_relative_balance=True, print_help=True, text_color="default"):
        super().__init__(name, initial_balance, relative_balance, betting_amount, use_relative_balance, text_color)
        self.print_help = print_help

    def play(self):
        while True:
            print(self.card)
            if self.print_help:
                print("b - bet (or call), c - check, f - fold")
            inp = input(">>> ").strip().lower()
            if inp in self.options:
                return inp
            else:
                print("Invalid command!")

    def play_opener(self, opponent_choice):
        self.options = self.options_normal
        return self.play()

    def play_dealer(self, opponent_choice):
        self.options = self.options_normal
        if opponent_choice == "b":
            self.options = self.options_on_bet
        return self.play()

    def play_opener_choice_on_dealer_bet(self, opponent_choice):
        self.options = self.options_on_bet
        return self.play()

    def reset(self):
        if self.use_relative_balance:
            self.relative_balance = 0
        else:
            self.balance = self.initial_balance

        self.card = None
        self.balance_history = []
        self.options = self.options_normal


class RandomAI(Playable):
    def play_opener(self, opponent_choice=None):
        return random.choice(self.options_normal)

    def play_dealer(self, opponent_choice):
        if opponent_choice == "c":
            return random.choice(self.options_normal)
        elif opponent_choice == "b":
            return random.choice(self.options_on_bet)

    def play_opener_choice_on_dealer_bet(self, opponent_choice):
        if opponent_choice == "c":
            return random.choice(self.options_normal)
        elif opponent_choice == "b":
            return random.choice(self.options_on_bet)


class SimpleAI(Playable):
    def __init__(self, name="No Name", initial_balance=10000, relative_balance=0, betting_amount=1,
                 use_relative_balance=True, text_color="default", data_path="simple_ai_data.txt"):
        super().__init__(name, initial_balance, relative_balance, betting_amount, use_relative_balance, text_color)

        self.structured_data = SimpleAIData(data_path)

    def play_opener(self, opponent_choice=None):
        if self.card.value == 1:
            return "c"
        elif self.card.value == 2:
            return "c"
        elif self.card.value == 3:
            return "b"

    def play_dealer(self, opponent_choice):
        if self.card.value == 1:
            return "f"
        elif self.card.value == 2:
            if opponent_choice == "c":
                return "c"
            elif opponent_choice == "b":
                return "f"
        elif self.card.value == 3:
            return "b"

    def play_opener_choice_on_dealer_bet(self, opponent_choice):
        if self.card.value == 1:
            return "f"
        elif self.card.value == 2:
            return "f"
        elif self.card.value == 3:
            return "b"


class BluffingAI(Playable):
    def __init__(self, name="No Name", initial_balance=10000, relative_balance=0, betting_amount=1,
                 use_relative_balance=True, text_color="default", data_path="bluffing_ai_data.txt"):
        super().__init__(name, initial_balance, relative_balance, betting_amount, use_relative_balance, text_color)

        self.structured_data = BluffingAIData(data_path)

        self.opener_betting = OpenerBetting()
        self.dealer_betting = DealerBetting()

    def play_opener(self, opponent_choice=None):
        rand = random.random()
        if self.card.value == 1:
            return "b" if rand < self.opener_betting.bluff_on_1 else "c"
        elif self.card.value == 2:
            return "b" if rand < self.opener_betting.bluff_on_2 else "c"
        elif self.card.value == 3:
            return "c" if rand < self.opener_betting.bluff_on_3 else "b"

    def play_dealer(self, opponent_choice):
        rand = random.random()
        if self.card.value == 1:
            if opponent_choice == "c":
                return "b" if rand < self.dealer_betting.bluff_on_1 else "c"
            else:
                return "f"
        elif self.card.value == 2:
            if opponent_choice == "c":
                return "c"
            elif opponent_choice == "b":
                return "b" if rand < self.dealer_betting.bluff_on_2 else "f"
        elif self.card.value == 3:
            return "b"

    def play_opener_choice_on_dealer_bet(self, opponent_choice):
        return self.play_dealer(opponent_choice)
