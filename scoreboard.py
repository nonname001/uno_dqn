class Scoreboard:
    def __init__(self, player_list):
        self.scores = [0] * len(player_list)
        self.player_list = player_list

    def add_to_score(self, player, points):
        self.scores[player] += points

    def get_score(self, player):
        return self.scores[player]

    def __str__(self):
        ret_val = ""
        for i in range(len(self.scores)):
            ret_val += "Player #" + str(i) + ": " + str(self.scores[i]) + "\n"
        return ret_val

    def get_player_list(self):
        return self.player_list

    def get_num_players(self):
        return len(self.player_list)

    def get_winner(self):
        winner = 0
        top_score = self.scores[0]
        for i in range(1, len(self.scores)):
            if self.scores[i] > top_score:
                top_score = self.scores[i]
                winner = i
        return winner
