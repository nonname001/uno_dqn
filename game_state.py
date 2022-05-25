from game import Game
from unoplayer import UnoPlayer


class GameState:
    def __init__(self):
        self.the_game = None
        self.num_cards_in_hands_of_upcoming_players = [0] * 4
        self.most_recent_color_called_by_upcoming_players = [None] * 4
        self.total_score_of_upcoming_players = [0] * 4

    def __init__(self, game):
        players = game.scoreboard.get_num_players()
        self.num_cards_in_hands_of_upcoming_players = [0] * players
        self.most_recent_color_called_by_upcoming_players = [None] * players
        self.total_score_of_upcoming_players = [0] * players
        direction_multiplier = 1 if game.direction == Game.Direction.FORWARDS else -1
        for i in range(len(game.h)):
            player_index = (game.curr_player + players + (direction_multiplier * (i + 1))) % players
            self.num_cards_in_hands_of_upcoming_players[i] = len(game.h[player_index])
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
