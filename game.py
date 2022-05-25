from enum import Enum
from hand import Hand
import sys
import random
import traceback
#from game_state import GameState
from deck import Deck
from unoplayer import UnoPlayer
from empty_deck_exception import EmptyDeckException


class Game:
    INIT_HAND_SIZE = 7

    class Direction(Enum):
        FORWARDS = 0
        BACKWARDS = 1

    PRINT_VERBOSE = True

    def __init__(self, scoreboard, player_class_list):
        self.scoreboard = scoreboard
        self.deck = Deck()
        self.h = [None] * scoreboard.get_num_players()
        self.most_recent_color_called = [None] * scoreboard.get_num_players()
        try:
            # print(scoreboard.get_num_players())
            # print(self.h)
            # print(player_class_list)
            # print(scoreboard.get_player_list())
            for i in range(scoreboard.get_num_players()):
                if "dqn" in player_class_list[i]:
                    self.h[i] = Hand(player_class_list[i], scoreboard.get_player_list()[i], dqn=True)
                else:
                    self.h[i] = Hand(player_class_list[i], scoreboard.get_player_list()[i])
                for j in range(self.INIT_HAND_SIZE):
                    self.h[i].add_card(self.deck.draw())
            self.up_card = self.deck.draw()
            while self.up_card.followed_by_call():
                self.deck.discard(self.up_card)
                self.up_card = self.deck.draw()
        except:
            print("Can't deal initial hands!", player_class_list)
            sys.exit(1)
        self.direction = self.Direction.FORWARDS
        self.curr_player = random.randint(0, scoreboard.get_num_players()-1)
        self.called_color = UnoPlayer.Color.NONE
        self.round_points = 0

    def print_state(self):
        for i in range(self.scoreboard.get_num_players()):
            print("Hand #", i, ":", self.h[i])

    def get_next_player(self):
        if self.direction == self.Direction.FORWARDS:
            return (self.curr_player + 1) % self.scoreboard.get_num_players()
        else:
            if self.curr_player == 0:
                return self.scoreboard.get_num_players() - 1
            else:
                return self.curr_player - 1

    def advance_to_next_player(self):
        self.curr_player = self.get_next_player()

    def reverse_direction(self):
        if self.direction == self.Direction.FORWARDS:
            self.direction = self.Direction.BACKWARDS
        else:
            self.direction = self.Direction.FORWARDS

    def play(self):
        print("Initial upcard is ", self.up_card)
        try:
            while True:
                if self.make_move(output=True):
                    break
        except EmptyDeckException:
            print("Deck exhausted: this game is a draw.")
        except:
            traceback.print_exc()

    def make_move(self, action=None, output=False):
        if output:
            print(str(self.h[self.curr_player].get_player_name()) + " (" + str(self.h[self.curr_player]) + ")", end="")
        played_card = self.h[self.curr_player].play(self, action)
        if not played_card:
            try:
                drawn_card = self.deck.draw()
            except:
                if output:
                    print("...deck exhausted, remixing...")
                self.deck.remix()
                drawn_card = self.deck.draw()
            self.h[self.curr_player].add_card(drawn_card)
            if output:
                print(" has to draw (" + str(drawn_card) + ").", end="")
            played_card = self.h[self.curr_player].play(self, action)
        if played_card:
            if output:
                print(" plays " + str(played_card) + " on " + str(self.up_card) + ".", end="")
            self.deck.discard(self.up_card)
            self.up_card = played_card
            if self.up_card.followed_by_call():
                self.called_color = self.h[self.curr_player].call_color(self)
                self.most_recent_color_called[self.curr_player] = self.called_color
                if output:
                    print(" (and calls " + str(self.called_color) + ").", end="")
            else:
                self.called_color = UnoPlayer.Color.NONE
        if self.h[self.curr_player].is_empty():
            self.round_points = 0
            for j in range(self.scoreboard.get_num_players()):
                self.round_points += self.h[j].count_cards()
            if output:
                print("\n" + self.h[self.curr_player].get_player_name() + " wins! (and collects " + str(
                    self.round_points) + " points.)")
            self.scoreboard.add_to_score(self.curr_player, self.round_points)
            if output:
                print("---------------\n" + str(self.scoreboard))
            return True
        if self.h[self.curr_player].size() == 1:
            if output:
                print(" UNO!", end="")
        if output:
            print()
        if played_card:
            played_card.perform_card_effect(self, output)
        else:
            self.advance_to_next_player()
        return False

    def print(self, s):
        if self.PRINT_VERBOSE:
            print(s, end="")

    def println(self, s):
        if self.PRINT_VERBOSE:
            print(s)

    def get_game_state(self, dqn=False, dqn_index=0):
        return GameState(self, dqn, dqn_index)

    def get_up_card(self):
        return self.up_card


class GameState:
    def __init__(self):
        self.the_game = None
        self.num_cards_in_hands_of_upcoming_players = [0] * 4
        self.most_recent_color_called_by_upcoming_players = [None] * 4
        self.total_score_of_upcoming_players = [0] * 4

    def __init__(self, game, dqn=False, dqn_index = 0):
        players = game.scoreboard.get_num_players()
        self.num_cards_in_hands_of_upcoming_players = [0] * players
        self.most_recent_color_called_by_upcoming_players = [None] * players
        self.total_score_of_upcoming_players = [0] * players
        direction_multiplier = 1 if game.direction == Game.Direction.FORWARDS else -1
        for i in range(len(game.h)):
            if dqn:
                player_index = (dqn_index + players + (direction_multiplier * (i + 1))) % players
            else:
                player_index = (game.curr_player + players + (direction_multiplier * (i + 1))) % players
            self.num_cards_in_hands_of_upcoming_players[i] = game.h[player_index].size()
            self.total_score_of_upcoming_players[i] = game.scoreboard.get_score(player_index)
            self.most_recent_color_called_by_upcoming_players[i] = game.most_recent_color_called[player_index]
        self.the_game = game

    def get_num_cards_in_hands_of_upcoming_players(self):
        return self.num_cards_in_hands_of_upcoming_players

    def get_total_score_of_upcoming_players(self):
        return self.total_score_of_upcoming_players

    def get_most_recent_color_called_by_upcoming_players(self):
        for i in range(len(self.most_recent_color_called_by_upcoming_players)):
            if not self.most_recent_color_called_by_upcoming_players[i]:
                self.most_recent_color_called_by_upcoming_players[i] = UnoPlayer.Color.NONE
        return self.most_recent_color_called_by_upcoming_players

    def get_played_cards(self):
        if self.the_game:
            return self.the_game.deck.get_discarded_cards()
        else:
            return []