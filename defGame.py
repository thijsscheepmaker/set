import pygame
import random

#pygame setup
pygame.init()

#hier wordt het scherm aangemaakt door afmetingen in te voeren en de clock van het spel gemaakt. running = True geeft aan dat de while loop verder beneden kan gaan lopen.
screen = pygame.display.set_mode((900, 1000))
clock = pygame.time.Clock()
running = True

level = 20

timer, tijd = level, str(level).rjust(3)

#zet een timer die gestart wordt als de gebruiker een actie doet en die duurt tot de waarde level*100 is afgeteld.
pygame.time.set_timer(pygame.USEREVENT, level*100)

#bepaald het lettertype en de grootte van de tekst voor de game.
font = pygame.font.SysFont('Arial', 23)

#maakt dat op de window van het programma Set staat
pygame.display.set_caption('Set')

pot_set = []

kaarten = []

objects = []

computer = 0
speler = 0

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
        self.eigenschappen = (kleur, vorm, opvulling, aantal)

    def is_set(self, kaart1, kaart2):
        def allemaal_hetzelfde(v0, v1, v2):
            return v0 == v1 and v1 == v2

        def allemaal_anders(v0, v1, v2):
            return len({v0, v1, v2}) == 3

        return all(allemaal_hetzelfde(v0, v1, v2) or allemaal_anders(v0, v1, v2)
                   for (v0, v1, v2) in zip(self.eigenschappen,
                                            kaart1.eigenschappen, 
                                            kaart2.eigenschappen))

    
    @staticmethod
    def alle_kaarten():
        return [Card(eigenschap1, eigenschap2, eigenschap3, eigenschap4)
                for eigenschap1 in (0, 1, 2)
                for eigenschap2 in (0, 1, 2)
                for eigenschap3 in (0, 1, 2)
                for eigenschap4 in (0, 1, 2)
                ]
    
    def __str__(self):
        return str(self.eigenschappen)

class Table:
    def __init__(self, n=12):                       
        self.deck = Card.alle_kaarten()
        drawn_idxs = random.sample(range(81), n)
        self.cards = [self.deck[i] for i in range(81) if i in drawn_idxs]
        self.deck = [self.deck[i] for i in range(81) if i not in drawn_idxs]

    def kaart_van_tafel_halen(self, idx):                 
        n = len(self.cards)
        self.cards = [self.cards[i] for i in range(n) if i not in idx]
        return self.cards
         
    def nieuwe_kaart_trekken(self):                                
        n = len(self.deck)
        idx = random.randint(0, n-1)
        new_card = self.deck.pop(idx)
        self.cards.append(new_card)
        return new_card

    def __str__(self):
        return str(self.cards)

    def vind_set(self):
        found = []
        idxs = []
        for i, ci in enumerate(self.cards):
            for j, cj in enumerate(self.cards[i+1:], i+1):
                for k, ck in enumerate(self.cards[j+1:], j+1):
                    if ci.is_set(cj, ck):
                        found.append((ci, cj, ck))
                        idxs.append((i,j,k))
        return found, idxs

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
        '''Neemt als input lijst van tuples van kaarten, en maakt van deze tuples de naam van het bestand van de kaart'''
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
    
    def __init__(self, x, y, width, height, buttonText='Set', onePress=False):
        '''Constructor van de knoppen. neemt als input de afmetingen, grootte en tekst op de knop. Er wordt een pygame oppervlak aangemaakt en hierop een vierkant gerenderd en toegevoegd aan de objects lijst.'''
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
        '''Functie neemt zichzelf als input en zorgt dat wanneer er op de knop geklikt wordt, dit wordt geregistreerd door de code en de functie onclick uitgevoerd wordt.'''
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
        '''Functie wordt uitgevoerd als op knop gedrukt wordt en append de gekozen kaart naar de pot_set lijst.'''
        pot_set.append(int(self.buttonText)) 
    

#alle kaartknoppen die op het scherm verschijnen. De string met het getal bepaald welke kaart de knop op het bord is.
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

x = Table()

Tafel = x.naam_kaart()

kaarten = Prep.filenames(Tafel)

foundsets = []

def goede_set_gegegeven():
    print("Je gegeven antwoord is goed! "+ '\n')

def foute_set_gegeven():
    print('Probeer opnieuw... ')
    kaarten_die_weg_moeten = [0,1,2]
    drie_kaarten_verwijderd = x.kaart_van_tafel_halen(kaarten_die_weg_moeten)
    x.nieuwe_kaart_trekken()
    x.nieuwe_kaart_trekken()
    x.nieuwe_kaart_trekken()
    return drie_kaarten_verwijderd

def computer_vindt_set():
    gevonden_sets, idxsset = x.vind_set()
    if gevonden_sets:
        kaarten_die_weg_moeten = x.kaart_van_tafel_halen(idxsset[0])
        for i in range(3):
            x.nieuwe_kaart_trekken()
        print(idxsset)

    else:
        kaarten_die_weg_moeten = foute_set_gegeven()
    return kaarten_die_weg_moeten

