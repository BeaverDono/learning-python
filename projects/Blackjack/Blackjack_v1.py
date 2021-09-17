'''
Author:     Christoffer Gray
Date:       9/14/2021
Milestone Project 2.5 "Blackjack"

Notes
-----------------------
CARDS
  - Suit, Rank, Value (Tuple)

DECK
  - New deck with all 52 cards
  - Card class object instance
  - Shuffle deck

PLAYER
  - Decides to place bet before hand starts
  - Player is dealt two cards by game logic
  - Player has to decide to hit, pass or split
  - CPU goes off of dealer rules

CHIPS CLASS
  - Handles adding and subtracting chip total

Game Logic Notes
  - Check total of cards if it goes beyond 21, BUST
    - Check to see if any of the cards is an Ace -> 1 or 11
        - Prevent BUST event from happening, -10 from total if Ace detected when value is over 21
    - Was going to do a soft 17 rule on dealer but went with it hitting to get above the player
'''
#Import Libraries
import random

#Global Variables
#Deck Variables
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 'Nine':9, 'Ten':10, 'Jack':10, 'Queen':10, 'King':10, 'Ace':11}
suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
playing = True

class Card():

    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.value = values[rank] # Keymaster
    
    def __str__(self):
        return self.rank + " of " + self.suit


class Deck():
    
    #Create the Deck at start
    def __init__(self):
        self.all_cards = []
        for suit in suits:
            for rank in ranks:
                created_card = Card(suit, rank)
                self.all_cards.append(created_card)
    
    # Shuffle method
    def shuffle(self):
        random.shuffle(self.all_cards)

    # Deal card
    # If I need to deal multiple cards, I'll use a for loop
    def deal(self):
        return self.all_cards.pop()


class Player():
    def __init__(self):
        self.hand = []
        self.value = 0
        self.aces = 0

    def add_card(self, new_card):
        # Pending the card to our hand
        self.hand.append(new_card)
        # Add the value of the card to your total
        self.value += values[new_card.rank]
        #Track Aces
        if new_card.rank == 'Ace':
            self.aces += 1

    def adjust_for_ace(self):
        # Check current value and see if we have an Ace
        while self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1

class Chips():
    def __init__(self, total=100):
        self.total = total
        self.bet = 0

    def add_chips(self):
        self.total += self.bet

    def remove_chips(self):
        self.total -= self.bet

# Functions
def take_bet(chips):
    while True:

        try:
            print(f'Player Chips Total: ${chips.total}')
            chips.bet = int(input('How many chips would you like to bet? '))
            
        except:
            print("Sorry! Please provide an integer bet!\n")
        else: 
            if chips.bet > chips.total:
                print("Not enough chips! You have {}\n".format(chips.total))
            else:
                break

def hit(deck, hand):
    single_card = deck.deal()
    hand.add_card(single_card)
    hand.adjust_for_ace()

def hit_or_stand(deck, hand):
    global playing

    while True:
        x = input('Hit or Stand? (Enter H or S) ')

        if x[0].upper() == 'H':
            hit(deck, hand)

        elif x[0].upper() == 'S':
            print("Player Stands - Dealer's Turn\n")
            playing = False
        else:
            print('Invalid Input!\n')
            continue
        break

def show_some(player, dealer):
    #Show only one of the dealer's card
    print("\n Dealer's Hand:  ")
    print(dealer.hand[0])
    print("Second Card Hidden!")

    #Show all of the player's cards
    print("\n Player's Hand: ")
    for x in range(len(player.hand)):
        print(player.hand[x-1])

def show_all(player, dealer):
    #Show all the dealer's cards and crunch the total value - Toying around with print function
    print("\n----------------\n\n Dealer's Hand: ", *dealer.hand, sep='\n')
    print(f"Value of Dealer's Hand: {dealer.value}")

    #Show all the player's cards
    print("\n Player's Hand: ", *player.hand, sep='\n')
    print(f"Value of Player's Hand: {player.value}")

def player_busts(player, dealer, chips):
    print("PLAYER HAS BUSTED!")
    chips.remove_chips()

def player_wins(player, dealer, chips):
    print("PLAYER HAS WON THE HAND!")
    chips.add_chips()

def dealer_busts(player, dealer, chips):
    print("DEALER HAS BUSTED!")
    chips.add_chips()

def dealer_wins(player, dealer, chips):
    print("DEALER HAS WON THE HAND!")
    chips.remove_chips()

def push(player, dealer):
    print('Dealer and Player tie - PUSH!')

# ---------------------- Game Logic --------------------------------

while True:
    print("Welcome to Blackjack!")
    
    #Create a new deck
    deck = Deck()
    deck.shuffle()

    #Setup Player and Chips
    player_hand = Player()
    player_hand.add_card(deck.deal())
    player_hand.add_card(deck.deal())

    #Setup for CPU
    dealer_hand = Player() 
    dealer_hand.add_card(deck.deal())
    dealer_hand.add_card(deck.deal())

    #Setup for Player's Chips
    player_chips = Chips()

    #Ask player for their bet
    take_bet(player_chips)

    #First time showing cards (Keep one of dealer's cards hidden)
    show_some(player_hand, dealer_hand)

    while playing:

        #Ask player to Hit or Stand
        hit_or_stand(deck, player_hand)
        show_some(player_hand, dealer_hand) #Update

        #If player's hand > 21, run bust and break loop
        if player_hand.value > 21:
            player_busts(player_hand, dealer_hand, player_chips)
            break
    
    # Dealer Logic
    if player_hand.value <= 21:

        # Soft 17 Rule
        while dealer_hand.value < player_hand.value:
            hit(deck, dealer_hand)
        
        # Update showing of cards (Show all since it is the dealer's turn to play)
        show_all(player_hand, dealer_hand)

        # Lets code in all the scenarios! YAY!
        if dealer_hand.value > 21:
            dealer_busts(player_hand, dealer_hand, player_chips)
        elif dealer_hand.value > player_hand.value:
            dealer_wins(player_hand, dealer_hand, player_chips)
        elif dealer_hand.value < player_hand.value:
            player_wins(player_hand, dealer_hand, player_chips)
        else:
            push(player_hand, dealer_hand)
    
    print(f'\n Player total chips: ${player_chips.total}')

    new_game = input("Would you like to play another hand? (Y/N) ")

    if new_game[0].upper() == 'Y':
        playing = True
        continue
    else:
        print('Thank you for playing!')
        break