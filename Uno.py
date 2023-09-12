from random import choice,randint
from time import sleep as wait

delay = 1.5

def say(string):
    print(" ")
    print(string)

def split(string,ch):
    res = []
    temp = ""
    for x in string:
        if x!=ch:temp=temp+x
        else:
            res.append(temp)
            temp = ""
    res.append(temp)
    return res

class Game:
    Players = []
    plrTurn = 0
    direction = 1
    Card = None
    cardAmount = 0

    Cards = [
    "0 Blue", "0 Green", "0 Red", "0 Yellow",
    "1 Blue", "1 Green", "1 Red", "1 Yellow",
    "2 Blue", "2 Green", "2 Red", "2 Yellow",
    "3 Blue", "3 Green", "3 Red", "3 Yellow",
    "4 Blue", "4 Green", "4 Red", "4 Yellow",
    "5 Blue", "5 Green", "5 Red", "5 Yellow",
    "6 Blue", "6 Green", "6 Red", "6 Yellow",
    "7 Blue", "7 Green", "7 Red", "7 Yellow",
    "8 Blue", "8 Green", "8 Red", "8 Yellow",
    "9 Blue", "9 Green", "9 Red", "9 Yellow",
    "Add2 Blue", "Add2 Green", "Add2 Red", "Add2 Yellow",
    "Reverse Blue", "Reverse Green", "Reverse Red", "Reverse Yellow",
    "Skip Blue", "Skip Green", "Skip Red", "Skip Yellow",
    "Wild", "WildDraw4"
    ]




    def __init__(self,Players,cardAmount):
        self.Players = Players
        self.cardAmount = cardAmount
        self.Card = self.Cards[randint(0,39)]
        self.direction = 1
        self.pendingCard = 0
        for Player in Players:
            for x in range(self.cardAmount):Player.Cards.append(self.takeCard())

    def takeCard(self):return choice(self.Cards) #str(self.Cards[randint(0,39)])

    def changeTurn(self):
        if self.direction == 1:
            if self.plrTurn<len(self.Players)-1:self.plrTurn+=self.direction
            else:self.plrTurn = 0
        else:
            if self.plrTurn>0:self.plrTurn+=self.direction
            else:self.plrTurn = len(self.Players)-1

    def cardHandler(self,card):
        spl = split(card," ")
        if spl[0] == "Reverse":
            self.direction = -1 if self.direction == 1 else 1
            return "R"
        elif spl[0] == "Skip":
            self.changeTurn()
            return "S"
        if spl[0] == "Add2":
            self.pendingCard +=2
            return self.pendingCard
        elif spl[0] == "WildDraw4":
            self.pendingCard += 4
            return self.pendingCard
            

    def move(self):
        plr = self.Players[self.plrTurn]
        if plr.isPlaying==True:
            print(plr.name+" is Moving...")
            say("Game's card : "+self.Card)
            wait(delay)
            plrmove = plr.move(self.Card,True if self.pendingCard>0 else False)
            process = None
            if plrmove==None:
                if self.pendingCard==0:
                    plr.Cards.append(self.takeCard())
                    print(plr.name+" Has drawn a card")
                    wait(delay)
                    self.changeTurn()
                    return None
                elif self.pendingCard>0:
                    for x in range(self.pendingCard):plr.Cards.append(self.takeCard())
                    say(plr.name+" Has drawn {} cards".format(str(self.pendingCard)))
                    self.pendingCard = 0
                    wait(delay)
                    self.changeTurn()
                    return None
            else:
                for x in plrmove:
                    process = self.cardHandler(x)
                    if process=="R":
                        self.changeTurn()
                        print("The game's direction has been reversed.")
                        self.Card = plrmove[0]
                    elif process=="S":
                        print(self.Players[self.plrTurn].name+" Has been skipped.")
                        self.Card = plrmove[0]
                    elif process==self.pendingCard:
                        print("The game's pending card is now "+str(self.pendingCard))
                        self.Card = plrmove[0]
                    else:self.Card = plrmove[0] 
            print(plr.name+" Has placed "+str(plrmove)+" ({} cards remaining)".format(str(len(plr.Cards)-len(plrmove))))
            for x in plrmove:
                #spl = split(x," ")
                if x in plr.Cards:plr.Cards.remove(x)
                '''if spl[0] == "Wild" or spl[0] == "WildDraw4":
                    plr.Cards.remove(spl)'''
            if len(plr.Cards)==0:
                say(plr.name+" Has finished the game")
                self.Players.remove(plr)
                self.changeTurn()
                if len(self.Players)==1:return False
                return None
            self.changeTurn()