#hier start de gameloop
while running:

    #loopt over alle gebeurtenissen uit de eventlog van pygame om deze te analyseren.
    for event in pygame.event.get():

        #zorgt ervoor dat wanneer er op het kruisje wordt geklikt, de game afsluit.
        if event.type == pygame.QUIT:
            running = False
        
        #zorgt ervoor dat wanneer de gebruiker iets doet, de tijd begint te lopen.
        if event.type == pygame.USEREVENT:
            timer -= 1
            if timer > 0:
                tijd = str(timer).rjust(3)
            else: tijd = 'Tijd is om!'

    #vult het scherm met de achtergrondkleur donkergroen.
    screen.fill("forestgreen")

    #hier worden een aantal dingen op het scherm geprint. De tijd, de score van de computer en de score van de speler.
    screen.blit(font.render(tijd, True, (0,0,0)), (560, 25))
    screen.blit(font.render("computer: " + str(computer), True, (0,0,0)), (50,100))
    screen.blit(font.render("speler: " + str(speler), True, (0,0,0)), (50,150))

    #over alle objecten in de objectslijst, ofwel, alle knoppen die in het spel zitten, wordt de onclick functie uitgevoerd die bepaald of er op de knop gedrukt is.
    for object in objects:
        object.onclick()
    
    #deze loop importeert alle gifs van de kaarten van de gebruiker naar de game, en print deze vervolgens over de knoppen van de kaarten op het scherm.
    for i in range(3):
            kaart = pygame.image.load("C:\\Users\\Thijs\\OneDrive\\Uni\\PythonR\\project\\kaarten\\" + kaarten[i] + ".gif").convert()
            screen.blit(kaart, (350+200*i,25))
            kaart2 = pygame.image.load("C:\\Users\\Thijs\\OneDrive\\Uni\\PythonR\\project\\kaarten\\" + kaarten[3+i] + ".gif").convert()
            screen.blit(kaart2, (350+200*i, 275))
            kaart3 = pygame.image.load("C:\\Users\\Thijs\\OneDrive\\Uni\\PythonR\\project\\kaarten\\" + kaarten[6+i] + ".gif").convert()
            screen.blit(kaart3, (350+200*i, 525))
            kaart4 = pygame.image.load("C:\\Users\\Thijs\\OneDrive\\Uni\\PythonR\\project\\kaarten\\" + kaarten[9+i] + ".gif").convert()
            screen.blit(kaart4, (350+200*i, 775))

    #als de speler drie kaarten heeft gekozen, wordt deze keuze geformateerd zodat deze geanalyseerd kan worden door de algoritme's
    if len(pot_set) == 3:
        gekozen_kaarten = str(pot_set[0]) + ',' + str(pot_set[1]) + ',' + str(pot_set[2])
        gekozen_positie = []

        #split de gekozen kaarten en sorteert deze op grootte, zodat het niet kan voorkomen dat een set niet herkend wordt door de verkeerde volgorde van keuze.
        for positie in gekozen_kaarten.split(","):
            positie = positie.strip()
            gekozen_positie.append(int(positie))
            gekozen_positie.sort()
        print(gekozen_positie)

        #controleert of alle gekozen posities tussen 0 en 11 liggen.
        if all(0 <= positie <= (len(x.cards)-1) for positie in gekozen_positie):
            gekozen_kaarten = [x.cards[positie] for positie in gekozen_positie]
            gekozen_kaarten = []

            #append de daadwerkelijke kaarten in de gekozen kaarten lijst, in plaats van de posities.
            for positie in gekozen_positie:
                gekozen_kaarten.append(x.cards[positie])

            print(gekozen_kaarten)

            #er wordt gecontroleerd of de gekozen kaarten een set vormen, als dit het geval is krijgt de speler een punt
            if gekozen_kaarten[0].is_set(gekozen_kaarten[1], gekozen_kaarten[2]):
                goede_set_gegegeven()
                speler = speler + 1
                verwijder_kaart_uit_tabel = []

                #de gekozen kaarten worden uit het spel gehaald zodat de zelfde set niet een tweede keer gekozen kan worden
                for positie in gekozen_positie:
                    verwijder_kaart_uit_tabel.append(positie)
                x.kaart_van_tafel_halen(verwijder_kaart_uit_tabel)

                #er worden drie nieuwe kaarten getrokken en deze worden opnieuw op het scherm geprint nadat de kaarten lijst is bijgewerkt via de filenames functie
                for i in range(3):
                    x.nieuwe_kaart_trekken()
                Tafel = x.naam_kaart()
                kaarten = Prep.filenames(Tafel)
                pot_set.clear()
            
            #als de speler geen set maakt met de gekozen kaarten worden de kaarten alsnog verwijdert, krijgt de computer een punt en worden er nieue kaarten getrokken.
            else:
                print('Dit is geen set...')
                removed_cards = computer_vindt_set()
                Tafel = x.naam_kaart()
                kaarten = Prep.filenames(Tafel)
                computer = computer + 1
                pot_set.clear()
        else:
            print('Je moet een kaart kiezen.')
        print("voorbij")
        pot_set.clear()
    
    #dit rendert alle code boven op het scherm en staat dus helemaal onderaan.
    pygame.display.flip()

    clock.tick(60)

#sluit de pygame sessie af
pygame.quit()

