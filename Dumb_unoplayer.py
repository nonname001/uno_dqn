from unoplayer import UnoPlayer


class Dumb_UnoPlayer(UnoPlayer):
    def play(self, hand, up_card, called_color, state):
        for i in range(len(hand)):
            if self.can_play_on(hand[i], up_card, called_color):
                return i
        return -1

    def call_color(self, hand):
        return self.Color.RED

    def can_play_on(self, card, up_card, called_color):
        result = card.get_rank() == self.Rank.WILD
        result = result or card.get_rank() == self.Rank.WILD_D4
        result = result or card.get_color() == up_card.get_color()
        result = result or card.get_color() == called_color
        result = result or ((card.get_rank() == up_card.get_rank()) and (card.get_rank() != self.Rank.NUMBER))
        result = result or (card.get_number() == up_card.get_number() and card.get_rank() == self.Rank.NUMBER and up_card.get_rank() == self.Rank.NUMBER)
        return result
