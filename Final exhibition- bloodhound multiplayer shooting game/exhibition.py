# Import modules-
import pygame
pygame.font.init()
from pygame import mixer
mixer.init()
import os

# Global variables for the game-
WIDTH, HEIGHT = 900, 500
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
# The border-(This is the boundary which limits the movement of the police and the thief.)
BORDER = pygame.Rect(WIDTH//2 - 5, 0, 10, HEIGHT)


# The basic control guide-
print("The controls:\nTHE POLICE: Press the LEFT ALT KEY tO fire a bullet.\nThe thief: Press the RIGHT ALT KEY to fire a bullet. ")

# Screen-
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))

# Caption-
pygame.display.set_caption("BLOODHOUND") 

# Font setting-
energy_font = pygame.font.SysFont('helvetica', 30)
result_font = pygame.font.SysFont('helvetica', 50)

# Frames per second-
FPS = 100

# Movement-
VEL = 10
BULLET_VEL = 7
MAX_BULLETS = 3
thief_width, thief_height = 112, 155
police_width, police_height = 157, 191
thief_HIT = pygame.USEREVENT + 1
police_HIT = pygame.USEREVENT + 2

# The background-
background = pygame.transform.scale(pygame.image.load(
    os.path.join("Images, sounds", "background.png"))

# The thief-
thief_image = pygame.image.load(
    os.path.join("Thief.png", "thief.png"))
the_thief = pygame.transform.rotate(pygame.transform.scale(
    thief_image, (thief_width, thief_height)), 360)

# The police-
police_image = pygame.image.load(
    os.path.join("Images, sounds", "police.png"))
the_police = pygame.transform.rotate(pygame.transform.scale(
    police_image, (police_width, police_height)), 360)

# Sound effects-
def bullet_sound():
    pygame.mixer.music.load(
        os.path.join("Images, sounds", "Gun+Silencer.mp3"))
    pygame.mixer.music.play(0)

def winning_sound():
    pygame.mixer.music.load(os.path.join("Images, sounds", "Winning sound.mp3"))
    pygame.mixer.music.play(0)

def start_sound():
    pygame.mixer.music.load(os.path.join("Images, sounds", "startsound.mp3"))
    pygame.mixer.music.play(0)

# Function which controls the everything that has to be displayed on the screen. 
def display_on_screen(thiefD, policeD, thief_bullets, police_bullets, thief_health, police_health):
    SCREEN.blit(background, (0, 0))
    pygame.draw.rect(SCREEN, BLACK, BORDER)

    thief_health_text = energy_font.render(
        "BLOOD: " + str(thief_health), 1, RED)
    police_health_text = energy_font.render(
        "BLOOD: " + str(police_health), 1, RED)
    SCREEN.blit(thief_health_text, (WIDTH - thief_health_text.get_width() - 10, 10))
    SCREEN.blit(police_health_text, (10, 10))

    SCREEN.blit(the_police, (policeD.x, policeD.y))
    SCREEN.blit(the_thief, (thiefD.x, thiefD.y))

    for bullet in thief_bullets:
        pygame.draw.rect(SCREEN, RED, bullet)

    for bullet in police_bullets:
        pygame.draw.rect(SCREEN, YELLOW, bullet)

    pygame.display.update()


# Police movement-
def police_handle_movement(keys_pressed, policeD):
    if keys_pressed[pygame.K_a] and policeD.x - VEL > 0:  # LEFT
        policeD.x -= VEL
    if keys_pressed[pygame.K_d] and policeD.x + VEL + policeD.width < BORDER.x:  # RIGHT
        policeD.x += VEL
    if keys_pressed[pygame.K_w] and policeD.y - VEL > 0:  # UP
        policeD.y -= VEL
    if keys_pressed[pygame.K_s] and policeD.y + VEL + policeD.height < HEIGHT - 15:  # DOWN
        policeD.y += VEL

# Thief movement-
def movement_of_thief(keys_pressed, thiefD):
    if keys_pressed[pygame.K_LEFT] and thiefD.x - VEL > BORDER.x + BORDER.width:  # LEFT
        thiefD.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and thiefD.x + VEL + thiefD.width < WIDTH:  # RIGHT
        thiefD.x += VEL
    if keys_pressed[pygame.K_UP] and thiefD.y - VEL > 0:  
        thiefD.y -= VEL
    if keys_pressed[pygame.K_DOWN] and thiefD.y + VEL + thiefD.height < HEIGHT - 15:  # DOWN
        thiefD.y += VEL

# The bullets-
def handle_bullets(police_bullets, thief_bullets, policeD, thiefD):
    for bullet in police_bullets:
        bullet.x += BULLET_VEL
        if thiefD.colliderect(bullet):
            pygame.event.post(pygame.event.Event(thief_HIT))
            police_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            police_bullets.remove(bullet)

    for bullet in thief_bullets:
        bullet.x -= BULLET_VEL
        if policeD.colliderect(bullet):
            pygame.event.post(pygame.event.Event(police_HIT))
            thief_bullets.remove(bullet)
        elif bullet.x < 0:
            thief_bullets.remove(bullet)

# The winner-
def winner_display(text):
    draw_text = result_font.render(text, 1, RED)
    SCREEN.blit(draw_text, (WIDTH/2 - draw_text.get_width() /
                         2, HEIGHT/2 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000)

# The main game loop-
def main():
    thiefD = pygame.Rect(700, 320, thief_width, thief_height)
    policeD = pygame.Rect(100, 290, police_width, police_height)

    thief_bullets = []
    police_bullets = []

    global thief_health, police_health
    thief_health = 10
    police_health = 10
    

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LALT and len(police_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(
                        policeD.x + policeD.width, policeD.y + policeD.height//3.9 - 2, 10, 5)
                    police_bullets.append(bullet)
                    bullet_sound()
                    

                if event.key == pygame.K_RALT and len(thief_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(
                        thiefD.x, thiefD.y + thiefD.height//8.5 - 2, 10, 5)
                    thief_bullets.append(bullet)
                    bullet_sound()
                    

            if event.type == thief_HIT:
                thief_health -= 1
                

            if event.type == police_HIT:
                police_health -= 1
                

        winner_text = ""
        if thief_health <= 0:
            winning_sound()
            winner_text = "CRIMINAL KILLED"

        if police_health <= 0:
            winning_sound()
            winner_text = "COP MARTYRED"

        if winner_text != "":
            winner_display(winner_text)
            break

        keys_pressed = pygame.key.get_pressed()
        police_handle_movement(keys_pressed, policeD)
        movement_of_thief(keys_pressed, thiefD)

        handle_bullets(police_bullets, thief_bullets, policeD, thiefD)

        display_on_screen(thiefD, policeD, thief_bullets, police_bullets,
                    thief_health, police_health)

    main()


if __name__ == "__main__":
    start_sound()
    main()