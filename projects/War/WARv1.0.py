'''
## Thoughts and Notes ##

CARD CLASS
  - Suit, Rank, Value (Tuple)

DECK CLASS
  - New Deck created
    - Create 52 cards objects
    - Hold as a list of card objects <---
        - Returns "Card class object" instances!
  - Shuffle Deck through method call
    - Random library shuffle() function?
  - Deal cards from the Deck object
    - Use pop() method?

PLAYER CLASS
  - Holding area for the cards the player has
  - Ability to play cards from hand
  - Ability to add cards that are won (append --> extend)
    - The reason you don't append won cards is you'll end up making a nested list

Game Logic/Notes:
  - Two Player (NPC) game of WAR. (Two instances of player)
  - Instance of a new deck that needs to be shuffled before splitting the deck between players
  - Check win/loss condition at the top of the round (if 0 cards found --> boolean value changed)
    - while loop with boolean
  - Compare cards that are at play
    - If cards are equal, hop into inner while loop (WAR)
        - 5 cards each player
'''

#Import Library(ies)
import random
import time

#Global Variables
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 'Nine':9, 'Ten':10, 'Jack':11, 'Queen':12, 'King':13, 'Ace':14}
suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')

class Card():

    def __init__(self, suit, rank):
        self.suit = suit 
        self.rank = rank 
        self.value = values[rank] # Workhorse

    def __str__(self):
        return self.rank + " of " + self.suit

class Deck():

    def __init__(self):
        self.all_cards = []
        for suit in suits:
            for rank in ranks:
                # Create the card object here
                created_card = Card(suit, rank)
                self.all_cards.append(created_card) 

    #Shuffle Deck
    def shuffle(self):
        random.shuffle(self.all_cards)
    
    #Deal one card
    def deal_one(self):
        return self.all_cards.pop()

class Player():
    def __init__(self,name):
        self.name = name
        self.all_cards = []

    def remove_one(self):
        return self.all_cards.pop(0) # Remove top card

    def add_cards(self, new_cards):
        if type(new_cards) == type([]): # Checking if its a list
            self.all_cards.extend(new_cards) # List of multiple card objects incoming
        else: # A single card
            self.all_cards.append(new_cards) # Single instance of card object incoming

    #def __str__(self):
    #   return (f'Player {self.name} has {len(self.all_cards)} cards')

#---------------------------------------------------
# GAME SETUP
#Setup in the instance of the new game
player_one = Player("One")
player_two = Player("Two")

#Create the new deck and shuffle
new_deck = Deck()
new_deck.shuffle()

# Splitting the deck
for x in range(26):
    player_one.add_cards(new_deck.deal_one())
    player_two.add_cards(new_deck.deal_one())

# WHILE LOOP (Game Logic)
Game_On = True
round_num = 0

while Game_On:
    round_num += 1
    print(f'Round Number: {round_num}')

    #Check for loss condition
    if len(player_one.all_cards) == 0:
        #Player Two Wins Condition
        Game_On = False
        print('Player Two wins!')
        break
    
    if len(player_two.all_cards) == 0:
        #Player One Wins Condition
        Game_On = False
        print('Player One wins!')
        break

    
    #Start of the round
    player_one_mat = []
    player_one_mat.append(player_one.remove_one())
    player_two_mat = []
    player_two_mat.append(player_two.remove_one())

    At_War = True 

    #WHILE LOOP (at_war state)
    while At_War:

        #Displays current number of cards in hand
        print(f'Player One({len(player_one.all_cards)}): {player_one_mat[-1]}')
        print(f'Player Two({len(player_two.all_cards)}): {player_two_mat[-1]}') 

        if player_one_mat[-1].value > player_two_mat[-1].value:
            player_one.add_cards(player_one_mat)
            player_one.add_cards(player_two_mat)
            At_War = False
            print('--- Player One wins this match! ---')
            time.sleep(2)
        elif player_one_mat[-1].value < player_two_mat[-1].value:
            player_two.add_cards(player_one_mat)
            player_two.add_cards(player_two_mat)
            At_War = False
            print('--- Player Two wins this match! ---')
            time.sleep(2)
        else:
            print('WAR!')

            if len(player_one.all_cards) < 5:
                print("Player One doesn't have enough cards!")
                print("Player Two wins!")
                Game_On = False
                break
            elif len(player_two.all_cards) < 5:
                print("Player Two doesn't have enough cards!")
                print("Player One wins!")
                Game_On = False
                break
            else:
                print('Each player is drawing additional cards for WAR...')
                time.sleep(2)
                for num in range(5):
                    player_one_mat.append(player_one.remove_one())
                    player_two_mat.append(player_two.remove_one())