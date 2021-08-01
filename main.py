import pygame, random


pygame.init()
pygame.font.init()


size = width, height = (1280, 720)
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Russian Arkanoid')


isStart = False
Attempts = 3
Score = 0
Combo = 1
brickList = ['Red', 'Orange', 'Yellow', 'Green', 'SkyBlue', 'Blue', 'Purple']
clock = pygame.time.Clock()
fps = 30


StrikeSound = pygame.mixer.Sound('data/Sounds/Strike.ogg')
BounceSound = pygame.mixer.Sound('data/Sounds/Bounce.ogg')
DestroySound = pygame.mixer.Sound('data/Sounds/Destroy.ogg')


def imageLoader(name):
    fullname = 'data' + '/' + name
    try:
        if name[-2:] == 'jpg':
            image = pygame.image.load(fullname).convert()
        else:
            image = pygame.image.load(fullname).convert_alpha()
    except:
        print('imagee not founded: ', name)
        raise SystemExit()

    return image


class Background(pygame.sprite.Sprite):
    image = imageLoader('FLAG.jpg')

    def __init__(self, x, y):
        super().__init__(all_sprites)
        self.image = Background.image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Platform(pygame.sprite.Sprite):
    image = imageLoader('Platform.png')

    def __init__(self, x, y):
        super().__init__(all_sprites)
        self.add(P1)
        self.image = Platform.image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vx = 0
        self.vy = 0

    def update(self):
        self.rect = self.rect.move(self.vx, self.vy)


class Brick(pygame.sprite.Sprite):
    image = imageLoader('Bricks/Red.png')
    Orange = imageLoader('Bricks/Orange.png')
    Yellow = imageLoader('Bricks/Yellow.png')
    Green = imageLoader('Bricks/Green.png')
    SkyBlue = imageLoader('Bricks/SkyBlue.png')
    Blue = imageLoader('Bricks/Blue.png')
    Purple = imageLoader('Bricks/Purple.png')



    def __init__(self, x, y):
        super().__init__(all_sprites)
        self.add(Bricks)
        self.strength = 0
        self.image = Brick.image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vx = 0
        self.vy = 0
        self.colorv = random.randint(1, 100)

        if self.colorv >= 1 and self.colorv <= 50:
            self.image = Brick.image
            self.strength = 1
        elif self.colorv > 50 and self.colorv <= 75:
            self.image = Brick.Orange
            self.strength = 2
        elif self.colorv > 75 and self.colorv <= 88:
            self.image = Brick.Yellow
            self.strength = 3
        elif self.colorv > 88 and self.colorv <= 94:
            self.image = Brick.Green
            self.strength = 4
        elif self.colorv > 94 and self.colorv <= 97:
            self.image = Brick.SkyBlue
            self.strength = 5
        elif self.colorv > 97 and self.colorv <= 99:
            self.image = Brick.Blue
            self.strength = 6
        elif self.colorv == 100:
            self.image = Brick.Purple
            self.strength = 7

    def update(self):
        self.rect = self.rect.move(self.vx, self.vy)


        if pygame.sprite.spritecollide(self, BallG, False):
            global Combo
            global Score
            global brickList

            Score += 5 * Combo
            Combo += 1
            StrikeSound.play()

            if self.strength == 1:
                DestroySound.play()
                self.kill()
            else:
                self.strength -= 1
                self.image = imageLoader('Bricks/' + brickList[self.strength - 1] + ".png")


