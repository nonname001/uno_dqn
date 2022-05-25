import random
import traceback
from card import Card
from unoplayer import UnoPlayer
from empty_deck_exception import EmptyDeckException


class Deck:
    NUMBER_OF_DUP_REGULAR_CARDS = 2
    NUMBER_OF_DUP_ZERO_CARDS = 1
    NUMBER_OF_DUP_SPECIAL_CARDS = 2
    NUMBER_OF_WILD_CARDS = 4
    NUMBER_OF_WILD_D4_CARDS = 4
    SHUFFLE_FACTOR = 1

    cards = []

    def __init__(self):
        self.fill_deck()
        self.shuffle()
        self.discarded_cards = []

    def fill_deck(self):
        for i in range(1, 10):
            for j in range(self.NUMBER_OF_DUP_REGULAR_CARDS):
                self.cards.append(Card(color=UnoPlayer.Color.RED, number=i, rank=UnoPlayer.Rank.NUMBER))
                self.cards.append(Card(color=UnoPlayer.Color.YELLOW, number=i, rank=UnoPlayer.Rank.NUMBER))
                self.cards.append(Card(color=UnoPlayer.Color.BLUE, number=i, rank=UnoPlayer.Rank.NUMBER))
                self.cards.append(Card(color=UnoPlayer.Color.GREEN, number=i, rank=UnoPlayer.Rank.NUMBER))

        for j in range(self.NUMBER_OF_DUP_ZERO_CARDS):
            self.cards.append(Card(color=UnoPlayer.Color.RED, number=0, rank=UnoPlayer.Rank.NUMBER))
            self.cards.append(Card(color=UnoPlayer.Color.YELLOW, number=0, rank=UnoPlayer.Rank.NUMBER))
            self.cards.append(Card(color=UnoPlayer.Color.BLUE, number=0, rank=UnoPlayer.Rank.NUMBER))
            self.cards.append(Card(color=UnoPlayer.Color.GREEN, number=0, rank=UnoPlayer.Rank.NUMBER))

        for j in range(self.NUMBER_OF_DUP_SPECIAL_CARDS):
            self.cards.append(Card(color=UnoPlayer.Color.RED, rank=UnoPlayer.Rank.SKIP, number=-1))
            self.cards.append(Card(color=UnoPlayer.Color.YELLOW, rank=UnoPlayer.Rank.SKIP, number=-1))
            self.cards.append(Card(color=UnoPlayer.Color.BLUE, rank=UnoPlayer.Rank.SKIP, number=-1))
            self.cards.append(Card(color=UnoPlayer.Color.GREEN, rank=UnoPlayer.Rank.SKIP, number=-1))
            self.cards.append(Card(color=UnoPlayer.Color.RED, rank=UnoPlayer.Rank.REVERSE, number=-1))
            self.cards.append(Card(color=UnoPlayer.Color.YELLOW, rank=UnoPlayer.Rank.REVERSE, number=-1))
            self.cards.append(Card(color=UnoPlayer.Color.BLUE, rank=UnoPlayer.Rank.REVERSE, number=-1))
            self.cards.append(Card(color=UnoPlayer.Color.GREEN, rank=UnoPlayer.Rank.REVERSE, number=-1))
            self.cards.append(Card(color=UnoPlayer.Color.RED, rank=UnoPlayer.Rank.DRAW_TWO, number=-1))
            self.cards.append(Card(color=UnoPlayer.Color.YELLOW, rank=UnoPlayer.Rank.DRAW_TWO, number=-1))
            self.cards.append(Card(color=UnoPlayer.Color.BLUE, rank=UnoPlayer.Rank.DRAW_TWO, number=-1))
            self.cards.append(Card(color=UnoPlayer.Color.GREEN, rank=UnoPlayer.Rank.DRAW_TWO, number=-1))

        for i in range(self.NUMBER_OF_WILD_CARDS):
            self.cards.append(Card(color=UnoPlayer.Color.NONE, rank=UnoPlayer.Rank.WILD, number=-1))

        for i in range(self.NUMBER_OF_WILD_D4_CARDS):
            self.cards.append(Card(color=UnoPlayer.Color.NONE, rank=UnoPlayer.Rank.WILD_D4, number=-1))

    def shuffle(self):
        for i in range(self.SHUFFLE_FACTOR * len(self.cards)):
            x = random.randint(0, len(self.cards)-1)
            y = random.randint(0, len(self.cards) - 1)
            temp = self.cards[x]
            self.cards[x] = self.cards[y]
            self.cards[y] = temp

    def is_empty(self):
        return len(self.cards) == 0

    def draw(self):
        if len(self.cards) == 0:
            raise EmptyDeckException
        temp = self.cards[0]
        del self.cards[0]
        return temp

    def discard(self, c):
        self.discarded_cards.append(c)

    def remix(self):
        self.cards += self.discarded_cards
        self.discarded_cards = []
        self.shuffle()

    def get_discarded_cards(self):
        return self.discarded_cards


if __name__ == "__main__":
    print("test Deck.")
    d = Deck()
    while not d.is_empty():
        try:
            print(d.draw())
        except:
            traceback.print_exc()
