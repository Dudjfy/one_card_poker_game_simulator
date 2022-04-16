from card import Card
import matplotlib.pyplot as plt
import random
import time


class Game:
    def __init__(self, p1, p2, games=1, display_text=False):
        self.games = games
        self.score_p1 = 0
        self.score_p2 = 0
        self.cards = [Card(1), Card(2), Card(3)]
        self.p1 = p1
        self.p2 = p2
        self.players = [self.p1, self.p2]
        self.display_text = display_text

        self.pool = 0
        self.opener = None
        self.dealer = None
        self.player_folded = False
        # self.opener_choice = None
        # self.dealer_choice = None

    def check_balance(self):
        return all([p.check_balance() for p in self.players])

    def players_bets(self):
        for p in self.players:
            self.pool += p.bet()

        return self.pool

    def choose_opener_and_dealer(self, i):
        self.opener = self.p1 if i % 2 == 0 else self.p2
        self.dealer = self.p2 if i % 2 == 0 else self.p1

        if self.display_text:
            print(f"Opener: {self.opener.name}, Dealer: {self.dealer.name}")

    def print_info(self, info_name, info_data):
        print(f"{info_name}{info_data} - {self.p1.name}: {self.p1.get_balance()}, {self.p2.name}: {self.p2.get_balance()}")

    def choose_cards(self):
        self.p1.card, self.p2.card = random.sample(self.cards, k=2)

        if self.display_text:
            for p in self.players:
                print(f"\t{p.name} {p.card}", end="")
            print()

    def reset_values(self):
        self.pool = 0
        self.opener = None
        self.dealer = None
        self.player_folded = False
        # self.opener_choice = None
        # self.dealer_choice = None

    def initial_setup(self, game):
        self.reset_values()
        self.players_bets()

        if self.display_text:
            self.print_info("Pool: ", self.pool)

        self.choose_opener_and_dealer(game)
        self.choose_cards()

    def get_opposite_player(self, player):
        if player is self.opener:
            return self.dealer
        else:
            return self.opener

    def player_choice(self, player, play_method, opponent_choice=None):
        player_choice = play_method(opponent_choice)
        if player_choice == "b":
            self.pool += player.bet()
        if self.display_text:
            print(f"\t\t{player.name} - {player_choice}")
        if player_choice == "f":
            self.pay_winner(self.get_opposite_player(player),
                            message_beginning="won", message_end=f", {player.name} folded")
        return player_choice

    def player_choices(self):
        # self.opener_choice = self.opener.play_opener()
        # if self.opener_choice == "b":
        #     self.pool += self.opener.bet()
        # if self.display_text:
        #     print(f"\t\t{self.opener.name} - {self.opener_choice}")
        # if not self.check_folds():
        #     return

        # self.dealer_choice = self.dealer.play_dealer(self.opener_choice)
        # if self.dealer_choice == "b":
        #     self.pool += self.dealer.bet()
        # if self.display_text:
        #     print(f"\t\t{self.dealer.name} - {self.dealer_choice}")
        # if not self.check_folds():
        #     return

        opener_choice = self.player_choice(self.opener, self.opener.play_opener)
        dealer_choice = self.player_choice(self.dealer, self.dealer.play_dealer, opener_choice)
        if opener_choice == "c" and dealer_choice == "b":
            opener_choice = self.player_choice(self.opener, self.opener.play_opener_choice_on_dealer_bet, dealer_choice)

        if opener_choice == "f" or dealer_choice == "f":
            self.player_folded = True

    def pay_winner(self, winner, message_beginning="", message_end=""):
        winner.win(self.pool)

        self.record_balance_changes()

        if self.display_text:
            print(f"{winner.name} {message_beginning} {self.pool}{message_end}")

    def payout(self):
        if self.player_folded:
            return

        winner = self.dealer
        if self.opener.card.value > self.dealer.card.value:
            winner = self.opener

        self.pay_winner(winner, message_beginning="got the larger card, won")

    def print_final_outcome(self):
        self.print_info("Final", "")
        print()

    def play_game(self, game):
        self.initial_setup(game)

        self.player_choices()

        self.payout()

        if self.display_text:
            self.print_final_outcome()

    def play_games(self, print_elapsed_time=False, print_portions=1, print_progress=False):
        if print_elapsed_time:
            start = time.time()

        if print_progress:
            print_step = self.games // print_portions

        for game in range(self.games):
            if print_progress:
                if (game + 1) % print_step == 0:
                    print(f"{(100 // print_portions) * ((game // print_step) + 1)}%")

            if not self.check_balance():
                break
            self.play_game(game)

        if print_elapsed_time:
            end = time.time()
            print(f"{round(end - start, 2)}s")

    def print_results(self):
        for p in self.players:
            plt.plot(p.balance_history, label=p.name)
        plt.legend()
        plt.show()

    def record_balance_changes(self):
        for p in self.players:
            p.record_balance_change()
