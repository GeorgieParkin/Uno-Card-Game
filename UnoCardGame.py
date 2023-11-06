
import random

class Card():
    def __init__ (self):
        pass

class NumberCard(Card):
    def __init__(self, value, colour):
        self.value = value
        self.colour = colour
        self.function = None

    def getName(self):
        return str(self.value) + self.colour

class ColourSpecialCard(Card):
    def __init__(self, function, colour):
        self.function = function
        self.colour = colour
        self.value = 20
        
    def getName(self):
        return self.colour + " " + self.function

class WildCard(Card):
    def __init__(self, function):
        self.function = function
        self.value = 50
        self.colour = None
    def getName(self):
        return self.function

class Player():
    def __init__(self,name):
        self.name = name
        self.hand = []
        self.calledUno = False

    def showHand(self):
        print("Here is your hand")
        cardnum = 1
        for k,c in enumerate(self.hand): 
            #enumerate takes list of items and gives each one a number
            #K is the number
            #c is the card
            print(k+1,": ", c.getName())
    def takeTurn(self, topcard, currentColour, game):
        #show hand
        self.showHand()
        #check if they can play if not give card
        valid = False
        for c in self.hand:
            if self.cardMatch(c, topcard, game):
                valid = True
        if not valid:
            print("You have no valid card, dealing an extra")
            game.deal(self,1)
            self.showHand()
            if not self.cardMatch(self.hand[-1], topcard):
                print("You still can not play. Miss a turn")
                return None
        valid = False
        while not valid:
            choice = input("Choose a card (1-" + str(len(self.hand)) + ") or U for Uno")
            if choice.upper == "U":
                #uno
                pass
            else:
                if choice.isdigit() and 1 <= int(choice) <= len(self.hand):
                    if self.cardMatch (self.hand[int(choice)-1], topcard, game):
                        valid = True
                        print("Playing", self.hand[int(choice)-1].getName())
                        return self.hand[int(choice)-1]
                if not valid:
                    print("That is not a valid choice")
        #check if the can play again if not end turn
        #ask which card or UNO
        #if Uno record (calledUno)
        #check if card is valid - if not ask again
        #return chosen card
    def cardMatch(self, c, topcard, game):
        valid = False
        if type(c) is WildCard:
            valid = True
        elif c.colour == topcard.colour or c.colour == game.currentColour:
            valid = True
        elif type(c) is NumberCard and c.value == topcard.value:
            valid = True
        elif c.function is not None and c.function == topcard.function:
            valid = True
        return valid
class Game():
    def __init__(self, numPlayers):
        self.makeDeck()
        self.discards = []
        self.players = []
        self.direction = 1
        for x in range(1,numPlayers+1):
            self.players.append(Player("Player " + str(x)))
            self.deal(self.players[-1], 7)
            #self.players[-1].showHand()
        self.runGame()

    def runGame(self):
        self.currentPlayer = -1
        self.effectActive = True
        self.discards.append(self.deck.pop())
        #self.discards.append(NumberCard(99, "K"))
        if type(self.discards[-1]) is WildCard:
            print("First card is a wild card")
            self.currentColour = input ("Pick a colour (R, G, B, Y)")
        else:
            self.currentColour = self.discards[-1].colour
        if self.discards[-1].function == "Reverse":
            self.direction = -1
            self.currentPlayer = 0
        while True:
            self.currentPlayer = (self.currentPlayer + self.direction) % len(self.players)
            topcard = self.discards[-1]
            print("\n"*50)
            print(self.players[self.currentPlayer].name + "'s turn")
            print("Top card is")
            print(topcard.getName())
            if type(topcard) is WildCard:
                print("Colour is", self.currentColour)
            if topcard.function == "Block" and self.effectActive:
                self.effectActive = False
                print("You skip your turn")
                input("press Enter to continue")
                continue
            if topcard.function == "+2" and self.effectActive:
                self.deal(self.players[self.currentPlayer], 2)
                self.effectActive = False
                input("press Enter to continue")
                continue
            if topcard.function == "+4Wild" and self.effectActive:
                self.deal(self.players[self.currentPlayer], 4)
                self.effectActive = False
                input("press Enter to continue")
                continue
            cardPlayed = self.players[self.currentPlayer].takeTurn(topcard, self.currentColour, self)
            if cardPlayed is not None:
                #remove it from the players's hand
                self.players[self.currentPlayer].hand.remove(cardPlayed)
                #put it in the discards
                self.effectActive = True
                self.discards.append(cardPlayed)
                if len(self.players[self.currentPlayer].hand) == 0:
                    print(self.players[self.currentPlayer].name, "is the winner")
                    break
                if type(self.discards[-1]) is WildCard:
                    print("First card is a wild card")
                    self.currentColour = input ("Pick a colour (R, G, B, Y)")
                else:
                    self.currentColour = self.discards[-1].colour
                if self.discards[-1].function == "Reverse":
                     self.direction = -1
                     self.currentPlayer = 0


    def deal(self, player, numCards):
        for x in range(numCards):
            newCard = self.deck.pop()
            player.hand.append(newCard)
            

    def makeDeck(self):
        self.deck = []
        for colour in ["R", "Y", "G", "B"]:
            for value in range (0,10):
                self.deck.append(NumberCard(value,colour))
                if value != 0:
                    self.deck.append(NumberCard(value,colour))
        for colour in ["R", "Y", "G", "B"]:
            for function in ["Block", "Reverse", "+2"]:
                self.deck.append(ColourSpecialCard(function,colour))
                self.deck.append(ColourSpecialCard(function,colour))
        for x in range(4):
            self.deck.append(WildCard("Wild"))
            self.deck.append(WildCard("+4Wild"))

        random.shuffle(self.deck)
        #for c in self.deck:
        #    print(c.getName())

theGame = Game(3)