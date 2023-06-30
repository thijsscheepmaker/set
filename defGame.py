import pygame
import random
import os

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
title = pygame.font.SysFont('Arial', 40)

#maakt dat op de window van het programma Set staat
pygame.display.set_caption('Set')

pot_set = []

kaarten = []

objects = []

computer = 0
speler = 0

folder_location = str.replace(__file__, "defGame.py", "kaarten")

colours = {0: 'green', 1: 'purple', 2: 'red'} #verschillende dictionaries waarbij het kenmerk (value) wordt gekoppeld aan de keys.
shapes = {0: 'diamond', 1: 'oval', 2: 'squiggle'}
filling = {0: 'empty', 1: 'filled', 2: 'shaded'}
amount = {0: '1', 1: '2', 2: '3'}

class Card: #deze classe staat staat symbool van een kaart uit het spel
    def __init__(self, kleur, vorm, opvulling, aantal): #de verschillende kenmerken/atributen van de kaarten
        self.kleur = kleur
        self.vorm = vorm
        self.opvulling = opvulling
        self.aantal = aantal
        self.eigenschappen = (kleur, vorm, opvulling, aantal) #een tuple met de vier eigenschappen.

    def is_set(self, kaart1, kaart2): #kijkt of 2 kaarten een set vormen met de huidige kaart.
        def allemaal_hetzelfde(v0, v1, v2): #kijkt of kenmerken gelijk zijn.
            return v0 == v1 and v1 == v2

        def allemaal_anders(v0, v1, v2): #kijkt of de kenmerken allemaal anders zijn.
            return len({v0, v1, v2}) == 3

        return all(allemaal_hetzelfde(v0, v1, v2) or allemaal_anders(v0, v1, v2) #True als er een set is en False als er geen set is. 
                   for (v0, v1, v2) in zip(self.eigenschappen,
                                            kaart1.eigenschappen, 
                                            kaart2.eigenschappen))

    @staticmethod
    def alle_kaarten(): #staticmethod die een lijst van alle mogelijke combinaties tussen de kaarten maakt. Rekening houdend met de kenmerken uiteraard. Voor elke combinatie wordt een object in Card gemaakt.
        return [Card(eigenschap1, eigenschap2, eigenschap3, eigenschap4)
                for eigenschap1 in (0, 1, 2)
                for eigenschap2 in (0, 1, 2)
                for eigenschap3 in (0, 1, 2)
                for eigenschap4 in (0, 1, 2)
                ]
    
    def __str__(self):
        return str(self.eigenschappen)

class Table: #deze classe staat voor de stapel met kaarten, waarbij deck staat voor een lijst van alle kaarten en cards staat voor de huidige kaarten op de tafel.
    def __init__(self, n=12): #in eerste instantie 12 kaarten van de stapel pakken die op tafel moeten komen liggen.                       
        self.deck = Card.alle_kaarten() #alle kaarten zitten nog in de stapel.
        drawn_idxs = random.sample(range(81), n) #welke random kaarten moeten van de stapel gekozen worden wordt hier bepaald.
        self.cards = [self.deck[i] for i in range(81) if i in drawn_idxs] #deze getrokken kaarten aan de kaarten op tafel toevoegen.
        self.deck = [self.deck[i] for i in range(81) if i not in drawn_idxs] #niet getrokken kaarten komen niet op tafel.

    def kaart_van_tafel_halen(self, idx): #een lijst met indexen die de bijbehorende kaarten van de tafel zal verwijderen uit de cards lijst.                 
        n = len(self.cards)
        self.cards = [self.cards[i] for i in range(n) if i not in idx]
        return self.cards
         
    def nieuwe_kaart_trekken(self): #pakt een kaart uit deck, waarbij deze kaart uit de stapel wordt gehaald en toegevoegd aan de lijst met kaarten op tafel.                                
        n = len(self.deck)
        idx = random.randint(0, n-1)
        new_card = self.deck.pop(idx)
        self.cards.append(new_card)
        return new_card

    def __str__(self):
        return str(self.cards)

    def vind_set(self): #uit de huidige kaarten op tafel worden de sets gezocht. Hierbij wordt naar elke mogelijke combinatie van de kaarten gekeken of ze een set vormen.
        found = [] #hierin zit de set.
        idxs = [] #index van de kaarten die de set vormen. Met index wordt de index van de kaarten op tafel bedoeld, waarbij ze in een lijn zijn gelegd ipv een rechthoek.
        for i, ci in enumerate(self.cards):
            for j, cj in enumerate(self.cards[i+1:], i+1):
                for k, ck in enumerate(self.cards[j+1:], j+1):
                    if ci.is_set(cj, ck): #is set wordt gebruikt om te kijkenk of er een set gevormd wordt.
                        found.append((ci, cj, ck))
                        idxs.append((i,j,k))
        return found, idxs

    def naam_kaart(self):
        return [str(c) for c in self.cards]

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
    
    def __init__(self, x, y, width, height, button_text='Set', one_press=False):
        '''Constructor van de knoppen. neemt als input de afmetingen, grootte en tekst op de knop. Er wordt een pygame oppervlak aangemaakt en hierop een vierkant gerenderd en toegevoegd aan de objects lijst.'''
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.onclick_function = self.select_card
        self.one_press = one_press
        self.already_pressed = False
        self.button_text = button_text
        self.button_surface = pygame.Surface((self.width, self.height))
        self.button_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.button_surface.fill('forestgreen')
        self.button_surf = font.render(button_text, True, (20, 20, 20))
        objects.append(self)

    def onclick(self):
        '''Functie neemt zichzelf als input en zorgt dat wanneer er op de knop geklikt wordt, dit wordt geregistreerd door de code en de functie onclick uitgevoerd wordt.'''
        mouse_position = pygame.mouse.get_pos()
        if self.button_rect.collidepoint(mouse_position):
            if pygame.mouse.get_pressed(num_buttons=3)[0]:
                if self.one_press:
                    self.onclick_function()
                elif  not self.already_pressed:
                    self.onclick_function()
                    self.already_pressed = True
            else:
                self.already_pressed = False

        self.button_surface.blit(self.button_surf, [
            self.button_rect.width/2 - self.button_surf.get_rect().width/2,
            self.button_rect.height/2 - self.button_surf.get_rect().height/2
        ])

        screen.blit(self.button_surface, self.button_rect)
    
    def select_card(self):
        '''Functie wordt uitgevoerd als op knop gedrukt wordt en append de gekozen kaart naar de pot_set lijst.'''
        pot_set.append(int(self.button_text)) 
    

