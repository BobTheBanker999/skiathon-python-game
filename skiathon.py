
# Import needed modules
import random
from time import sleep
import pygame
from pygame.locals import *
import sys

sleep(2)

# Constants defining screen size
SCREEN_W = 800
SCREEN_H = 600

# Define Fred!!!
class Fred(pygame.sprite.Sprite):
    # Constrouctor (i no i spel that rong)
    def __init__(self):
        super(Fred, self).__init__()
        self.surf = pygame.image.load("./fred/fred_skis.png").convert()
        self.rect = self.surf.get_rect()

    # Move fred based on keypresses
    def update(self, pressed_keys):
        # Move Fred
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -5)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 5)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)
        if pressed_keys[K_0]:
            self.kill()
            print(get_death_message())

        # Keep fred onscreen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_W:
            self.rect.right = SCREEN_W
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > SCREEN_H:
            self.rect.bottom = SCREEN_H


# Define TNT Barrels!
class TntBarrel(pygame.sprite.Sprite):
    def __init__(self):
        super(TntBarrel, self).__init__()
        self.surf = pygame.image.load("./enemy/tnt_barrel.png")

        # Random starting pos
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_W + 20, SCREEN_W + 100),
                random.randint(0, SCREEN_H)
            )
        )

        # Random speed
        self.speed = 7

    # Move TNT barrels
    def update(self):
        self.rect.move_ip(-self.speed, 0)

        # Delete barrels of TNT if off screen
        if self.rect.right < 0:
            self.kill()

# Define Coins!!! YAAYYY MONEYYYYYY
class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super(Coin, self).__init__()
        self.surf = pygame.image.load("./powerups/coin.png")

        # Random starting pos
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_W + 20, SCREEN_W + 100),
                random.randint(0, SCREEN_H)
            )
        )

    # Move the coins to create an 'endless runner' feel
    def update(self):
        self.rect.move_ip(-7, 0)
        if self.rect.right < 0:
            self.kill()

# Define powerups
# Define Coins!!! YAAYYY MONEYYYYYY
class Powerup(pygame.sprite.Sprite):
    def __init__(self):
        super(Powerup, self).__init__()
        self.surf = pygame.image.load("./powerups/powerup.png")

        # Random starting pos
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_W + 20, SCREEN_W + 100),
                random.randint(0, SCREEN_H)
            )
        )

    # Move the coins to create an 'endless runner' feel
    def update(self):
        self.rect.move_ip(-7, 0)
        if self.rect.right < 0:
            self.kill()



# Create function for returning death message
def get_death_message():
    available_messages = ["Fred crashed into a Rock", "Fred did not look where he was skiing", "Fwed cwashed into a Wock", "[ERROR]: Could not locate death message"]
    return str(random.choice(available_messages))  

# Initialize pygame
pygame.init()

# Make some noise
pygame.mixer.init()

# Set up the clock - frame rate and such
clock = pygame.time.Clock()

# Create the screen and set caption to 'Ski -a- Thon'
print("Created screen")
screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
pygame.display.set_caption("Ski -a- Thon!")

# Create custom events for adding a new tnt barrel
ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 200)

# Custom event to add coin
ADDCOIN = pygame.USEREVENT + 2
pygame.time.set_timer(ADDCOIN, 1000)

# Create FRED!! YAYY
fred = Fred()
print("Created Fred")

# Create groups to hold objects/sprites
barrels = pygame.sprite.Group()
coins = pygame.sprite.Group()

all_sprites = pygame.sprite.Group()
all_sprites.add(fred)

# Load assets
fred_death_noise = pygame.mixer.Sound("./fred/fred_dying.wav")
fred_pick_coin_noise = pygame.mixer.Sound("./powerups/coin_picked.wav")

# Background music
pygame.mixer.music.load("./soundfx/music1.mp3")
pygame.mixer.music.play(loops=-1)

# Console message
print("Preparing to run main loop...")

# Boolean to keep game running
running = True

# Distance traveled
distance_t = 0

# Coins collected
coins_c = 0

# Console message
print("Running main loop...")

# IMPORTANT!
# Main loop
try:
    while running:

        # Scan game events
        for event in pygame.event.get():

            # QUIT if user closes the window
            if event.type == QUIT:
                print("Exited... code 0\n\n")
                pygame.quit()
            # Should we add a new tnt barrel?
            elif event.type == ADDENEMY:
                new_enemy = TntBarrel()
                barrels.add(new_enemy)
                all_sprites.add(new_enemy)
            # Should we add a cloud?
            elif event.type == ADDCOIN:
                new_coin = Coin()
                coins.add(new_coin)
                all_sprites.add(new_coin)

        # Get keys pressed
        pressed_keys = pygame.key.get_pressed()
        fred.update(pressed_keys)

        # Update tnt pos
        barrels.update()

        # Update coin pos
        coins.update()

        # Fill the screen with white snow
        screen.fill((212, 238, 255))

        # Check if tnt has collided with the player
        if pygame.sprite.spritecollideany(fred, barrels):
            fred.kill()
            fred_death_noise.play()
            print(get_death_message())

            print("Distance: " + str(distance_t) + " ft")
            print("Hot Chocolate: " + str(coins_c) + " liters\n\n")
            sleep(2)
            pygame.quit()
            print("Exited... code 0\n\n")

        # Check if coin has collided with player. if so, update score and kill coin
        if pygame.sprite.spritecollideany(fred, coins):
            coins_c += 1
            fred_pick_coin_noise.play()
            sleep(0.0001)

        # Runs for all sprites and draws them on the screen
        for entity in all_sprites:

            screen.blit(entity.surf, entity.rect)

        # Update distance
        if fred.alive():
            distance_t += 1


        # Render version number
        font = pygame.font.SysFont(None, 25)
        g_version = font.render("v1.1.0 (First Release)", True, [62, 12, 94])
        screen.blit(g_version, (5, 50))

        # Render distance traveled
        dt_t = font.render("Distance Traveled: " + str(distance_t) + " ft", True, [170, 170, 0])
        screen.blit(dt_t, (5, 75))

        # Render coins collected
        co_c = font.render("Hot Chocolate: " + str(coins_c) + " liters", True, [139,69,19])
        screen.blit(co_c, (5, 100))

        # Render thanks to Beethoven
        t_bt = font.render("Thanks to Beethoven for the music", True, [0, 170, 0])
        screen.blit(t_bt, (5, 558))

        # Render credits
        cjs = font.render("Copyright © 2021 - 2022 ChikenJuice Studios. Do not distribute!", True, [255, 0, 0])
        screen.blit(cjs, (5, 583))

        pygame.display.flip()

        # Frame rate
        clock.tick(30)

except pygame.error:
    pass
