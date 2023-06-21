import pygame
import sys

kaarten = []

pygame.init()

screen = pygame.display.set_mode((1200, 700))
clock = pygame.time.Clock()
running = True

font = pygame.font.SysFont('Arial', 40)

pygame.display.set_caption('Set')


objects = []

class Button():
    
    def __init__(self, x, y, width, height, buttonText='Set', onclickFunction=None, onePress=False):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.onclickFuntion = onclickFunction
        self.onePress = onePress
        self.alreadyPressed = False

        self.fillColors = {
            'normal': 'gray77',
            'hover': 'gray61',
            'pressed': 'gray48'
        }

        self.buttonSurface = pygame.Surface((self.width, self.height))
        self.buttonRect = pygame.Rect(self.x, self.y, self.width, self.height)

        self.buttonSurf = font.render(buttonText, True, (20, 20, 20))
        
        objects.append(self)

    def onclick(self):
        mousePos = pygame.mouse.get_pos()
        self.buttonSurface.fill(self.fillColors['normal'])
        if self.buttonRect.collidepoint(mousePos):
            self.buttonSurface.fill(self.fillColors['hover'])
            if pygame.mouse.get_pressed(num_buttons=3)[0]:
                self.buttonSurface.fill(self.fillColors['pressed'])
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

    def drawStack():
        kaarten = ['greendiamondempty1', 'greendiamondempty2', 'greendiamondempty3', 'greendiamondfilled1', 'greendiamondfilled2', 'greendiamondfilled3'
           , 'greendiamondempty1', 'greendiamondempty2', 'greendiamondempty3', 'greendiamondfilled1', 'greendiamondfilled2', 'greendiamondfilled3']
        

drawStackButton = Button(100, 100, 100, 50, 'Draw stack', Button.drawStack)

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("forestgreen")
    
    for i in range(6):
        try:
            kaart = pygame.image.load("C:\\Users\\Thijs\\OneDrive\\Uni\\PythonR\\project\\kaarten\\" + kaarten[i] + ".gif").convert()
            screen.blit(kaart, (175+150*i,100))
            kaart2 = pygame.image.load("C:\\Users\\Thijs\\OneDrive\\Uni\\PythonR\\project\\kaarten\\" + kaarten[6+i] + ".gif").convert()
            screen.blit(kaart2, (175+150*i, 400))
        except IndexError:
            pass

    for object in objects:
        object.onclick()

    pygame.display.flip()

    clock.tick(60)

pygame.quit()

