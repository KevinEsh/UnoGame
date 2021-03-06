from random import shuffle, choice
from src.models.card import *
from src.models.player import *

class Game:
    def __init__(self, names, init_cards=5, init_player=0, reverse=False):
        """Game settings"""
        self.names = names
        self.init_cards = init_cards
        self.turn = init_player
        self.reverse = reverse
        self.colors = ["Blue", "Green", "Yellow", "Red"]
        self.values = list(range(10)) + list(range(1,10)) + ["+2", "Revert", "Cancel"]*2  + ["WildCard", "+4"]

    def __str__(self):
        return f"Game(names=[{len(self.names)})], init_cards={self.init_cards}, revert={self.reverse})"

    def __repr__(self):
        return self.__str__(self)

    def __generateDeck(self):
        self.deck = []
        for value in self.values:
            for color in self.colors:
                if value == "WildCard":
                    self.deck.append(WildCard(value, None))
                elif value in ["+2", "+4"]:
                    self.deck.append(PlusCard(value, color))
                elif value == "Cancel":
                    self.deck.append(CancelCard(value, color))
                elif value == "Revert":
                    self.deck.append(RevertCard(value, color))
                else:
                    self.deck.append(Card(value, color))
        shuffle(self.deck)

    def __generateDumpDeck(self):
        card = self.deck.pop()
        if isinstance(card, WildCard):
            card.color = choice(self.colors)
        self.dump_deck = [card]

    def __generatePlayers(self):
        self.players = []
        for name in self.names:
            self.players.append(Player(name, self.deck[:self.init_cards]))
            self.deck = self.deck[self.init_cards:]

    def generate(self):
        self.__generateDeck()
        self.__generateDumpDeck()
        self.__generatePlayers()

    def uno(self, player):
        return len(player.cards) == 1

    def topCard(self):
        return self.dump_deck[-1]

    def nextTurn(self):
        if self.reverse:
            self.turn = self.turn - 1 if self.turn else len(self.players) - 1
        else:
            self.turn = (self.turn + 1) % len(self.players)
        return self.turn

    def validCard(self, card):
        if isinstance(card, WildCard):
            return True
        elif card.value == self.topCard().value or card.color == self.topCard().color:
            return True
        else:
            return False