class GreenBall(pygame.sprite.Sprite):
    image = imageLoader('GreenBall.png')

    def __init__(self, x, y):
        super().__init__(all_sprites)
        self.add(BallG)
        self.image = GreenBall.image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vx = 0
        self.vy = 0
        self.rdirb = 0
        self.rdirp = 0

    def update(self):
        self.rect = self.rect.move(self.vx, self.vy)  # Двигаем мячик


        if pygame.sprite.spritecollide(self, Bricks, False):

            StrikeSound.play()

            self.rdirb = random.randint(1, 3)
            if self.rdirb == 1:
                self.vx = self.vx
                self.vy = -self.vy
            elif self.rdirb == 2:
                self.vx = -self.vx
                self.vy = -self.vy
            elif self.rdirb == 3:
                self.vx = -self.vx
                self.vy = self.vy


        if pygame.sprite.spritecollide(self, P1, False):
            global Combo
            BounceSound.play()
            Combo = 1
            self.rdirp = random.randint(1, 2)

            if self.rdirp == 1:
                self.vx = self.vx
                self.vy = -self.vy
            elif self.rdirp == 2:
                self.vx = -self.vx
                self.vy = -self.vy


        if self.rect.y <= 0:
            self.vx = self.vx
            self.vy = -self.vy

        if self.rect.x >= 1250 or self.rect.x <= 0:
            self.vx = -self.vx
            self.vy = self.vy


        if self.rect.y >= 720:
            self.depth()


    def run(self):
        global isStart
        self.vx = -6
        self.vy = -6
        isStart = 1


    def depth(self):
        global isStart
        global Attempts
        global Combo
        if Attempts > 0:
            self.vx = 0
            self.vy = 0
            self.rect.x = 628
            self.rect.y = 550
            Player.rect.x = 540
            isStart = 0
            Attempts -= 1
            Combo = 1
        elif Attempts <= 0:
            self.vx = 0
            self.vy = 0
            self.rect.x = -100
            self.rect.y = -100
            isStart = 2
            Combo = 1


gameFont = pygame.font.SysFont('Verdana', 30)
scoreText = gameFont.render('Счёт: ' + str(Score), True, (255, 0, 0))
comboText = gameFont.render('К-К-КОМБО: ' + str(Combo), True, (255, 255, 255))
attemptsText = gameFont.render('Попытки: ' + str(Attempts), True, (255, 255, 255))


all_sprites = pygame.sprite.Group()
P1 = pygame.sprite.Group()
BallG = pygame.sprite.Group()
Bricks = pygame.sprite.Group()


BackGroundObj = Background(0, 0)
Player = Platform(573, 640)
Ball = GreenBall(628, 550)


brk_x, brk_y = 0, 100
for i in range(9):
    for j in range(20):
        Brick(brk_x, brk_y)

        brk_x += 64
    brk_y += 32
    brk_x -= 20 * 64

playing = True
while playing:

    keys = pygame.key.get_pressed()

    if keys[pygame.K_RIGHT] and isStart == True and Player.rect.x < 1080:
        Player.rect.x += 9
    if keys[pygame.K_LEFT] and isStart == True and Player.rect.x > 0:
        Player.rect.x -= 9

    if len(Bricks) <= 0:
        Ball.vx = 0
        Ball.vy = 0
        isStart = 3

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and isStart == 0 and Attempts > 0:
            Ball.run()

        if event.type == pygame.QUIT:
            playing = False

    screen.fill((0, 0, 0))

    scoreText = gameFont.render('Счёт: ' + str(Score), True, (255, 0, 0))
    comboText = gameFont.render('К-К-КОМБО: ' + str(Combo), True, (255, 255, 255))

    if Attempts > 0:
        attemptsText = gameFont.render('Попытки: ' + str(Attempts), True, (255, 255, 255))
    elif Attempts <= 0:
        attemptsText = gameFont.render('Вы проиграли!', True, (255, 255, 255))
    elif Attempts > 0 and isStart == 3:
        attemptsText = gameFont.render('ПОБЕДА!!!', True, (255, 255, 255))

    for sprite in all_sprites:
        sprite.update()
    all_sprites.draw(screen)
    screen.blit(scoreText, (1050, 20))
    screen.blit(comboText, (20, 660))
    screen.blit(attemptsText, (1020, 660))
    pygame.display.flip()
    pygame.time.delay(20)
    clock.tick(fps)