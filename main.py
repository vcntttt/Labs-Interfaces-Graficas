import pygame
from PIL import Image
import random

class Box:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.x = random.randint(0, self.width)
        self.y = random.randint(0, self.height)
        # Inspirado en demo del profe caro (inspirado -> tremendo plagio)
        self.dX = 0
        self.dY = 0
        self.nR = 0
        self.initImage()

    def initImage(self):
        # L -> Escala de grises
        # Se vuelve a rgb para que sea compatible con pygame
        pilImage = Image.open('assets/box.jpg').convert('L').convert('RGB')
        # capaz me pasé con hacer todo en una linea
        mode , size, data = pilImage.mode , pilImage.size, pilImage.tobytes()

        self.image = pygame.image.fromstring(data, size, mode)

    def update(self):
        self.nR -= 1
        if self.nR < 0:
            self.nR = random.randint(100, 500)
            nDir = random.randint(1, 9)

            if nDir == 1:
                self.dX = +0
                self.dY = -1
            elif nDir == 2:
                self.dX = +1
                self.dY = -1
            elif nDir == 3:
                self.dX = +1
                self.dY = +0
            elif nDir == 4:
                self.dX = +1
                self.dY = +1
            elif nDir == 5:
                self.dX = +0
                self.dY = +1
            elif nDir == 6:
                self.dX = -1
                self.dY = +1
            elif nDir == 7:
                self.dX = -1
                self.dY = +0
            else:
                self.dX = -1
                self.dY = -1

        self.x += self.dX
        self.y += self.dY

        if self.x < 0:
            self.x = 0
            self.nR = 0
        if self.x > 800 - self.image.get_width():
            self.x = 800 - self.image.get_width()

        if self.y < 0:
            self.y = 0
            self.nR = 0
        if self.y > 600 - self.image.get_height():
            self.y = 600 - self.image.get_height()


class Game:
    def __init__(self):
        self.width, self.height = 800, 600
        self.MobileWidth, self.MobileHeight = 320, 200
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.background = pygame.image.load('assets/fondo.jpg').convert()
        self.yBackground = 0
        self.boxes = [Box(self.MobileWidth, self.MobileHeight)
                      for i in range(5)]

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
            self.yBackground += 1
            if self.yBackground >= self.height:
                self.yBackground = 0
            self.screen.blit(self.background, (0, self.yBackground))
            self.screen.blit(
                self.background, (0, self.yBackground - self.height))

            for box in self.boxes:
                box.update()
                self.screen.blit(box.image, (box.x, box.y))

            pygame.display.flip()
            pygame.time.delay(5)  # hay que dejarlo en 20 despues


game = Game()
game.run()
