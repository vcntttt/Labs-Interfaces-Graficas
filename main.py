import pygame
from PIL import Image
import random
import cv2

class Box:
    def __init__(self, width, height, imagenMascara, videoFrame):
        self.width = width
        self.height = height
        self.videoFrame = videoFrame
        self.frameActual = 0
        self.bgImage = Image.open('assets/box.jpg').convert('L')
        self.mask = Image.open(imagenMascara).convert('L')
        self.image = self.initImage(self.videoFrame[self.frameActual])
        self.x = random.randint(0, self.width)
        self.y = random.randint(0, self.height)
        self.dX = 0
        self.dY = 0
        self.nR = 0

    def initImage(self, frame):
        bgResize = self.bgImage.resize(frame.size)
        mascaraResize = self.mask.resize(frame.size)
        rgbFrame = frame.convert("RGB")
        imagenFinal = Image.composite(rgbFrame, bgResize.convert('RGB'), mascaraResize)
        return pygame.image.fromstring(imagenFinal.tobytes(), imagenFinal.size, 'RGB')

    def update(self):
        self.frameActual = (self.frameActual + 1) % len(self.videoFrame)
        self.image = self.initImage(self.videoFrame[self.frameActual])
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
        self.videoFrame = cargaDeFrames('assets/video_03.mp4', (320, 200))
        images = ["assets/planti_01.jpg",
                "assets/planti_02.jpg",
                "assets/planti_03.jpg",
                "assets/planti_04.jpg",
                "assets/planti_05.jpg"]
        self.boxes = [Box(self.MobileWidth, self.MobileHeight, images[i], self.videoFrame)
            for i in range(1,5)]

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
            pygame.time.delay(5)

def cargaDeFrames(rutaVideo, size, frameStep=3):
    cap = cv2.VideoCapture(rutaVideo)
    frames = []
    success, frame = cap.read()
    frameCount = 0
    while success:
        if frameCount % frameStep == 0:
            frame = cv2.resize(frame, size)
            pil_frame = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            frames.append(pil_frame)
        success, frame = cap.read()
        frameCount += 1
    cap.release()
    return frames
    
game = Game()
game.run()
