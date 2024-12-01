import random

suits = ("Hearts", "Diamonds", "Spades", "Clubs")
ranks = (
    "Two",
    "Three",
    "Four",
    "Five",
    "Six",
    "Seven",
    "Eight",
    "Nine",
    "Ten",
    "Jack",
    "Queen",
    "King",
    "Ace",
)
values = {
    "Two": 2,
    "Three": 3,
    "Four": 4,
    "Five": 5,
    "Six": 6,
    "Seven": 7,
    "Eight": 8,
    "Nine": 9,
    "Ten": 10,
    "Jack": 10,
    "Queen": 10,
    "King": 10,
    "Ace": 11,
}


# At the top of the file, replace the global playing variables with a GameState
class GameState:
    def __init__(self):
        self.playing = True
        self.dealer_playing = True


# Create a global instance
GAME_STATE = GameState()


class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.value = values[rank]

    def __str__(self):
        return self.rank + " of " + self.suit


class Deck:
    def __init__(self):
        self.deck = []
        # Creats all cards and stores them in a list as elements of the Card Class.
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit, rank))

    def shuffle(self):
        random.shuffle(self.deck)

    def deal(self):
        return self.deck.pop()


class Hand:
    def __init__(self):
        self.cards = []
        # self.aces = 0

    def add_card(self, card):
        # Recieves and stores card(s) in hand
        if type(card) is type([]):
            self.cards.extend(card)
        else:
            self.cards.append(card)

    def calc_value(self):
        # Loop to calculate value of hands.
        # Should loop through the card elements and obtain their value and sum up the hand value.
        # Here we need to check for aces and adjust according to the Special rule: Ace can be 11 or 1, whichever is preferable to the player.
        # Basically, if ace is causing player to bust - then the value will be reduced to 1.
        self.value = 0
        for card in self.cards:
            self.value += values[card.rank]

            if self.value > 21 and self.check_for_aces() != 0:
                self.value -= self.adjust_for_ace()

        return self.value

    def check_for_aces(self):
        self.aces = 0
        for card in self.cards:
            if card.rank == "Ace":
                self.aces += 1

        return self.aces

    def adjust_for_ace(self):
        return 10 * self.aces


class Chip:
    """

    Class to track player bets and saldos. Upon initiation, requires player input on how much they put into the game initially.

    """

    def __init__(self, name, total=0):
        self.total = total
        self.name = name
        self.bet = 0

    def __str__(self):
        return f"{self.name} has {self.total} chips"

    def win_bet(self, bet):
        self.total += bet

    def loses_bet(self, bet):
        self.total -= bet


def take_bet():
    """
    When function is called, then player will get a chance to wager a bet of his choice. Check that bet is correctly input as an integer.
    """
    player_bet = 0
    while True:
        try:
            player_bet += int(input("Please place your bet: "))
            break
        except:
            print("Please place your bet. Bet must be a number:")
            continue
        finally:
            print(f"Bet of {player_bet} chips has been placed.")
    return player_bet


def hit(deck, hand):
    """
    During game, player will get a choice whether to hit or stand. When they hit, then the deck will deal a card to the player. Function takes takes a deck and hand instance as input.
    """
    hand.add_card(deck.deal())


def hit_or_stand(deck, hand):
    """
    function to promt player or dealer whether they want to hit or stay. Dealer will hit if their hand value is lower than 17.
    """
    while True:
        try:
            ask = int(input("Hit 1 to hit or 2 to stay"))
            break
        except:
            print("Press 1 to Hit or 2 to stay: ")
            continue

    if ask == 1:
        print("Player chose to hit.")
        hit(deck, hand)
    else:
        print("Player chose to stay.")
        GAME_STATE.playing = False


def dealer_hit(deck, hand):
    if hand.calc_value() < 17:
        hit(deck, hand)
        print("Dealer Hits.")
    else:
        print("Dealer Stays.")
        GAME_STATE.dealer_playing = False


def show_some(dealer, player):
    """
    Takes in hand instances as input.
    Function displays all player cards and only 1 of the dealer card. Function also shows each parties hand value.
    """
    print(f"Dealer Card 1: {dealer.cards[0]} : {dealer.cards[0].value}")
    print(f"\n{name}'s Cards:")
    for card in player.cards:
        print(f"{card} : {card.value}")
    print(f"Total Value: {player.calc_value()}")


