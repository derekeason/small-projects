"""
The classic card game also known as 21. (This version
doesn't have splitting or insurance.)
More info at: https://en.wikipedia.org/wiki/Blackjack

"""
import random, sys

# Setup the constraints:
HEARTS = chr(9829)
DIAMONDS = chr(9830)
SPADES = chr(9824)
CLUBS = chr(9827)
BACKSIDE = 'backside'

def main():
    print('''
    
    Rules:

        Try to get as close to 21 without going over.
        Kings, Queens, and Jacks are worth 10 points.
        Aces are worth either 1 or 11 points.
        Cards 2 through 10 are worth their face value.
        (H)it to take another card.
        (S)tand to stop taking cards.
        On your first play, you can (D)ouble down to increase
        your bet but must hit exactly one more time before
        standing. In case of a tie, the bet is returned to
        the player. The dealer stops hitting at 17.

        ''')    

    money = 5000
    while True:
        if money <= 0: # check if player has run out of money
            print("You're broke!")
            print("Good thing you weren't playing with real money.")
            print('Thanks for playing!')
            sys.exit()

        print('Money:', money)
        bet = getBet(money) 

        deck = getDeck() # gives the dealer and player two cards from the deck each
        dealerHand = [deck.pop(), deck.pop()]
        playerHand = [deck.pop(), deck.pop()]

        print('Bet:', bet)
        while True: # keep looping until player stands or busts
            displayHands(playerHand, dealerHand, False)
            print()
            
            if getHandValue(playerHand) > 21:
                break
        
            # get player's move, either H, S, or D:
            move = getMove(playerHand, money - bet)
        
            # handle the player actions:
            if move == 'D':
                # player is doubling down, they can increase their bet:
                additionalBet = getBet(min(bet, (money - bet)))
                bet += additionalBet
                print(f'Bet increase to {bet}.')
                print('Bet:', bet)
            
            if move in ('H', 'D'):
                # hit or doubling down takes another card
                newCard = deck.pop()
                rank, suit = newCard
                print(f'You drew a {rank} of {suit}.')
                playerHand.append(newCard)
            
                if getHandValue(playerHand) > 21:
                    continue # the player busted

            if move in ('S', 'D'):
                break
        # handle the dealer's actions:
        if getHandValue(playerHand) <= 21:
            while getHandValue(dealerHand) < 17:
                print('Dealer hits...')
                dealerHand.append(deck.pop())
                displayHands(playerHand, dealerHand, False)

            if getHandValue(dealerHand) > 21:
                break # the dealer busted
            input('Press Enter to continue...\n\n')

        # show the final hands:
        displayHands(playerHand, dealerHand, True)

        playerValue = getHandValue(playerHand)
        dealerValue = getHandValue(dealerHand)

        # see if player won, lost or tied:
        if dealerValue > 21:
            print(f'Dealer busts! You win ${bet}!')
            money += bet
        elif (playerValue > 21) or (playerValue < dealerValue):
            print('You lost!')
            money -= bet
        elif playerValue > dealerValue:
            print(f'You won ${bet}!')
            money += bet
        elif playerValue == dealerValue:
            print("It's a tie, the bet is returned to you...")

        input('Press Enter to continue...\n\n')

def getBet(maxBet):
    '''
    Ask the player how much they want to bet for this round.
    '''
    while True:
        print(f'How much do you bet? (1 - {maxBet}), or QUIT')
        bet = input('> ').upper().strip()
        if bet == 'QUIT':
            print('Thanks for playing!')
            sys.exit()

        if not bet.isdecimal():
            continue # asks again if player didn't enter a number

        bet = int(bet)
        if 1 <= bet <= maxBet:            
            return bet # player entered a valid bet.        


def getDeck():
    deck = []
    for suit in (HEARTS, DIAMONDS, SPADES, CLUBS):
        for rank in range(2, 11):
            deck.append((str(rank), suit)) # numbered cards
        for rank in ('J', 'Q', 'K', 'A'):
            deck.append((rank, suit)) # face and ace cards

    random.shuffle(deck)
    return deck

def displayHands(playerHand, dealerHand, showDealerHand):
    """
    Show the player's and dealer's cards. Hide the dealer's 
    first card if showDealerHand is False.
    """
    print()
    if showDealerHand:
        print('DEALER:', getHandValue(dealerHand))
        displayCards(dealerHand)
    else:
        print('DEALER: ???')
        displayCards([BACKSIDE] + dealerHand[1:]) # hide dealer's first card

    print('PLAYER:', getHandValue(playerHand))
    displayCards(playerHand)

def getHandValue(cards):
    """
    Returns the value of the cards. Face cards are worth 10, aces are
    worth 11 or 1 (this function picks the most suitable ace value).
    """
    value = 0
    numberOfAces = 0

    # add the value for the non-ace cards:
    for card in cards:
        rank = card[0] # card is tuple like (rank, suit)
        if rank == 'A':
            numberOfAces +=1
        elif rank in ('K', 'Q', 'J'):
            value += 10 # face cards are worth 10 points
        else: value += int(rank) # number cards are worth their number

    # add the value for the aces:
    value += numberOfAces # add 1 per ace
    for i in range(numberOfAces):
        if value + 10 <= 21:
            value += 10
    
    return value

def displayCards(cards):
    """
    Display all the cards in the cards list.
    """
    rows = ['', '', '', '', ''] # the text to display on each row

    for i, card in enumerate(cards):
        rows[0] += ' ____ ' # print the top line of the card
        if card == BACKSIDE:
            rows[1] += '|## | '
            rows[2] += '|###| '
            rows[3] += '|_##| '
        else:
             # Print the card's front:
             rank, suit = card  # The card is a tuple data structure.
             rows[1] += '|{} | '.format(rank.ljust(2))
             rows[2] += '| {} | '.format(suit)
             rows[3] += '|_{}| '.format(rank.rjust(2, '_'))

    for row in rows:
        print(row)


def getMove(playerHand, money):
    """
    Asks the player for their move, and returns 'H' for hit, 'S' for
    stand, and 'D' for double down.
    """
    while True:
        moves = ['(H)it', '(S)tand']

        # the player can double down on their first move, which we can
        # tell because they'll have exactly two cards:
        if len(playerHand) == 2 and money > 0:
            moves.append('(D)ouble down')

        movePrompt = ',  '.join(moves) + '> '
        move = input(movePrompt).upper()
        if move in ('H', 'S'):
            return move # player entered a valid move
        if move == 'D' and '(D)ouble down' in moves:
            return move # player entered a valid move


if __name__ == '__main__':
    main() 
        

