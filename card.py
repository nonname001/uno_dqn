from unoplayer import UnoPlayer
from empty_deck_exception import EmptyDeckException


class Card:
    PRINT_IN_COLOR = False

    # def __init__(self, color, rank):
    #     self.color = color
    #     self.rank = rank
    #     self.number = -1

    # def __init__(self, color, number):
    #     self.color = color
    #     self.rank = UnoPlayer.Rank.NUMBER
    #     self.number = number

    def __init__(self, color, rank, number):
        self.color = color
        self.rank = rank
        self.number = number

    def __str__(self):
        ret_val = ""
        if self.color == UnoPlayer.Color.RED:
            ret_val += "R"
        elif self.color == UnoPlayer.Color.YELLOW:
            ret_val += "Y"
        elif self.color == UnoPlayer.Color.GREEN:
            ret_val += "G"
        elif self.color == UnoPlayer.Color.BLUE:
            ret_val += "B"
        elif self.color == UnoPlayer.Color.NONE:
            ret_val += ""
        if self.rank == UnoPlayer.Rank.NUMBER:
            ret_val += str(self.number)
        elif self.rank == UnoPlayer.Rank.SKIP:
            ret_val += "S"
        elif self.rank == UnoPlayer.Rank.REVERSE:
            ret_val += "R"
        elif self.rank == UnoPlayer.Rank.WILD:
            ret_val += "W"
        elif self.rank == UnoPlayer.Rank.DRAW_TWO:
            ret_val += "+2"
        elif self.rank == UnoPlayer.Rank.WILD_D4:
            ret_val += "W4"
        return ret_val

    def forfeit_cost(self):
        if self.rank == UnoPlayer.Rank.SKIP or self.rank == UnoPlayer.Rank.REVERSE or self.rank == UnoPlayer.Rank.DRAW_TWO:
            return 20
        elif self.rank == UnoPlayer.Rank.WILD or self.rank == UnoPlayer.Rank.WILD_D4:
            return 50
        elif self.rank == UnoPlayer.Rank.NUMBER:
            return self.number
        print("Illegal card!")
        return -10000

    def can_play_on(self, c, called_color):
        if self.rank == UnoPlayer.Rank.WILD or self.rank == UnoPlayer.Rank.WILD_D4 or self.color == c.color or self.color == called_color or (
                self.rank == c.rank and self.rank != UnoPlayer.Rank.NUMBER) or self.number == c.number and self.rank == UnoPlayer.Rank.NUMBER and c.rank == UnoPlayer.Rank.NUMBER:
            return True
        else:
            return False

    def followed_by_call(self):
        return self.rank == UnoPlayer.Rank.WILD or self.rank == UnoPlayer.Rank.WILD_D4

    def perform_card_effect(self, game, output):
        if self.rank == UnoPlayer.Rank.SKIP:
            game.advance_to_next_player()
            game.advance_to_next_player()
        elif self.rank == UnoPlayer.Rank.REVERSE:
            game.reverse_direction()
            game.advance_to_next_player()
        elif self.rank == UnoPlayer.Rank.DRAW_TWO:
            self.next_player_draw(game, output)
            self.next_player_draw(game, output)
            game.advance_to_next_player()
            game.advance_to_next_player()
        elif self.rank == UnoPlayer.Rank.WILD_D4:
            self.next_player_draw(game, output)
            self.next_player_draw(game, output)
            self.next_player_draw(game, output)
            self.next_player_draw(game, output)
            game.advance_to_next_player()
            game.advance_to_next_player()
        else:
            game.advance_to_next_player()

    def next_player_draw(self, game, output):
        next_player = game.get_next_player()
        try:
            drawn_card = game.deck.draw()
        except EmptyDeckException:
            game.print("...deck exhausted, remixing...")
            game.deck.remix()
            drawn_card = game.deck.draw()
        game.h[next_player].add_card(drawn_card)
        if output:
            game.println("  " + game.h[next_player].get_player_name() + " draws " + str(drawn_card) + ".")

    def get_color(self):
        return self.color

    def get_rank(self):
        return self.rank

    def get_number(self):
        return self.number

    def __eq__(self, other):
        return self.color == other.color and self.rank == other.rank and self.number == other.number
