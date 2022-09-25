# Import the pygame module
import pygame

# Import pygame.locals for easier access to key coordinates
# Updated to conform to flake8 and black standards
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

# Define constants for the screen width and height
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600

class Ball(pygame.sprite.Sprite):
    
    def __init__(self):
        super(Ball, self).__init__()
        self.surf = pygame.Surface((5, 5))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect(center = (30, SCREEN_HEIGHT/2))
        self.speedX = 10
        self.speedY = 10
    
    # Move the sprite
    def update(self):
        if self.rect.left < 0 or self.rect.right > SCREEN_WIDTH: 
            self.speedX = -self.speedX
        if pygame.sprite.spritecollide(ball, all_players, False):
            self.speedY = -self.speedY
        
        if self.rect.top < 0:
            self.rect.center = (30, SCREEN_HEIGHT/2)
            player2.points+=1
        
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.center = (30, SCREEN_HEIGHT/2)
            player1.points+=1

        self.rect.move_ip(self.speedX,self.speedY)
        

# Define a player object by extending pygame.sprite.Sprite
# The surface drawn on the screen is now an attribute of 'player'
class Player(pygame.sprite.Sprite):
    
    def __init__(self, xPos):
        super(Player, self).__init__()
        self.surf = pygame.Surface((75, 10))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect(center = (SCREEN_WIDTH/2, xPos))
        self.points = 0
        self.xPos = xPos

    # Move the sprite based on user keypresses
    def update(self, pressed_keys, player, leftKey, rightKey):
        if pressed_keys[leftKey]:
            self.rect.move_ip(-5, 0)
        if pressed_keys[rightKey]:
            self.rect.move_ip(5, 0)

        if numJoysticks > 2:
            axis1 = 0
            if player == 1:
                axis1 = joysticks[1]
            elif player == 2:
                axis1 = joysticks[2]
            if axis1 >= .8:
                self.rect.move_ip(-5, 0)
            if axis1 <- -.8:
                self.rect.move_ip(5, 0)

        # Keep player on the screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        
        # font.render_to(screen, (40, self.xPos), str(self.points), (255, 255, 255))
        text_surf = font.render(str(self.points), True, (255,255,255))
        text_rect = text_surf.get_rect(center=(40, self.xPos))
        screen.blit(text_surf, text_rect)   

# Initialize pygame
pygame.init()
pygame.font.init()

# look for joysticks
numJoysticks = pygame.joystick.get_count()
print("Detected num Joysticks: ", numJoysticks)
useJoysticks = numJoysticks != 0

# init all the joysticks we have
joysticks = []
for i in range(numJoysticks):
    j = pygame.joystick.Joystick(i)
    j.init()
    joysticks.append(j)

# Joystick constants
# north button goes forward

JOY_BTN_NORTH = 3     
JOY_BTN_SOUTH = 6    
JOY_BTN_EAST = 5     
JOY_BTN_WEST = 2    
JOY_BTN_CENTER = 4
JOY_BTN_COIN = 0
JOY_BTN_PLAYER = 1

# Create the screen object
# The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Instantiate player. Right now, this is just a rectangle.
player1 = Player(25)
player2 = Player(SCREEN_HEIGHT-25)
ball = Ball()

all_players = pygame.sprite.Group()
all_players.add(player1)
all_players.add(player2)

all_sprites = pygame.sprite.Group()
all_sprites.add(all_players)
all_sprites.add(ball)


# Variable to keep the main loop running
running = True

# Setup the clock for a decent framerate
clock = pygame.time.Clock()

#init font
font = pygame.font.SysFont(None, 25)

# Main loop
while running:
    # for loop through the event queue
    for event in pygame.event.get():
        # Check for KEYDOWN event
        if event.type == KEYDOWN:
            # If the Esc key is pressed, then exit the main loop
            if event.key == K_ESCAPE:
                running = False
        # Check for QUIT event. If QUIT, then set running to false.
        elif event.type == QUIT:
            running = False

    # Get all the keys currently pressed
    pressed_keys = pygame.key.get_pressed()

    # Fill the screen with black
    screen.fill((0, 0, 0))

    # Update the player sprite based on user keypresses
    player1.update(pressed_keys, 1, K_LEFT, K_RIGHT)  
    player2.update(pressed_keys, 2, pygame.K_z, pygame.K_x)

    ball.update()

    # Draw all sprites
    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)

    # Update the display
    pygame.display.flip()

    #maintain framerate
    clock.tick(30)