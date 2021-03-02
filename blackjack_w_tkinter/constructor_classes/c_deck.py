# This class represents a single playing card deck. The deck contains 52 cards,
# 13 cards per suit. The deck knows all it cards, it can deal a random card and
# remove a certain card.

from .c_card import Card
import random as rd


class Deck:
    def __init__(self):
        """
        Constructor, Creates a single, 52 card deck.
        """
        # The cards of the deck
        self.__cards = []

        # Four possible suits diamonds, hearts, clubs and spades
        self.__suits = ["D", "H", "C", "S"]

        # Creates the deck
        for number in range(1, 14):

            for suit in self.__suits:
                self.__cards.append(Card(suit, number))

    def deal(self):
        """
        Deals and removes a random card from the deck.
        :return: Card, the dealt card.
        """
        card = rd.choice(self.__cards)
        self.remove_card(card)
        return card

    def remove_card(self, card):
        """
        Removes a certain card from the deck.
        :param card: Card, the card to be removed
        :return: None
        """
        self.__cards.remove(card)


print("c_deck.py imported")