#alle kaartknoppen die op het scherm verschijnen. De string met het getal bepaald welke kaart de knop op het bord is.
card_button0 = Button(350, 25, 100, 200, '0')
card_button1 = Button(550, 25, 100, 200, '1')
card_button2 = Button(750, 25, 100, 200, '2')
card_button3 = Button(350, 275, 100, 200, '3')
card_button4 = Button(550, 275, 100, 200, '4')
card_button5 = Button(750, 275, 100, 200, '5')
card_button6 = Button(350, 525, 100, 200, '6')
card_button7 = Button(550, 525, 100, 200, '7')
card_button8 = Button(750, 525, 100, 200, '8')
card_button9 = Button(350, 775, 100, 200, '9')
card_button10 = Button(550, 775, 100, 200, '10')
card_button11 = Button(750, 775, 100, 200, '11')

x = Table()

tafel = x.naam_kaart()

kaarten = Prep.filenames(tafel)

foundsets = []

def goede_set_gegegeven():
    print("Je gegeven antwoord is goed! "+ '\n') #er wordt geprint dat je antwoord goed is.

def foute_set_gegeven(): #wanneer de foute set wordt gegeven worden deze kaarten verwijderd en worden er drie nieuwe kaarten bijgelegd op tafel.
    print('Probeer opnieuw... ')
    kaarten_die_weg_moeten = [0,1,2]
    drie_kaarten_verwijderd = x.kaart_van_tafel_halen(kaarten_die_weg_moeten)
    x.nieuwe_kaart_trekken()
    x.nieuwe_kaart_trekken()
    x.nieuwe_kaart_trekken()
    return drie_kaarten_verwijderd

def computer_vindt_set(): #de computer gaat een set zoeken en zal de eerste set die gevonden wordt van tafel halen en hier drie nieuwe kaarten voor in de plaats leggen.
    gevonden_sets, idxsset = x.vind_set()
    if gevonden_sets:
        kaarten_die_weg_moeten = x.kaart_van_tafel_halen(idxsset[0])
        x.nieuwe_kaart_trekken()
        x.nieuwe_kaart_trekken()
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
    screen.blit(font.render("speler: " + str(speler), True, (0,0,0)), (50,130))
    screen.blit(title.render("Set", True, (255, 215, 0)), (50, 40))

    #over alle objecten in de objectslijst, ofwel, alle knoppen die in het spel zitten, wordt de onclick functie uitgevoerd die bepaald of er op de knop gedrukt is.
    for object in objects:
        object.onclick()
    
    #deze loop importeert alle gifs van de kaarten van de gebruiker naar de game, en print deze vervolgens over de knoppen van de kaarten op het scherm.
    for i in range(3):
            kaart = pygame.image.load(folder_location + "\\" + kaarten[i] + ".gif").convert()
            screen.blit(kaart, (350+200*i,25))
            kaart2 = pygame.image.load(folder_location + "\\" + kaarten[3+i] + ".gif").convert()
            screen.blit(kaart2, (350+200*i, 275))
            kaart3 = pygame.image.load(folder_location + "\\" + kaarten[6+i] + ".gif").convert()
            screen.blit(kaart3, (350+200*i, 525))
            kaart4 = pygame.image.load(folder_location + "\\" + kaarten[9+i] + ".gif").convert()
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
                x.nieuwe_kaart_trekken()
                x.nieuwe_kaart_trekken()
                x.nieuwe_kaart_trekken()
                tafel = x.naam_kaart()
                kaarten = Prep.filenames(tafel)
                pot_set.clear()
            
            #als de speler geen set maakt met de gekozen kaarten worden de kaarten alsnog verwijdert, krijgt de computer een punt en worden er nieue kaarten getrokken.
            else:
                print('Dit is geen set...')
                removed_cards = computer_vindt_set()
                tafel = x.naam_kaart()
                kaarten = Prep.filenames(tafel)
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

