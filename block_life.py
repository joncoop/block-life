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
font_sm = pygame.font.Font(None, 40)
font_md = pygame.font.Font(None, 80)
font_lg = pygame.font.Font(None, 100)
font_xl = pygame.font.Font(None, 140)

# Stages
START = 0
PLAYING = 1
END = 2

# Physics
gravity = 1
terminal_velocity = 7

# Helper functions
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

def setup():
    global block, block_vx, block_vy, block_speed, score 
    global platform_gap, walls, wall_speed, stage
           
    ''' Make a block '''
    block =  [375, 25, 50, 50]
    block_vx = 0
    block_vy = 0
    block_speed = 6
    score = 0

    ''' make starting walls '''
    platform_gap = 200
    walls = []

    for i in range(4):
        left, right = generate_platform(i * platform_gap + platform_gap)
        walls.append(left)
        walls.append(right)

    ''' initial wall speed '''
    wall_speed = 2

    ''' set stage '''
    stage = START

def update_platforms():
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
            
def update_block():
    global block, block_vx, block_vy
    
    ''' apply gravity '''
    block_vy += gravity
    block_vy = min(block_vy, terminal_velocity)

    if block[1] < 500:
        block[1] += block_vy
    else:
        for wall in walls:
            wall[1] -= block_vy

    ''' resolve collisions with each wall '''
    for wall in walls:
        if intersects(block, wall):
            block_vy = 0
            block[1] = wall[1] - block[3]

    ''' move the block in horizontal direction '''
    block[0] += block_vx

    ''' resolve collisions with each wall again '''
    for wall in walls:
        if intersects(block, wall):
            if block_vx > 0:
                block[0] = wall[0] - block[2]
            elif block_vx < 0:
                block[0] = wall[0] + wall[2]

    ''' keep block on the screen '''
    if block[0] < 0:
        block[0] = 0
    elif block[0] > WIDTH - block[2]:
        block[0] = WIDTH - block[2]
        
def update_score():
    global score

    score += 1
    
def update_level():
    global wall_speed
    
    if score % 500 == 0:
        wall_speed += .5
            
# Drawing functions
def draw_block():
    pygame.draw.rect(screen, YELLOW, block)

def draw_platforms():
    for w in walls:
        pygame.draw.rect(screen, WHITE, w)
        
def draw_score():
    text = font_md.render(str(score), 1, RED)
    screen.blit(text, (20, 20))
    
def draw_start_screen():
        text = font_xl.render("BLOCK LIFE", 1, RED)
        w = text.get_width()
        screen.blit(text, (WIDTH/2 - w/2, 180))
        
        text = font_sm.render("Press SPACE to start", 1, RED)
        w = text.get_width()
        screen.blit(text, (WIDTH/2 - w/2, 280))
        
def draw_end_screen():
        text = font_lg.render("GAME OVER", 1, RED)
        w = text.get_width()
        screen.blit(text, (WIDTH/2 - w/2, 200))
        
        text = font_sm.render("Press SPACE to play again", 1, RED)
        w = text.get_width()
        screen.blit(text, (WIDTH/2 - w/2, 280))

# Game loop
setup()
done = False

while not done:
    # Event processing (React to key presses, mouse clicks, etc.)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if stage == START:
                    stage = PLAYING
                elif stage == END:
                    setup()

    state = pygame.key.get_pressed()
    
    # Game logic
    if stage == PLAYING:
        ''' block controls '''
        left = state[pygame.K_LEFT]
        right = state[pygame.K_RIGHT]
            
        if left:
            block_vx = -block_speed
        elif right:
            block_vx = block_speed
        else:
            block_vx = 0

        ''' update game '''
        update_platforms()
        update_block()
        update_score()
        update_level()
        
        ''' check for dead block '''
        if block[1] < 0:
            stage = END
            
    # Drawing code
    screen.fill(BLACK)
    draw_block()
    draw_platforms()
    draw_score()

    if stage == START:
        draw_start_screen()
    elif stage == END:
        draw_end_screen()
        
    # Update screen
    pygame.display.flip()

    # Limit refresh rate 
    clock.tick(refresh_rate)

# Close window and quit
pygame.quit()