def show_all(dealer, player):
    """
    Takes in hand instances as input.
    Function displays all player and dealer cards. Function also shows each parties hand value.
    """
    print("Dealers Cards: ")
    for card in dealer.cards:
        print(f"{card} : {card.value}")
    print(f"Total Value: {dealer.calc_value()}")

    print(f"\n{name}'s Cards:")
    for card in player.cards:
        print(f"{card} : {card.value}")
    print(f"Total Value: {player.calc_value()}")


class Scenarios:
    """
    Class to check who won and to move chips around as needed.
    Upon creation, it takes the dealer and players hand along with the stake.
    If anything else than a push happens, play stops.
    """

    def __init__(self, dealer, player, bet):
        self.dealer = dealer
        self.player = player
        self.dealer_value = self.dealer.calc_value()
        self.player_value = self.player.calc_value()
        self.bet = bet
        self.check()

    def check(self):
        if self.dealer_value > 21:
            self.dealer_busts()
        elif self.player_value > 21:
            self.player_busts()
        elif self.dealer_value > self.player_value:
            self.dealer_wins()
        elif self.player_value > self.dealer_value:
            self.player_wins()
        else:
            self.push()

    def player_busts(self):
        player_bank.loses_bet(self.bet)
        print(f"{name} bust. {name} has {player_bank.total} chips left")
        GAME_STATE.playing = False

    def player_wins(self):
        player_bank.win_bet(self.bet)
        print(f"{name} wins this round! {name} has {player_bank.total} chips left")
        GAME_STATE.playing = False

    def dealer_busts(self):
        player_bank.win_bet(self.bet)
        print(f"{name} wins this round! {name} has {player_bank.total} chips left")
        GAME_STATE.playing = False

    def dealer_wins(self):
        player_bank.loses_bet(self.bet)
        print(f"{name} loses this round. {name} has {player_bank.total} chips left")
        GAME_STATE.playing = False

    def push(self):
        print("Its a Push!")
        GAME_STATE.playing = True


name = input("Player name:")

while True:
    try:
        saldo = int(input("Starting Saldo: "))
        break
    except:
        print("Please supply a number for the starting saldo: ")
        continue

player_bank = Chip(name, saldo)

print(f"Player has been added.\n{player_bank}")

while True:
    GAME_STATE.playing = True
    GAME_STATE.dealer_playing = True

    # Print an opening statement
    print("This is Blackjack.")

    # Setup player and their starting chips

    # Create & shuffle the deck, deal two cards to each player
    gamedeck = Deck()
    gamedeck.shuffle()
    card1 = gamedeck.deal()
    card2 = gamedeck.deal()
    card3 = gamedeck.deal()
    card4 = gamedeck.deal()

    dealercards = [card1, card3]
    playercards = [card2, card4]

    # Create hands
    dealerhand = Hand()
    dealerhand.add_card(dealercards)
    playerhand = Hand()
    playerhand.add_card(playercards)

    # Prompt the Player for their bet
    bet = take_bet()
    player = Chip(name, player_bank)

    # Show cards (but keep one dealer card hidden)
    show_some(dealerhand, playerhand)

    while GAME_STATE.playing:
        # recall this variable from our hit_or_stand function, player playing
        # Prompt for Player to Hit or Stand
        hit_or_stand(gamedeck, playerhand)

        # Show cards (but keep one dealer card hidden)
        show_some(dealerhand, playerhand)

        # If player's hand exceeds 21, run player_busts() and break out of loop
        if playerhand.calc_value() > 21:
            GAME_STATE.playing = False
            break

    # See if dealer wants to hit or not
    while GAME_STATE.dealer_playing and playerhand.calc_value() <= 21:
        dealer_hit(gamedeck, dealerhand)

    check = Scenarios(dealerhand, playerhand, bet)
    show_all(dealerhand, playerhand)

    # Inform Player of their chips total

    # Ask to play again
    play_again = input(
        "Press Y if you want to play again, press N if you want to stop: "
    )
    if play_again == "Y":
        playing = True
        continue
    else:
        break
