# This class represents a single playing card. The card has a certain suit, name
# and value. This class is mainly made for blackjack, and therefore the value
# of the card is also calculated by blackjack rules.

class Card:
    def __init__(self, suit, name):
        """
        Constructer, creates a single playing card
        :param suit: str, One of the four playing card suit.
        :param name: int, The cards facevalue, e.g Queen is 12 etc.
        """
        self.__name = name
        self.__suit = suit

    def __gt__(self, other_card):
        """
        Defines comparing method "greater than". The card which has greater value
        is bigger
        :param other_card: Card, other playing card.
        :return: Bool, True if self.__card is bigger, otherwise false.
        """
        if self.value() > other_card.value():
            return True
        else:
            return False

    def __str__(self):
        """
        The string representation of the card, for example hearts of Queen as
        string is expressed as "12H"

        :return: str, the string representation of the card.
        """
        return f"{self.__name}{self.__suit}"

    def value(self):
        """
        Returns the value of the card by blackjack rules.
        :return: int, the value of the card.
        """
        if self.__name < 10:
            return self.__name

        else:
            return 10

    def suit(self):
        """
        Returns the suit of the card.
        :return: str
        """
        return self.__suit


print("c_card.py imported")