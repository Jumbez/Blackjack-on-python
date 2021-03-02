# This class represents a single blackjack hand. The hand can draw random cards
# from the specified deck, the hand knows its value and its cards. This class
# has mainly made for blackjack, and therefore the hand also knows if it is
# busted


class Hand:

    def __init__(self, deck):
        """
        Constructor, creates attributes to maintain hands value, cards and deck.
        :param deck: Deck, The deck that hand uses to draw cards.
        """
        # Hands value
        self.__value = 0

        # List of the cards of the hand. Items are Card-objects
        self.__cards = []

        # The deck of the hand, Deck-object
        self.__deck = deck

    def take_card(self):
        """
        Adds a random card to the hand from its deck and also removes the card
        from the deck.
        :return: Int, The value of the hand.
        """
        card = self.__deck.deal()
        self.__cards.append(card)
        self.calculate_hand_value()
        return self.__value

    def calculate_hand_value(self):
        """
        Calculates the value of the hand by blackjack rules.
        :return: None
        """
        self.__value = 0

        for card in sorted(self.__cards, reverse=True):
            if card.value() != 1:
                self.__value += card.value()
            else:
                if (self.__value + card.value() + 10) <= 21:
                    self.__value += 11
                else:
                    self.__value += 1

    def has_busted(self):
        """
        Checks if the hand has busted, e.g the value of the hand is over 21
        :return: Bool, True if the value is over 21, False otherwise
        """
        if self.__value > 21:
            return True
        else:
            return False

    def return_cards(self):
        """
        Returns the cards of the hand.
        :return: List
        """
        return self.__cards

    def return_value(self):
        """
        Returns the value of the hand by blackjack rules.
        :return: Int, the value of the hand.
        """
        self.calculate_hand_value()
        return self.__value


print("c_hand.py imported")
