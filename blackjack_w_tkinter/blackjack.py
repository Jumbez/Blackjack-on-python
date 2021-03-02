# Ari Hietanen          282456      ari.hietanen@tuni.fi
# Jukka-Pekka Keinänen  290650      jukka-pekka.keinanen@tuni.fi

# TIE-02101, Ohjelmointi 1
# Tehtävän graafinen käyttöliittymä ratkaisu:
# Ohjelmassa on toteuttu klassinen kasinoilla pelattava korttipeli blackjack.
# Pelin säännöt löytyvät tekstitiedostosta rules, ja ohjelman toteutuksessa
# käytetyt luokat kansiosta constructor_classes. Pelissä voi kerrallaan pelata
# yhden pakan kerrallaan, jonka jälkeen se on käynnistettävä uudelleen. Peli
# tähtäsi arvostelussa skaalautuvaksi projektiksi.

import tkinter as tk
from tkinter import messagebox
import time
from constructor_classes.c_deck import Deck
from constructor_classes.c_hand import Hand


CHIPS = [2, 5, 10, 50, 100]
STARTING_FUNDS = 500


class GUI:
    def __init__(self, deck):

        # After defining the root window it is split into two parts
        self.__root = tk.Tk()
        self.__root.title("Blackjack")
        self.__root.geometry("1500x1000")
        self.__root.resizable(True, True)

        # 1) Options frame at the bottom with all the buttons
        self.options_frame = tk.Frame(self.__root, bd=5,
                                      height=1024)
        self.options_frame.pack(side=tk.BOTTOM, fill="x", expand=False)

        # 2) Game canvas at the top where the actual game happens
        self.game_canvas = tk.Canvas(self.__root, bg="green")
        self.game_canvas.pack(side=tk.TOP, fill="both", expand=True)

        # Defining a couple of variables for the Bet functions
        self.funds = tk.DoubleVar()
        self.funds_text = tk.StringVar()

        self.bet = tk.DoubleVar()
        self.bet_text = tk.StringVar()

        self.bet_modifier = tk.IntVar()
        self.bet_modification = tk.IntVar()

        # Filling up the options-frame
        tk.Label(self.options_frame,
                 textvar=self.funds_text).grid(row=3, column=1, columnspan=2,
                                               sticky=tk.W)
        tk.Label(self.options_frame,
                 textvar=self.bet_text).grid(row=4, column=1, columnspan=2,
                                             sticky=tk.W)

        # Create radio buttons for choosing the desired chip
        for i in CHIPS:
            tk.Radiobutton(self.options_frame, text=f"Modify bet by  {i}€",
                           variable=self.bet_modifier, value=i)\
                .grid(row=CHIPS.index(i), column=0, sticky="W")

        # Radio buttons to choose whether you want to raise or lower the bet
        tk.Radiobutton(self.options_frame, text="Raise bet",
                       variable=self.bet_modification, value=1)\
            .grid(row=2, column=1)
        tk.Radiobutton(self.options_frame, text="Lower bet",
                       variable=self.bet_modification, value=0) \
            .grid(row=2, column=2)

        # The other Buttons of the code
        self.balance_bet_btn = tk.Button(self.options_frame,
                                         text="Balance bet to Zero",
                                         command=self.balance_bet)
        self.balance_bet_btn.grid(row=0, column=1, sticky="WE", columnspan=3)
        self.modify_bet_btn = tk.Button(self.options_frame, text="Modify Bet",
                                        command=self.define_bet)
        self.modify_bet_btn.grid(row=1, column=1, sticky="WE", columnspan=3)

        self._start_hit_btn = tk.Button(self.options_frame,
                                        text="Start the Turn / Deal Cards",
                                        command=self.deal_base_cards)
        self._start_hit_btn.grid(row=0, column=4, columnspan=3, rowspan=2,
                                 sticky="NEWS")
        self._stand_btn = tk.Button(
            self.options_frame, text="Stand",
            command=self.player_stand_dealer_draw, state=tk.DISABLED)

        self._stand_btn.grid(row=2, column=4, columnspan=3, rowspan=3,
                             sticky="NEWS")

        self.action_info = tk.Label(self.options_frame, text="")
        self.action_info.config(font=("Courier", 28))
        self.action_info.grid(row=1, column=20, rowspan=4, sticky="WE")

        # Setting the columnconfigure to ease locations of the widgets in
        # options_frame
        self.options_frame.grid_columnconfigure(20, weight=4)
        self.options_frame.grid_columnconfigure(4, weight=1)
        self.options_frame.grid_columnconfigure(5, weight=1)
        self.options_frame.grid_columnconfigure(6, weight=1)

        # Defining some instance variables that are used later in the program
        self.deck = deck  # The parameter of Class GUI
        self.player_pos_counter = 1
        self.dealer_pos_counter = 1
        self.player_hand = Hand(self.deck)
        self.dealer_hand = Hand(self.deck)
        self.cards_of_the_turn = []

        # The 1st row is for the player's info texts
        # The 2nd row is for the dealer's info texts
        self.canvas_texts = [[], []]

        self.initialize_game()
        self.__root.mainloop()

    def create_popup(self):
        """
        Creates a popup-window, which guides the player if he
         doesn't know the blackjack rules
        :return:
        """
        tk.messagebox.showinfo(title="rules",
                               message="The rules of the blackjack"
                               " can be found at rules.txt file")

    def initialize_game(self):
        """
        A function ran once at the beginning of the game/launch of the window
        """
        self.create_popup()
        self.funds.set(STARTING_FUNDS)  # Set default funds
        self.funds_text.set(f"Current funds: {self.funds.get()}€")
        self.bet.set(0)  # Set default bet at the beginning
        self.bet_text.set(f"Current bet: {self.bet.get()}€")
        self.bet_modifier.set(CHIPS[0])
        self.bet_modification.set(1)

        # The game is began at the same time a turn starts
        self.begin_turn()

    def define_bet(self):
        """
        Increases/decreases the bet.
        :return:
        """
        if self.bet_modification.get() == 1:
            if self.funds.get()-self.bet_modifier.get() >= 0:
                self.funds.set(self.funds.get()-self.bet_modifier.get())
                self.bet.set(self.bet.get() + self.bet_modifier.get())
                self.funds_text.set(f"Current funds: {self.funds.get()}€")
                self.bet_text.set(f"Current bet: {self.bet.get()}€")
            else:
                self.action_info.configure(
                    text="You don't have enough funds to increase the bet "
                         "for the selected amount!")
        else:
            if self.bet.get()-self.bet_modifier.get() >= 0:
                self.funds.set(self.funds.get()+self.bet_modifier.get())
                self.bet.set(self.bet.get() - self.bet_modifier.get())
                self.funds_text.set(f"Current funds: {self.funds.get()}€")
                self.bet_text.set(f"Current bet: {self.bet.get()}€")
            else:
                self.action_info.configure(
                    text="The bet can't be negative")

    def balance_bet(self):
        """
        Changes the bet 0 and returns the Funds to the state they were
        AT THE BEGINNING OF THE CURRENT TURN
        """
        self.funds.set(self.funds.get()+self.bet.get())
        self.bet.set(0)
        self.bet_text.set(f"Current bet: {self.bet.get()}€")
        self.funds_text.set(f"Current funds: {self.funds.get()}€")

    def begin_turn(self):
        """
        General method which is run at the beginning of each turn.
        """
        self.action_info.configure(text="")

        # Resets the locations where the cards will appear
        self.player_pos_counter = 1
        self.dealer_pos_counter = 1

        # Resets the instance variables used during previous turns
        self.game_canvas.delete("all")
        self.player_hand = Hand(self.deck)
        self.dealer_hand = Hand(self.deck)
        self.cards_of_the_turn = []

        # Resets the buttons
        self._stand_btn.configure(state=tk.DISABLED)
        self._start_hit_btn.configure(state=tk.NORMAL,
                                      text="Start the Turn / Deal Cards",
                                      command=self.deal_base_cards)
        self.balance_bet_btn.configure(state=tk.NORMAL)
        self.modify_bet_btn.configure(state=tk.NORMAL)

    def deal_base_cards(self):
        # Dealing order: player, dealer(hidden), player, dealer(visible)
        self.balance_bet_btn.configure(state=tk.DISABLED)
        self.modify_bet_btn.configure(state=tk.DISABLED)
        self._start_hit_btn.configure(state=tk.DISABLED)
        self.deal_a_card(False, False)
        self.deal_a_card(True, True)
        self.deal_a_card(False, False)
        self.deal_a_card(True, False)
        self._start_hit_btn.configure(text="Hit",
                                      command=self.player_draw_a_card,
                                      state=tk.NORMAL)
        self._stand_btn.configure(state=tk.NORMAL)

    def deal_a_card(self, dealer, hidden):
        """
        Deals one card from the deck created by the constructor classes.
        This method takes care of the "backend" side of the matters as well as
        calls place_a_card to draw the image on game_canvas. It is relatively
        modular and is called every time a card appears in the canvas.
        :param dealer: If it's the dealer, it will set a different placement
        location for the cards as well as set the correct owner for the dealt
        card.
        :type dealer: bool
        :param hidden: If dealer is True, for the 1st deal the card will be dealt
        backside up. This parameter will set the image of the card the red
        "backside" of the card when they're drawn to the canvas.
        :type hidden: bool
        :return: The value of the hand of the "owner of the dealt card" after
        the card was dealt.
        """

        try:
            if dealer:
                hand_val = self.dealer_hand.take_card()
                card = self.dealer_hand.return_cards()[-1]
                x = 500+self.dealer_pos_counter*150
                y = 100
                if hidden:
                    card_pic_name = f"back"
                else:
                    card_pic_name = f"{str(card)}"

                self.dealer_pos_counter += 1

            else:  # player
                hand_val = self.player_hand.take_card()
                card = self.player_hand.return_cards()[-1]
                card_pic_name = f"{str(card)}"
                x = 100+self.player_pos_counter*30
                y = 350+self.player_pos_counter*30
                self.player_pos_counter += 1  # Updates counter for the location

            # Places the card on the canvas
            self.place_a_card(x, y, card_pic_name)

            return hand_val

        # In case there are no more cards left in the deck:
        except IndexError:
            self.action_info.configure(
                text="There were no more cards left in the deck and thus none "
                     "could be dealt.")

    def place_a_card(self, x, y, card):
        """
        Adds a PhotoImage variable to self.cards_of_the_turn and  places a
        single card in the game_canvas.
        :param x: The x-location of the card in the canvast
        :type x: int
        :param y: The y-location of the card in the canvas
        :type y: int
        :param card: the name of the card in the format ValueSuit, e.g. "1S"
        :type card: str
        """
        img_path = f"pics/{card}.gif"
        card_img = tk.PhotoImage(file=img_path)
        self.cards_of_the_turn.append(card_img)

        self.game_canvas.create_image(x, y, image=card_img, anchor=tk.NW)
        self.game_canvas.update()

        time.sleep(1)

    def player_draw_a_card(self):
        """
        The phase followed by the initial dealing at the beginning of the turn
        Every this method draws a new card for the player
        """
        self._start_hit_btn.configure(text="Hit",
                                      command=self.player_draw_a_card,
                                      state=tk.DISABLED)
        self._stand_btn.configure(state=tk.DISABLED)

        self.deal_a_card(False, False)
        if self.player_hand.has_busted():

            self.compare_results()
            self.reveal_dealers_1st()
        else:
            self._start_hit_btn.configure(text="Hit",
                                          command=self.player_draw_a_card,
                                          state=tk.NORMAL)
            self._stand_btn.configure(state=tk.NORMAL)

    def reveal_dealers_1st(self):
        """
        Reveals the first card of the dealer.
        :return:
        """
        # Disables the stand and hit buttons
        self._stand_btn.configure(state=tk.DISABLED)
        self._start_hit_btn.configure(state=tk.DISABLED)

        card = self.dealer_hand.return_cards()[0]
        self.place_a_card(650, 100, f"{str(card)}")

    def player_stand_dealer_draw(self):
        """
        If the player stands or busts, the dealer draws cards until he busts or
        gets value of 17 or higher.
        """
        # Flips the hidden card making it visible
        self.reveal_dealers_1st()

        if self.dealer_hand.return_value() >= 17:
            self.compare_results()
        else:
            self.deal_a_card(True, False)
            self.player_stand_dealer_draw()

    def compare_results(self):
        """
        Compares the results and updates players cash balance.
        """
        # Hand values
        plr_hd_val = self.player_hand.return_value()
        dlr_hd_val = self.dealer_hand.return_value()

        # Checks if players has busted
        if self.player_hand.has_busted():
            self.funds.set(self.funds.get())
            self.action_info.configure(text="Player busts, "
                                            "dealer wins the hand!")

        # Checks if both dealer and the player have a blackjack
        elif ((plr_hd_val == 21 and len(self.player_hand.return_cards()) == 2)
              and (dlr_hd_val == 21 and len(
                    self.dealer_hand.return_cards()) == 2)):
            gain = self.bet.get()
            self.funds.set(self.funds.get() + gain)
            self.action_info.configure(
                text="Both, player and dealer gets a blackjack! It's a draw.")

        # Checks if player has the blackjack.
        elif plr_hd_val == 21 and len(self.player_hand.return_cards()) == 2:
            gain = 2.5 * self.bet.get()
            self.funds.set(self.funds.get() + gain)
            self.action_info.configure(text="It's a blackjack! Player wins the "
                                            "hand and {:.1f} €.".format(gain))
        # Checks if the players wins
        elif plr_hd_val > dlr_hd_val and (not self.dealer_hand.has_busted()):
            self.action_info.configure(text="Player wins the hand and"
                                            " {:.1f} €!"
                                            .format(2 * self.bet.get()))
            gain = 2 * self.bet.get()
            self.funds.set(self.funds.get() + gain)

        # Checks if the dealer has busted
        elif self.dealer_hand.has_busted():
            gain = 2 * self.bet.get()
            self.funds.set(self.funds.get() + gain)
            self.action_info.configure(text="Dealer busts, "
                                        "Player wins the hand and {:.1f} € !"
                                       .format(gain))

        # Checks if the dealer has a blackjack
        elif dlr_hd_val == 21 and len(self.dealer_hand.return_cards()) == 2:
            self.funds.set(self.funds.get())
            self.action_info.configure(text="Dealer gets a blackjack!"
                                            " Dealer wins the hand.")

        # Checks if the dealer has won
        elif dlr_hd_val > plr_hd_val:
            self.funds.set(self.funds.get())
            self.action_info.configure(text="Dealer wins the hand!")

        # Otherwise it's a draw
        else:
            gain = self.bet.get()
            self.funds.set(self.funds.get() + gain)
            self.action_info.configure(text="It's a draw!")

        self.bet.set(0)
        self.funds_text.set(f"Current funds: {self.funds.get()}€")
        self.bet_text.set(f"Current bet: {self.bet.get()}€")
        self.__root.after(10000, lambda: [self.begin_turn()])


def main():

    deck = Deck()
    GUI(deck)


main()
