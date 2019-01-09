# Imports
import pygame
import random

# Initialize game engine
pygame.init()

# Window
WIDTH = 800
HEIGHT = 600
SIZE = (WIDTH, HEIGHT)
TITLE = "Block Life"
screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption(TITLE)

# Timer
clock = pygame.time.Clock()
refresh_rate = 60

# Colors
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# Fonts
my_font = pygame.font.Font(None, 50)
    
# helper functions
def intersects(rect1, rect2):
    left1 = rect1[0]
    right1 = rect1[0] + rect1[2] - 1
    top1 = rect1[1]
    bottom1 = rect1[1] + rect1[3] - 1

    left2 = rect2[0]
    right2 = rect2[0] + rect2[2] - 1
    top2 = rect2[1]
    bottom2 = rect2[1] + rect2[3] - 1

    return not (right1 < left2 or right2 < left1 or
                bottom1 < top2 or bottom2 < top1)

def generate_platform(y):
    opening_size = 200
    w = WIDTH - opening_size
    h = 50

    offset = random.randrange(0, w)

    wall1 = [0, y, w, h]
    wall2 = [w + opening_size, y, w, h]

    wall1[0] -= offset
    wall2[0] -= offset
    
    return wall1, wall2

# Game physics
gravity = 1
terminal_velocity = 6

# Make a duck
duck =  [200, 100, 50, 50]
duck_vx = 0
duck_vy = 0
duck_speed = 6
duck_is_alive = True
score = 0

# make starting walls
platform_gap = 200
walls = []

for i in range(4):
    left, right = generate_platform(i * platform_gap + platform_gap)
    walls.append(left)
    walls.append(right)

wall_speed = 2

# Game loop
done = False

while not done:
    # Event processing (React to key presses, mouse clicks, etc.)
    ''' for now, we'll just check to see if the X is clicked '''
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    state = pygame.key.get_pressed()

    left = state[pygame.K_LEFT]
    right = state[pygame.K_RIGHT]
        
    if left:
        duck_vx = -duck_speed
    elif right:
        duck_vx = duck_speed
    else:
        duck_vx = 0
    
    # Game logic (Check for collisions, update points, etc.)
    ''' check for dead duck '''
    if duck[1] < 0:
        duck_is_alive = False

    if duck_is_alive:
        ''' move walls '''
        to_remove = None
        
        for w in walls:
            w[1] -= wall_speed

            if w[1] + w[3] < 0:
                to_remove = w

        if to_remove != None:
            walls.remove(to_remove)
            y = walls[-1][1] + platform_gap
            left, right = generate_platform(y)
            walls.append(left)
            walls.append(right)
            
        ''' apply gravity to the duck '''
        duck_vy += gravity
        duck_vy = min(duck_vy, terminal_velocity)
        duck[1] += duck_vy
        
        ''' resolve collisions with each wall '''
        for wall in walls:
            if intersects(duck, wall):
                duck_vy = 0
                duck[1] = wall[1] - duck[3]

        ''' move the duck in horizontal direction '''
        duck[0] += duck_vx

        ''' resolve collisions with each wall again '''
        for wall in walls:
            if intersects(duck, wall):
                if duck_vx > 0:
                    duck[0] = wall[0] - duck[2]
                elif duck_vx < 0:
                    duck[0] = wall[0] + wall[2]

        ''' update score '''
        score += 1
        
    # Drawing code (Describe the picture. It isn't actually drawn yet.)
    screen.fill(BLACK)

    pygame.draw.rect(screen, YELLOW, duck)

    for w in walls:
        pygame.draw.rect(screen, WHITE, w)

    score_txt = my_font.render(str(score), 1, RED)
    screen.blit(score_txt, (20, 20))
    
    # Update screen (Actually draw the picture in the window.)
    pygame.display.flip()

    # Limit refresh rate of game loop 
    clock.tick(refresh_rate)

# Close window and quit
pygame.quit()
