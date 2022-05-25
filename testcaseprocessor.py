import traceback
import sys
from unoplayer import UnoPlayer
from card import Card
from game import GameState

player = "SmithJ"
classname = player + "_unoplayer"
filename = "testCases.txt"


def get_class( kls ): # credits to hasen from stackoverflow
    parts = kls.split('.')
    module = ".".join(parts[:-1])
    m = __import__( module )
    for comp in parts[1:]:
        m = getattr(m, comp)
    return m


class TestCaseProcessor:

    def __init__(self, classname):
        self.classname = classname
        self.thePlayer = get_class(classname + "_unoplayer")
        self.thePlayer = self.thePlayer()

    def do_it(self):
        num_hands_tested = 0
        r = open(filename,'r')
        line = r.readline()
        while line:
            hand = []
            cards = line.split(',')
            for i in cards:
                card = Card(UnoPlayer.Color.value_of(i.split()[0]), UnoPlayer.Rank.value_of(i.split()[1]), i.split()[2])
                hand.append(card)
            up_card_line = r.readline()
            up_card = Card(UnoPlayer.Color.value_of(up_card_line.split()[0]), UnoPlayer.Rank.value_of(up_card_line.split()[1]), up_card_line.split()[2])

            called_color_line = r.readline()
            called_color = UnoPlayer.Color.value_of(called_color_line)

            valid_plays = []
            valid_plays_line = r.readline()
            valid_play = valid_plays_line.split(',')

            for i in valid_play:
                valid_plays.append(int(i))

            self.test_hand(hand, up_card, called_color, valid_plays)
            num_hands_tested += 1

            if num_hands_tested < 100 or num_hands_tested % 100 == 0:
                print(num_hands_tested, "test hands passed!")

            r.readline()
            line = r.readline()

    def test_hand(self, hand, up_card, called_color, valid_plays):
        card_played = self.thePlayer.play(hand, up_card, called_color, GameState())
        if card_played not in valid_plays:
            print("Whoops -- your play() method has an error!")
            print("You were given this hand: ")
            for i in range(len(hand)):
                print(i, hand[i])
            print("and the up card was:", up_card)
            if up_card.get_rank() == UnoPlayer.Rank.WILD or up_card.get_rank() == UnoPlayer.Rank.WILD_D4:
                print("and the called color was:", called_color)
            print("and you (wrongly) returned", card_played)
            print("Valid plays would have included:")
            print(",".join(valid_plays))
            sys.exit(3)

        color = self.thePlayer.call_color(hand)

        if color != UnoPlayer.Color.RED and color != UnoPlayer.Color.BLUE and color != UnoPlayer.Color.GREEN and color != UnoPlayer.Color.YELLOW:
            print("Whoops -- your callColor() method has an error!")
            print("You were given this hand: ")
            for i in range(len(hand)):
                print(i, hand[i])
            print("and the up card was:", up_card)
            if up_card.get_rank() == UnoPlayer.Rank.WILD or up_card.get_rank() == UnoPlayer.Rank.WILD_D4:
                print("and the called color was:", called_color)
            print("and you (wrongly) returned", card_played)
            print("Valid plays would have included:")
            print(",".join(valid_plays))
            sys.exit(4)


if __name__ == "__main__":
    try:
        TestCaseProcessor(player).do_it()
    except:
        traceback.print_exc()
