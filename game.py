import uuid
import random


ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
colors = ['clubs', 'diamonds', 'hearts', 'spades']
options = ['raise', 'call', 'fold']

class Agent():
    def __init__(self):
        self.hand = []
        self.id = str(uuid.uuid4())
        self.ranks_in_hand = dict()
        self.colors_in_hand = dict()
        self.hand_representation = list()


    def play_turn(self, turn, representations, player_amounts, pot, current_price):

        self.update_representation()


    def update_representation(self):
        self.ranks_in_hand = dict()
        self.colors_in_hand = dict()

        for i in self.hand:
            self.ranks_in_hand.setdefault(i['rank'], 0)
            self.ranks_in_hand[i['rank']] += 1

            self.colors_in_hand.setdefault(i['color'], 0)
            self.colors_in_hand[i['color']] += 1

        self.max_rank_index = max([ranks.index(j['rank']) for j in self.hand])
        self.min_rank_index = max([ranks.index(j['rank']) for j in self.hand])

        self.full_hand_representation = list()
        for i in self.hand:
            color_rep = [1 if j == i['color'] else 0 for j in colors]
            rank_rep = [1 if j == i['color'] else 0 for j in ranks]
            self.full_hand_representation.extend(color_rep)
            self.full_hand_representation.extend(rank_rep)

        while len(self.full_hand_representation) < 5*(len(ranks) + len(colors)):
            self.full_hand_representation.append(0)

        self.partial_representation = list()
        for i in ranks:
            self.partial_representation.append(self.ranks_in_hand.get(i, 0 ))
        for i in colors:
            self.partial_representation.append(self.colors_in_hand.get(i, 0 ))

    def get_representation(self):
        return self.full_hand_representation


    def get_id(self):
        return self.id


class Game():
    def __init__(self):
        self.players = [Agent() for _ in range(5)]
        self.generate_cards()
        self.stake = 0


    def play_game(self, starting_amount = 5):
        player_amounts = {i.get_id():starting_amount for i in self.players}
        pot = 0
        current_price = 1
        self.generate_cards()

        random.shuffle(self.deck)
        for i in self.players:
            i.hand.append(self.deck.pop())
        for i in self.players:
            i.hand.append(self.deck.pop())
        for i in self.players:
            i.update_representation()
        representations = [i.get_representation() for i in self.players]
        for c, i in enumerate(self.players):
            i.play_turn([1 if j == c else 0 for j in range(5)], representations, player_amounts, pot, current_price)







    def generate_cards(self):
        self.deck = []
        for i in ranks:
            for j in colors:
                self.deck.append({'rank':i, 'color':j})


    def get_winner(self):
        self.winners = []

        # Royal flush
        for i in self.players:
            if [j for j in i.hand if j['rank'] in ['A', '10', 'J', 'Q', 'K']] and \
                    len(list(set([j['color'] for j in i.hand]))) == 1:
                self.winners.append(i.get_id())

        # Straight flush
        if not self.winners:
            highest_flush_val = dict()

            for i in self.players:

                if i.max_rank_index - i.min_rank_index == 5 and len(list(set([j['color'] for j in i.hand]))) == 1:
                    highest_flush_val.setdefault(i.max_rank_index, [])
                    highest_flush_val[i.max_rank_index].append(i.get_id())
            if highest_flush_val:
                max_res = max(highest_flush_val.keys())
                self.winners = highest_flush_val[max_res]

        #4 of a kind
        if not self.winners:
            highest_val = dict()
            for i in self.players:
                if max(i.ranks_in_hand.values()) == 4:
                    reverse_dict = {j:i for i, j in i.ranks_in_hand.items()}
                    highest_val[i.get_id()] = ranks.index(reverse_dict[4])
            if highest_val:
                self.winners = [ i for i, j in highest_val.items() if j == max(highest_val.values())]


        #full house
        if not self.winners:
            highest_val = dict()
            for i in self.players:
                if 3 in i.ranks_in_hand.values() and 2 in i.ranks_in_hand.values():
                    reverse_dict = {j:i for i, j in i.ranks_in_hand.items()}
                    highest_val[i.get_id()] = (ranks.index(reverse_dict[3]), ranks.index(reverse_dict[2]))
            if highest_val:
                self.winners = [ i for i, j in highest_val.items() if j == max(highest_val.values())]

        #flush
        if not self.winners:
            highest_val = dict()
            for i in self.players:
                if 5 in i.colors_in_hand.values():
                    reverse_dict = {j:i for i, j in i.colors_in_hand.items()}
                    highest_val[i.get_id()] = (colors.index(reverse_dict[3]), colors.index(reverse_dict[2]))
            if highest_val:
                self.winners = [ i for i, j in highest_val.items() if j == max(highest_val.values())]

        #straight
        if not self.winners:
            highest_val = dict()
            for i in self.players:
                if i.max_rank_index - i.min_rank_index == 5 and len(i.ranks_in_hand.keys()) == 5:
                    highest_val[i.get_id()] = i.max_rank_index
            if highest_val:
                self.winners = [ i for i, j in highest_val.items() if j == max(highest_val.values())]

        #3 of a kind
        if not self.winners:
            highest_val = dict()
            for i in self.players:
                if max(i.ranks_in_hand.values()) == 3:
                    reverse_dict = {j:i for i, j in i.ranks_in_hand.items()}
                    highest_val[i.get_id()] = ranks.index(reverse_dict[3])
            if highest_val:
                self.winners = [ i for i, j in highest_val.items() if j == max(highest_val.values())]

        #two pair

        # if not self.winners:
        #     highest_val = dict()
        #     for i in self.players:
        #
        #         pair_counter =
        #
        #         if 2 in i.ranks_in_hand.values():
        #             reverse_dict = {j:i for i, j in i.ranks_in_hand.items()}
        #             highest_val[i.get_id()] = ranks.index(reverse_dict[3])
        #     if highest_val:
        #         self.winners = [ i for i, j in highest_val.items() if j == max(highest_val.values())]



        #one pair
        # if not self.winners:
        #     highest_val = dict()
        #     for i in self.players:
        #
        #         pair_counter =
        #
        #         if 2 in i.ranks_in_hand.values():
        #             reverse_dict = {j:i for i, j in i.ranks_in_hand.items()}
        #             highest_val[i.get_id()] = ranks.index(reverse_dict[3])
        #     if highest_val:
        #         self.winners = [ i for i, j in highest_val.items() if j == max(highest_val.values())]

        #high card
        if not self.winners:
            highest_val = dict()
            for i in self.players:
                highest_val[i.get_id()] = i.max_rank_index
            self.winners = [ i for i, j in highest_val.items() if j == max(highest_val.values())]
