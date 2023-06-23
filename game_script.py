import pygame
import random

pygame.init()

screen = pygame.display.set_mode((900, 1000))
clock = pygame.time.Clock()
running = True

level = 20

timer, tijd = level, str(level).rjust(3)

pygame.time.set_timer(pygame.USEREVENT, level*100)

font = pygame.font.SysFont('Arial', 23)

pygame.display.set_caption('Set')

pot_set = []

kaarten = []

objects = []

colours = {0: 'green', 1: 'purple', 2: 'red'}
shapes = {0: 'diamond', 1: 'oval', 2: 'squiggle'}
filling = {0: 'empty', 1: 'filled', 2: 'shaded'}
amount = {0: '1', 1: '2', 2: '3'}

class Card:
    def __init__(self, kleur, vorm, opvulling, aantal):
        self.kleur = kleur
        self.vorm = vorm
        self.opvulling = opvulling
        self.aantal = aantal
        self.attrs = (kleur, vorm, opvulling, aantal)

    def isset(self, kaart1, kaart2):
        def allsame(v0, v1, v2):
            return v0 == v1 and v1 == v2

        def alldifferent(v0, v1, v2):
            return len({v0, v1, v2}) == 3

        return all(allsame(v0, v1, v2) or alldifferent(v0, v1, v2)
                   for (v0, v1, v2) in zip(self.attrs, kaart1.attrs, kaart2.attrs))

    @staticmethod
    def allcards():
        return [Card(att0, att1, att2, att3)
                for att0 in (0, 1, 2)
                for att1 in (0, 1, 2)
                for att2 in (0, 1, 2)
                for att3 in (0, 1, 2)
                ]

    def __str__(self):
        return str(self.attrs)

class Table:
    def __init__(self, n=12):
        self.cards = random.sample(Card.allcards(), n)

    def __str__(self):
        return str(self.cards)

    def findsets_gnt(self):
        found = []
        for i, ci in enumerate(self.cards):
            for j, cj in enumerate(self.cards[i+1:], i+1):
                for k, ck in enumerate(self.cards[j+1:], j+1):
                    if ci.isset(cj, ck):
                        found.append((ci, cj, ck))
        return found

    def findsets_gnt_mod(self):
        found = []
        for i, ci in enumerate(self.cards):
            for j, cj in enumerate(self.cards[i+1:], i+1):
                for k, ck in enumerate(self.cards[j+1:], j+1):
                    if ci.isset(cj, ck):
                        found.append((ci, cj, ck))
        return found

    def naam_kaart(self):
        return [str(c) for c in self.cards]

colours = {0: 'green', 1: 'purple', 2: 'red'}
shapes = {0: 'diamond', 1: 'oval', 2: 'squiggle'}
filling = {0: 'empty', 1: 'filled', 2: 'shaded'}
amount = {0: '1', 1: '2', 2: '3'}

def replace_cards(table):
    del table.cards[:3]
    table.cards[:0] = random.sample(Card.allcards(), 3)

class Prep():
    
    def filenames(cardtup):
        cardfiles = []
        for i in range(len(cardtup)):
            cardfiles.append(str(
                colours.get(int(cardtup[i][1])) +
                shapes.get(int(cardtup[i][4])) +
                filling.get(int(cardtup[i][7])) +
                amount.get(int(cardtup[i][10]))
            ))
        return cardfiles
            
class Button():
    
    def __init__(self, x, y, width, height, buttonText='Set', onclickFunction=None, onePress=False):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.onclickFuntion = self.selectcard
        self.onePress = onePress
        self.alreadyPressed = False
        self.buttonText = buttonText
        self.buttonSurface = pygame.Surface((self.width, self.height))
        self.buttonRect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.buttonSurface.fill('forestgreen')
        self.buttonSurf = font.render(buttonText, True, (20, 20, 20))
        objects.append(self)

    def onclick(self):
        mousePos = pygame.mouse.get_pos()
        if self.buttonRect.collidepoint(mousePos):
            if pygame.mouse.get_pressed(num_buttons=3)[0]:
                if self.onePress:
                    self.onclickFuntion()
                elif  not self.alreadyPressed:
                    self.onclickFuntion()
                    self.alreadyPressed = True
            else:
                self.alreadyPressed = False

        self.buttonSurface.blit(self.buttonSurf, [
            self.buttonRect.width/2 - self.buttonSurf.get_rect().width/2,
            self.buttonRect.height/2 - self.buttonSurf.get_rect().height/2
        ])

        screen.blit(self.buttonSurface, self.buttonRect)
    
    def selectcard(self):
        pot_set.append(int(self.buttonText)) 
    
    def drawcards():
        global kaarten
        z = Table()
        cardtup = z.naam_kaart()
        kaarten = Prep.filenames(cardtup)
        return kaarten

cardButton0 = Button(350, 25, 100, 200, '0')
cardButton1 = Button(550, 25, 100, 200, '1')
cardButton2 = Button(750, 25, 100, 200, '2')
cardButton3 = Button(350, 275, 100, 200, '3')
cardButton4 = Button(550, 275, 100, 200, '4')
cardButton5 = Button(750, 275, 100, 200, '5')
cardButton6 = Button(350, 525, 100, 200, '6')
cardButton7 = Button(550, 525, 100, 200, '7')
cardButton8 = Button(750, 525, 100, 200, '8')
cardButton9 = Button(350, 775, 100, 200, '9')
cardButton10 = Button(550, 775, 100, 200, '10')
cardButton11 = Button(750, 775, 100, 200, '11')

pc = 0
player = 0
z = Table()

Tafel = z.naam_kaart()

print(Tafel)

kaarten = Prep.filenames(Tafel)

foundsets = []

foundsets = z.findsets_gnt()

for tup in foundsets:
    x1 = str(tup[0])
    x2 = str(tup[1])
    x3 = str(tup[2])
    xlijst = [x1, x2, x3]


while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.USEREVENT:
            timer -= 1
            if timer > 0:
                tijd = str(timer).rjust(3)
            else: tijd = 'Tijd is om!'

    screen.fill("forestgreen")

    screen.blit(font.render(tijd, True, (0,0,0)), (560, 25))

    for object in objects:
        object.onclick()
    
    for i in range(3):
            kaart = pygame.image.load("C:\\Users\\Thijs\\OneDrive\\Uni\\PythonR\\project\\kaarten\\" + kaarten[i] + ".gif").convert()
            screen.blit(kaart, (350+200*i,25))
            kaart2 = pygame.image.load("C:\\Users\\Thijs\\OneDrive\\Uni\\PythonR\\project\\kaarten\\" + kaarten[3+i] + ".gif").convert()
            screen.blit(kaart2, (350+200*i, 275))
            kaart3 = pygame.image.load("C:\\Users\\Thijs\\OneDrive\\Uni\\PythonR\\project\\kaarten\\" + kaarten[6+i] + ".gif").convert()
            screen.blit(kaart3, (350+200*i, 525))
            kaart4 = pygame.image.load("C:\\Users\\Thijs\\OneDrive\\Uni\\PythonR\\project\\kaarten\\" + kaarten[9+i] + ".gif").convert()
            screen.blit(kaart4, (350+200*i, 775))

    if len(pot_set) == 3:
        print(str(pot_set[0]) + ' ' + str(pot_set[1]) + ' ' + str(pot_set[2]))
        pot_set.clear()
        
    pygame.display.flip()

    clock.tick(60)

pygame.quit()

