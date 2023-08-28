import pygame
import os
pygame.font.init()
pygame.mixer.init()

screen_width = 1080
screen_height = 720
spaceship_width = 75
spaceship_height = 65
FPS = 60
vel = 5
bullet_vel = 10
border = pygame.Rect(533, 0, 14, 720)
white = (255, 255, 255)
black = (0, 0, 0)

bullet_hit = pygame.mixer.Sound(os.path.join("Assets", "Grenade+1.mp3"))
bullet_shot = pygame.mixer.Sound(os.path.join("Assets", "Gun+Silencer.mp3"))

health_font = pygame.font.SysFont("comicsans", 40)
winner_font = pygame.font.SysFont("comicsans", 100)

yellow_hit = pygame.USEREVENT + 1
red_hit = pygame.USEREVENT + 2


win = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Improved Game")
red_spaceship_img = pygame.image.load(os.path.join("Assets", "spaceship_red.png")).convert_alpha()
yellow_spaceship_img = pygame.image.load(os.path.join("Assets", "spaceship_yellow.png")).convert_alpha()
yellow_spaceship = pygame.transform.rotate(pygame.transform.scale(yellow_spaceship_img, (spaceship_width, spaceship_height)), 90)
red_spaceship = pygame.transform.rotate(pygame.transform.scale(red_spaceship_img, (spaceship_width, spaceship_height)), 270)
red_ship = pygame.Rect(900, 300, spaceship_width, spaceship_height)
yellow_ship = pygame.Rect(100, 300, spaceship_width, spaceship_height)
space = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "space.png")), (screen_width, screen_height)).convert()



max_bullets = 3
yellow_bullets = []
red_bullets = []

def draw_winner(text):
    draw_text = winner_font.render(text, 1, (250, 250, 250))
    win.blit(draw_text, (540 - draw_text.get_width()/2, 360 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000)


def bullet_pew(yellow_bullets, red_bullets, yellow_spaceship, red_spaceship):

    for bullet in yellow_bullets:
        bullet.x += bullet_vel
        if red_ship.colliderect(bullet):
            pygame.event.post(pygame.event.Event(red_hit))
            yellow_bullets.remove(bullet)
            bullet_hit.play()
        elif bullet.x > 1080:
            yellow_bullets.remove(bullet)

    for bullet in red_bullets:
        bullet.x -= bullet_vel
        if yellow_ship.colliderect(bullet):
            pygame.event.post(pygame.event.Event(yellow_hit))
            red_bullets.remove(bullet)
            bullet_hit.play()
        elif bullet.x < 0:
            red_bullets.remove(bullet)


def drawing(red_spaceship, yellow_spaceship, red_bullets, yellow_bullets, red_health, yellow_health):
    win.blit(space, (0, 0))
    pygame.draw.rect(win, black, border)

    red_health_text = health_font.render("Health " + str(red_health), 1, (250, 250, 250))
    yellow_health_text = health_font.render("Health " + str(yellow_health), 1, (250, 250, 250))
    win.blit(red_health_text, (890, 10))
    win.blit(yellow_health_text, (10, 10))

    win.blit(yellow_spaceship, (yellow_ship.x, yellow_ship.y))
    win.blit(red_spaceship, (red_ship.x, red_ship.y))

    for bullet in yellow_bullets:
        pygame.draw.rect(win, (255, 255, 0), bullet)
    for bullet in red_bullets:
        pygame.draw.rect(win, (255, 0, 0), bullet)

    pygame.display.update()

def main_game():
    clock = pygame.time.Clock()

    red_health = 5
    yellow_health = 5

    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(yellow_bullets) < max_bullets:
                    bullet = pygame.Rect(yellow_ship.x + spaceship_width, yellow_ship.y + spaceship_height // 2 - 2, 10,5)
                    yellow_bullets.append(bullet)
                    bullet_shot.play()

            if event.type == pygame.KEYDOWN and len(red_bullets) < max_bullets:
                if event.key == pygame.K_RCTRL:
                    bullet = pygame.Rect(red_ship.x, red_ship.y + spaceship_height // 2 - 2, 10, 5)
                    red_bullets.append(bullet)
                    bullet_shot.play()

            if event.type == red_hit:
                red_health -= 1

            if event.type == yellow_hit:
                yellow_health -= 1


        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_a] and yellow_ship.x > 0:
            yellow_ship.x -= vel
        if keys_pressed[pygame.K_d] and yellow_ship.x < 450:
            yellow_ship.x += vel
        if keys_pressed[pygame.K_w] and yellow_ship.y > 0:
            yellow_ship.y -= vel
        if keys_pressed[pygame.K_s] and yellow_ship.y < 650:
            yellow_ship.y += vel
        if keys_pressed[pygame.K_LEFT] and red_ship.x > 570:
            red_ship.x -= vel
        if keys_pressed[pygame.K_RIGHT] and red_ship.x < 1010:
            red_ship.x += vel
        if keys_pressed[pygame.K_UP] and red_ship.y > 0:
            red_ship.y -= vel
        if keys_pressed[pygame.K_DOWN] and red_ship.y < 650:
            red_ship.y += vel


        winner_text = ""
        if red_health <= 0:
            winner_text = "Yellow wins!"
        if yellow_health <= 0:
            winner_text = "Red wins"
        if winner_text != "":
            draw_winner(winner_text) #someone won
            break

        bullet_pew(yellow_bullets, red_bullets, yellow_spaceship, red_spaceship)
        drawing(red_spaceship, yellow_spaceship, red_bullets, yellow_bullets, red_health, yellow_health)

    main_game()




if __name__ == "__main__":
    main_game()


