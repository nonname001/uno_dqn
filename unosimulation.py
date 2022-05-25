import traceback
from game import Game
from scoreboard import Scoreboard

PRINT_VERBOSE = True
PLAYER_FILENAME = "players.txt"
player_names = []
player_classes = []
GAMES = 2


def load_player_data():
    r = open(PLAYER_FILENAME, 'r')
    line = r.readline().strip().split(',')
    while line[0]:
        player_names.append(line[0])
        player_classes.append(line[1] + "_unoplayer." + line[1] + "_UnoPlayer")
        line = r.readline().strip().split(',')


if __name__ == "__main__":
    num_games = GAMES
    try:
        load_player_data()
        s = Scoreboard(player_names.copy())
        for i in range(num_games):
            g = Game(s, player_classes)
            g.play()
        print(s)
    except:
        traceback.print_exc()