class AddPlayers:
    Cards = None
    isPlaying = False
    MC = False
    name = None

    def __init__(self,name,isMC):
        self.isPlaying = True
        self.name = name
        self.Cards = []
        self.MC = isMC
        self.cardChosen = []

    def loop(self):
        for x in self.Cards: 
            if split(x," ")[0] == split(self.cardChosen[len(self.cardChosen)-1]," ")[0]:self.cardChosen.append(x) #checks for card in hand for the same number

    def check(self,mode):
        for x in self.Cards:
            if mode == 1:
                if split(x," ")[0] == split(self.cardChosen[len(self.cardChosen)-1]," ")[0]:return True
            elif mode == delay:
                if split(x," ")[0] == "Add2" or x == "WildDraw4":return True
        return False

    def move(self,card,pend):
        self.cardChosen = [] 
        if self.isPlaying==True:
            cat1,cat2 = split(card,' ')
            self.cardChosen = []
            if self.MC == False:
                for x in self.Cards: #Card loops
                    spl = split(x," ")
                    if pend == True:
                        if spl[0] == "Add2" or x == "WildDraw4":
                            self.cardChosen.append(x)
                            break
                    else:
                        if x == "Wild" or x == "WildDraw4":
                            self.cardChosen.append(x+choice([" Green"," Red"," Blue"," Yellow"]))
                            self.Cards.remove(x)
                            break
                        elif spl[0]==cat1: #Checking goes here (num)
                            self.cardChosen.append(str(x))
                            self.Cards.remove(x)
                            self.loop()
                            break
                        elif spl[1]==cat2: #Here too (color)
                            self.cardChosen.append(str(x))
                            self.Cards.remove(x)
                            self.loop()
                            break
                if self.cardChosen == []:return None #If no card is True, will return None
                #shuffle(self.cardChosen)
                return self.cardChosen
            if self.MC == True:
                print("Cards : "+str(self.Cards))
                while inp:=input("Move :"): #Asks for input and will run the elif, and else otherwise
                    if self.cardChosen !=[]:
                        print("Chosen Cards : "+str(self.cardChosen))
                    if inp in self.Cards:
                        inpSplit = split(inp," ")
                        if pend == True:
                            if self.check(2)==True:
                                while inp:=input("Move :"):
                                    if inpSplit[0] == "Add2" or inp == "WildDraw4":
                                        self.cardChosen.append(inp)
                                        self.Cards.remove(inp)
                                        print("Added "+inp)
                                    elif inp == "Add":break
                                    else:print("Please add a draw card or draw anyways.")
                            else:break
                        else:
                            if inp == "Wild":
                                if len(self.Cards)>1:
                                    while inp:=input("Add another card or pick a color :"):
                                        if inp in self.Cards:
                                            self.cardChosen.append(inp)
                                            self.cardChosen.append("Wild")
                                            break
                                        elif inp in ["Green","Red","Blue","Yellow"]:
                                            self.cardChosen.append("Wild "+inp)
                                            break
                                elif len(self.Cards)<=1:
                                    while inp:=input("Pleace choose a color :"):
                                        if inp in ["Green","Red","Blue","Yellow"]:
                                            self.cardChosen.append("Wild "+inp)
                                            break
                                break
                            elif inp == "WildDraw4":
                                while inp:=input("Please choose a color :"):
                                    if inp in ["Green","Red","Blue","Yellow"]:
                                            self.cardChosen.append("WildDraw4 "+inp)
                                            break
                                break
                            elif inpSplit[0] == cat1: #checks if number of card is the same
                                self.cardChosen.append(str(inp))
                                self.Cards.remove(inp)
                                if self.check(1) == True:
                                    while inp:=input("Add another card? or put? :"):
                                        if inp in self.Cards:
                                            inpSplit = split(inp," ")
                                            if inpSplit[0] == split(self.cardChosen[len(self.cardChosen)-1]," ")[0]:
                                                self.cardChosen.append(inp)
                                                self.Cards.remove(inp)
                                                print("Chosen Cards : "+str(self.cardChosen))
                                            else:print("Card not matching")
                                        elif inp.lower() == 'put':break
                                        else:print("Card not found")
                                    break
                                else:break
                            elif inpSplit[1] == cat2: #checks if color of the card is the same
                                self.cardChosen.append(str(inp))
                                self.Cards.remove(inp)
                                if self.check(1) == True:
                                    while inp:=input("Add another card? :"):
                                        if inp in self.Cards:
                                            inpSplit = split(inp," ")
                                            if inpSplit[0] == split(self.cardChosen[len(self.cardChosen)-1]," ")[0]:
                                                self.cardChosen.append(inp)
                                                self.Cards.remove(inp)
                                                print("Chosen Cards : "+str(self.cardChosen))
                                            else:print("Card not matching")
                                        elif inp.lower() == 'put':break
                                        else:print("Card not found")
                                    break
                                else:break
                            else:print("Card not match")
                    elif inp.lower()=='draw':return None
                    else:print("Card Doesn't Exist.")
                return self.cardChosen





            

# Setup
plrAmount = int(input("Player amount :"))
cardAm = int(input("Card Amount :"))
mainPlayer = AddPlayers("Player1",True)
mainPlayer.MC = True
plram = 2
plrs = [mainPlayer]
for x in range(plrAmount-1):
    plrs.append(AddPlayers("Player"+str(plram),False))
    plram+=1
game = Game(plrs,cardAm)
# Game
while True:
    a=game.move()
    if a==False:
        say("the game has finished.")
        wait(5)
        break