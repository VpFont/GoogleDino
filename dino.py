from pygame import *
from os import *
import random
import sys

font.init()

#Константи
pathAssets = "Assets"
clock = time.Clock()
windows_width, windows_height = 1100, 600
FPS = 30
RUNNING = [image.load(path.join(pathAssets ,"DinoRun1.png")),
        image.load(path.join(pathAssets, "DinoRun2.png"))]
JUMPING = image.load(path.join(pathAssets, "DinoJump.png"))
DUCKING = [image.load(path.join(pathAssets, "DinoDuck1.png")),
        image.load(path.join(pathAssets, "DinoDuck2.png"))]

SMALL_CACTUS = [image.load(path.join(pathAssets, "SmallCactus1.png")),
                image.load(path.join(pathAssets, "SmallCactus2.png")),
                image.load(path.join(pathAssets, "SmallCactus3.png"))]
LARGE_CACTUS = [image.load(path.join(pathAssets, "LargeCactus1.png")),
                image.load(path.join(pathAssets, "LargeCactus2.png")),
                image.load(path.join(pathAssets, "LargeCactus3.png"))]

BIRD = [image.load(path.join(pathAssets, "Bird1.png")),
        image.load(path.join(pathAssets, "Bird2.png"))]

CLOUD = image.load(path.join(pathAssets, "Cloud.png"))

BG = image.load(path.join(pathAssets, "Track.png"))

windows = display.set_mode((windows_width, windows_height))
display.set_caption("Гугл Динозаврик")

class Dino:
    X_POS = 80
    Y_POS = 310
    Y_POS_DUCK = 340
    JUMP_VEL = 8.5

    def __init__(self):
        self.duck_img = DUCKING
        self.run_img = RUNNING
        self.jump_img = JUMPING

        self.dino_duck = False
        self.dino_run = True
        self.dino_jump = False

        self.step_index = 0
        self.jump_vel = self.JUMP_VEL
        self.image = self.run_img[0]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS

    def update(self, userInput):
        if self.dino_duck:
            self.duck()
        if self.dino_run:
            self.run()
        if self.dino_jump:
            self.jump()

        if self.step_index >= 10:
            self.step_index = 0

        if userInput[K_w] and not self.dino_jump:
            self.dino_duck = False
            self.dino_run = False
            self.dino_jump = True
        elif userInput[K_s] and not self.dino_jump:
            self.dino_duck = True
            self.dino_run = False
            self.dino_jump = False
        elif not (self.dino_jump or userInput[K_s]):
            self.dino_duck = False
            self.dino_run = True
            self.dino_jump = False

    def duck(self):
        self.image = self.duck_img[self.step_index // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS_DUCK
        self.step_index += 1

    def run(self):
        self.image = self.run_img[self.step_index // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS
        self.step_index += 1

    def jump(self):
        self.image = self.jump_img
        if self.dino_jump:
            self.dino_rect.y -= self.jump_vel * 4
            self.jump_vel -= 0.8
        if self.jump_vel < - self.JUMP_VEL:
            self.dino_jump = False
            self.jump_vel = self.JUMP_VEL

    def draw(self, windows):
        windows.blit(self.image, (self.dino_rect.x, self.dino_rect.y))

class Cloud:
    def __init__(self):
        self.x = windows_width + random.randint(800, 1000)
        self.y = random.randint(50, 100)
        self.image = CLOUD
        self.width = self.image.get_width()

    def update(self):
        self.x -= game_speed
        if self.x < -self.width:
            self.x = windows_width + random.randint(1000, 1600)
            self.y = random.randint(50, 100)

    def draw(self, windows):
        windows.blit(self.image, (self.x, self.y))


class Obstacle:
    def __init__(self, image, type):
        self.image = image
        self.type = type
        self.rect = self.image[self.type].get_rect()
        self.rect.x = windows_width

    def update(self):
        self.rect.x -= game_speed
        if self.rect.x < -self.rect.width:
            obstacles.pop()
            del self

    def draw(self, windows):
        windows.blit(self.image[self.type], self.rect)


class SmallCactus(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 325


class LargeCactus(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 300


class Bird(Obstacle):
    def __init__(self, image):
        self.type = 0
        super().__init__(image, self.type)
        self.rect.y = 250
        self.index = 0

    def draw(self, windows):
        if self.index >= 9:
            self.index = 0
        windows.blit(self.image[self.index // 5], self.rect)
        self.index += 1
    

def main():
    global obstacles, game_speed, x_pos_bg, y_pos_bg, points
    font1 = font.Font("freesansbold.ttf", 15)
    clock = time.Clock()
    x_pos_bg = 0
    y_pos_bg = 380
    game_speed = 14
    points = 0
    player = Dino()
    clouds = []
    obstacles = []
    death_count = 0

    for i in range(0, 2):
        clouds.append(Cloud())

    def score():
        global points, game_speed
        points += 1
        if points % 100 == 0:
            game_speed += 1

        text = font1.render("Рахунок: " + str(points), True, (0, 0, 0))
        textRect = text.get_rect()
        textRect.center = (1000, 40)
        windows.blit(text, textRect)

    def background():
        global x_pos_bg, y_pos_bg
        image_width = BG.get_width()
        windows.blit(BG, (x_pos_bg, y_pos_bg))
        windows.blit(BG, (image_width + x_pos_bg, y_pos_bg))
        if x_pos_bg <= -image_width:
            windows.blit(BG, (image_width + x_pos_bg, y_pos_bg))
            x_pos_bg = 0
        x_pos_bg -= game_speed

    gameLoop = True

    while gameLoop:
        for e in event.get():
            if e.type == QUIT:
                gameLoop = False

        windows.fill((255, 255, 255))
        background()
        userInput = key.get_pressed()

        player.update(userInput)
        player.draw(windows)

        if len(obstacles) == 0:
            if random.randint(0, 2) == 0:
                obstacles.append(SmallCactus(SMALL_CACTUS))
            elif random.randint(0, 2) == 1:
                obstacles.append(LargeCactus(LARGE_CACTUS))
            elif random.randint(0, 2) == 2:
                obstacles.append(Bird(BIRD))

        for obstacle in obstacles:
            obstacle.draw(windows)
            obstacle.update()
            if player.dino_rect.colliderect(obstacle.rect):
                time.delay(200)
                death_count += 1
                menu(death_count)

        for cloud in clouds:
            cloud.draw(windows)
            cloud.update()

        score()

        clock.tick(FPS)
        display.update()


def menu(death_count):
    global points
    menuLoop = True
    while menuLoop:
        windows.fill((255, 255, 255))
        font2 = font.Font("freesansbold.ttf", 30)

        if death_count == 0:
            text = font2.render("Натисніть будь-яку кнопку для старту", True, (0, 0, 0))
        elif death_count > 0:
            text = font2.render("Натисніть будь-яку кнопку для рестарту", True, (0, 0, 0))
            score = font2.render("Твій рахунок: " + str(points), True, (0, 0, 0))
            scoreRect = score.get_rect()
            scoreRect.center = (windows_width // 2, windows_height // 2 + 50)
            windows.blit(score, scoreRect)
        textRect = text.get_rect()
        textRect.center = (windows_width // 2, windows_height // 2)
        windows.blit(text, textRect)
        windows.blit(RUNNING[0], (windows_width // 2 - 20, windows_height // 2 - 140))
        display.update()

        for e in event.get():
            if e.type == QUIT:
                menuLoop = False
            if e.type == KEYDOWN:
                main()
    sys.exit()

menu(death_count=0)