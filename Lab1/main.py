import pygame
from PIL import Image, ImageOps
import random
import cv2

class Box:
    def __init__(self, width, height, plantilla, videoFrame):
        self.width = width
        self.height = height
        self.x = random.randint(0, self.width)
        self.y = random.randint(0, self.height)
        self.dX = self.dY = self.nR = self.frameActual = 0
        self.mask = ImageOps.invert(Image.open(plantilla).convert(
            'L').resize((self.width, self.height)))
        self.videoFrames = videoFrame
        self.surface = pygame.Surface((self.width, self.height))
        self.background = Image.open('assets/box.jpg').convert('L').convert('RGB')

    def updateImg(self):
        videoFrame = self.videoFrames[self.frameActual]

        finalImg = Image.composite(videoFrame, self.background, self.mask)
        mode, size, data = finalImg.mode, finalImg.size, finalImg.tobytes()
        self.image = pygame.image.fromstring(data, size, mode)
        self.surface.blit(self.image, (0, 0))
        self.frameActual = (self.frameActual + 1) % len(self.videoFrames)

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
        if self.x > 800 - self.width:
            self.x = 800 - self.width

        if self.y < 0:
            self.y = 0
            self.nR = 0
        if self.y > 600 - self.height:
            self.y = 600 - self.height

        self.updateImg()


class Game:
    def __init__(self):
        self.width, self.height = 800, 600
        self.MobileWidth, self.MobileHeight = 320, 200
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.background = pygame.image.load('assets/fondo.jpg').convert()
        self.yBackground = 0
        plantillas = ["assets/planti_01.jpg",
                      "assets/planti_02.jpg",
                      "assets/planti_03.jpg",
                      "assets/planti_04.jpg",
                      "assets/planti_05.jpg"]
        self.videoFrames = self.cargaFrame(
            'assets/video_03.mp4', (self.MobileWidth, self.MobileHeight))
        self.boxes = [Box(self.MobileWidth, self.MobileHeight, plantillas[i], self.videoFrames)
                      for i in range(5)]

    def cargaFrame(self, videoPath, size, frameStep=3):
        cap = cv2.VideoCapture(videoPath)
        frames = []
        success, frame = cap.read()
        frameCount = 0
        while success:
            if frameCount % frameStep == 0:
                frame = cv2.resize(frame, size)
                pil_frame = Image.fromarray(
                    cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
                frames.append(pil_frame)
            success, frame = cap.read()
            frameCount += 1
        cap.release()
        return frames

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
            pygame.time.delay(10)

game = Game()
game.run()
