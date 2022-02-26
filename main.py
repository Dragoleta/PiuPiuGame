import pygame
import os
pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hell Yeah!!!!!!!!!")
BORDER = pygame.Rect((WIDTH//2 - 5), 0, 10, HEIGHT)

BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)

FPS = 60
VEL = 5
BULLET_VEL = 10
MAXBULLETS = 3
SPC_WIDTH, SPC_HEIGHT = 55, 40

BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join("assets", 'hit.mp3'))
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join("assets", 'fire.mp3'))

HEALTH_FONT = pygame.font.SysFont('comicsans', 20)
WINNER_FONT = pygame.font.SysFont('comicsans', 50)

YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

YELLOW_SPC_IMAGE = pygame.image.load(
    os.path.join("assets", "spaceship_yellow.png"))
YELLOW_SPC = pygame.transform.rotate(pygame.transform.scale(
    YELLOW_SPC_IMAGE, (SPC_WIDTH, SPC_HEIGHT)), 90)

RED_SPC_IMAGE = pygame.image.load(
    os.path.join("assets", "spaceship_red.png"))
RED_SPC = pygame.transform.rotate(pygame.transform.scale(
    RED_SPC_IMAGE, (SPC_WIDTH, SPC_HEIGHT)), -90)

SPACE = pygame.transform.scale(pygame.image.load(
    os.path.join("assets", 'space.png')), (WIDTH, HEIGHT))


def drawWindow(red, yellow, redBullets, yellowBullets, redHp, yellowHp):
    WIN.blit(SPACE, (0, 0))
    pygame.draw.rect(WIN, BLACK, BORDER)

    redHpText = HEALTH_FONT.render("Health: " + str(redHp), 1, WHITE)
    yellowHpText = HEALTH_FONT.render("Health: " + str(yellowHp), 1, WHITE)
    WIN.blit(redHpText, (WIDTH - redHpText.get_width() - 10, 10))
    WIN.blit(yellowHpText, (10, 10))

    WIN.blit(YELLOW_SPC, (yellow.x, yellow.y))
    WIN.blit(RED_SPC, (red.x, red.y))

    for bullet in redBullets:
        pygame.draw.rect(WIN, RED, bullet)
    for bullet in yellowBullets:
        pygame.draw.rect(WIN, YELLOW, bullet)
    pygame.display.update()


def yellowMoveHandler(keys_pressed, yellow):
    if keys_pressed[pygame.K_a] and yellow.x - VEL > 0:  # left
        yellow.x -= VEL
    if keys_pressed[pygame.K_d] and yellow.x + VEL + yellow.width < BORDER.x:  # right
        yellow.x += VEL
    if keys_pressed[pygame.K_w] and yellow.y - VEL > 0:  # up
        yellow.y -= VEL
    if keys_pressed[pygame.K_s] and yellow.y + VEL + yellow.height < HEIGHT:  # down
        yellow.y += VEL


def redMoveHandler(keys_pressed, red):
    if keys_pressed[pygame.K_LEFT] and red.x - VEL > BORDER.width + BORDER.x:  # left
        red.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and red.x + VEL < WIDTH - red.width:  # right
        red.x += VEL
    if keys_pressed[pygame.K_UP] and red.y - VEL > 0:  # up
        red.y -= VEL
    if keys_pressed[pygame.K_DOWN] and red.y + VEL + red.height < HEIGHT:  # down
        red.y += VEL


def bulletHandler(yellowBullets, redBullets, yellow, red):
    for bullet in yellowBullets:
        bullet.x += BULLET_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellowBullets.remove(bullet)
        elif bullet.x > WIDTH:
            yellowBullets.remove(bullet)

    for bullet in redBullets:
        bullet.x -= BULLET_VEL
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            redBullets.remove(bullet)
        elif bullet.x < 0:
            redBullets.remove(bullet)


def drawWinner(text):
    text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(text, (WIDTH/2 - text.get_width() /
             2, HEIGHT/2 - text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000)


def main():
    red = pygame.Rect(700, 300, SPC_WIDTH, SPC_HEIGHT)
    yellow = pygame.Rect(100, 300, SPC_WIDTH, SPC_HEIGHT)
    redBullets = []
    yellowBullets = []
    redHp, yellowHp = 10, 10
    clock = pygame.time.Clock()
    run = True

    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN and len(yellowBullets) < MAXBULLETS:
                if event.key == pygame.K_LCTRL:
                    bullet = pygame.Rect(
                        yellow.x + yellow.width, yellow.y + yellow.height//2 - 2, 10, 5)
                    yellowBullets.append(bullet)
                    BULLET_FIRE_SOUND.play()
                if event.key == pygame.K_RCTRL and len(redBullets) < MAXBULLETS:
                    bullet = pygame.Rect(
                        red.x, red.y + red.height//2 - 2, 10, 5)
                    redBullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

            if event.type == RED_HIT:
                redHp -= 1
                BULLET_HIT_SOUND.play()
            if event.type == YELLOW_HIT:
                yellowHp -= 1
                BULLET_HIT_SOUND.play()

        winnerText = ""

        if redHp <= 0:
            winnerText = "Yellow Wins!"

        if yellowHp <= 0:
            winnerText = "Red Wins!"

        if winnerText != "":
            drawWinner(winnerText)
            break

        keys_pressed = pygame.key.get_pressed()
        yellowMoveHandler(keys_pressed, yellow)
        redMoveHandler(keys_pressed, red)
        bulletHandler(yellowBullets, redBullets, yellow, red)
        drawWindow(red, yellow, redBullets, yellowBullets, redHp, yellowHp)

    main()


if __name__ == '__main__':
    main()
