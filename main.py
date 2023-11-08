import pygame
import random
import time

pygame.font.init()

WIDTH, HEIGHT = 1000, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Lulu's Space Adventure")

BG = pygame.transform.scale(pygame.image.load('space-bg.jpg'), (WIDTH, HEIGHT))

PLAYER_WIDTH, PLAYER_HEIGHT = 50, 75
PLAYER_VELOCITY = 5

FONT = pygame.font.SysFont('comicsans', 30)

STAR_WIDTH = 10
STAR_HEIGHT = 20
STAR_VELOCITY = 5
hit = False

def draw(player, elapsed_time, stars):
    WIN.blit(BG, (0, 0))

    time_text = FONT.render(f"Time: {round(elapsed_time)}s", 1, (255, 255, 255))

    WIN.blit(time_text, (WIDTH - time_text.get_width() - 10, 10))

    pygame.draw.rect(WIN, "red", player)

    for star in stars:
        pygame.draw.rect(WIN, "yellow", star)

    pygame.display.update()

def main():
    run = True
    FPS = 120
    clock = pygame.time.Clock()
    global hit

    start_time = time.time()
    elapsed_time = 0

    player = pygame.Rect(100, HEIGHT - PLAYER_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT)

    star_add_interval = 2000
    star_count = 0

    stars = []

    while run:
        star_count += clock.tick(FPS)
        elapsed_time = time.time() - start_time

        if star_count > star_add_interval:
            for _ in range(3):
                star_x = random.randint(0, WIDTH - STAR_WIDTH)
                star = pygame.Rect(star_x, -STAR_HEIGHT, STAR_WIDTH, STAR_HEIGHT)
                stars.append(star)

            star_add_interval = max(200, star_add_interval - 50)
            star_count = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.K_ESCAPE:
                run = False
                break
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x - PLAYER_VELOCITY >= 0:
            player.x -= PLAYER_VELOCITY
        if keys[pygame.K_RIGHT] and player.x + PLAYER_VELOCITY + PLAYER_WIDTH <= WIDTH:
            player.x += PLAYER_VELOCITY

        for star in stars[:]:
            star.y += STAR_VELOCITY

            if star.y + star.height >= player.y and star.colliderect(player):
                hit = True

            if star.y > HEIGHT:
                stars.remove(star)

        if hit:
            lost_text = FONT.render("You Lost!", 1, (255, 255, 255))
            WIN.blit(lost_text, (WIDTH/2 - lost_text.get_width()/2, HEIGHT/2 - lost_text.get_height()/2))
            pygame.display.update()
            pygame.time.delay(4000)
            break

        draw(player, elapsed_time, stars)

    pygame.quit()


if __name__ == "__main__":
    main()