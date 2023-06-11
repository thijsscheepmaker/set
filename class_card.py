class card:
    #kleur = ["green", "purple", "red"]
    
    #vorm = ["diamond", "ovale", "squiggle"]
    
    #vulling = ["empty", "filled", "shaded"]
    
    #aantal = [1, 2, 3]

    def __init__(self, kleur = 0, vorm = 0, vulling = 0, aantal = 0):
        self.kleur = kleur
        self.vorm = vorm
        self.vulling = vulling
        self.aantal = aantal

    def show(self):
        print("{}{}{}{}".format(self.kleur, self.vorm, self.vulling, self.aantal))

    #def __list__(self):
    #    lijst = [self.kleur, self.vorm, self.vulling, self.aantal]
    #    return lijst
    
    #def __str__(self):
    #    lijst = [self.kleur, self.vorm, self.vulling, self.aantal]
    #    return ''.join(lijst)

class deck:

    def __init__(self):
        self.cards = []
        self.build()

    def build(self):
        for kleur in ["green", "purple", "red"]:
            for vorm in ["diamond", "ovale", "squiggle"]:
                for vulling in ["empty", "filled", "shaded"]:
                    for aantal in [1, 2, 3]:
                        self.cards.append(card(kleur, vorm, vulling, aantal))
                
    def show(self):
        for c in self.cards:
            c.show()
    
    def shuffle(self):
        import random
        for i in range(len(self.cards)-1, 0, -1):
            r = random.randint(0, i)
            self.cards[i], self.cards[r] = self.cards[r], self.cards[i]

    def drawCard(self):
        self.cards.pop()


Deck = deck()
Deck.shuffle()

kaart = Deck.drawCard()
kaart.show()


#Deck.show()
#kaart = card("green", "diamond", "empty", 2)
#kaart.show()
#https://medium.com/@anthonytapias/build-a-deck-of-cards-with-oo-python-c41913a744d3