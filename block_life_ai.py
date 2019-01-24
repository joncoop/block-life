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
YELLOW = (255, 205, 1)
WHITE = (255, 255, 255)
BROWN = (100, 75, 55)
SKY_BLUE = (135, 206, 235)

# Sounds
start_theme = None
main_theme = "sounds/theme.ogg"
end_theme = None

coin_sound = pygame.mixer.Sound("sounds/coin.ogg")

# Fonts
font_xs = pygame.font.Font(None, 40)
font_sm = pygame.font.Font(None, 48)
font_md = pygame.font.Font(None, 64)
font_lg = pygame.font.Font(None, 96)
font_xl = pygame.font.Font("fonts/LuckiestGuy.ttf", 112)

# Images
''' platforms '''
mud_left = pygame.image.load("images/mud_left.png").convert_alpha()
mud_middle = pygame.image.load("images/mud_middle.png").convert_alpha()
mud_right = pygame.image.load("images/mud_right.png").convert_alpha()

platform_surf = pygame.Surface([600, 48], pygame.SRCALPHA, 32)
platform_surf.blit(mud_left, [0, 0])
for i in range(48, 600-48, 48):
    platform_surf.blit(mud_middle, [i, 0])
platform_surf.blit(mud_right, [600-48, 0])

''' stars '''
star = pygame.image.load("images/star.png").convert_alpha()
star_sm = pygame.image.load("images/star_sm.png").convert_alpha()

''' block '''
happy = pygame.image.load("images/happy.png").convert_alpha()
scared = pygame.image.load("images/scared.png").convert_alpha()
falling = pygame.image.load("images/falling.png").convert_alpha()
dead = pygame.image.load("images/dead.png").convert_alpha()

''' background '''
rocks = pygame.image.load("images/rocks.png").convert_alpha()
bg_surf = pygame.Surface([WIDTH, HEIGHT + 600], pygame.SRCALPHA, 32)
bg_surf.fill(SKY_BLUE)
for x in range(0, WIDTH, 200):
    for y in range(400, HEIGHT + 600, 200):
        bg_surf.blit(rocks, [x, y])

''' window icon '''
icon = pygame.image.load("images/icon.png").convert_alpha()
pygame.display.set_icon(icon)

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

    if random.randrange(0, 2) == 0:
        x = random.randrange(50, WIDTH - 50)
        y = y - 48
        coin = [x, y, 36, 36]
    else:
        coin = None
        
    return wall1, wall2, coin

def set_music(track):
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.fadeout(2500)

    if track != None:  
        pygame.mixer.music.load(track)
        pygame.mixer.music.play(-1)
    
def setup():
    global block, block_vx, block_vy, block_speed, face
    global platform_gap, walls, wall_speed, stage
    global ticks, score, coins, collected_coins
    global bg_y, scroll_speed
           
    ''' Make a block '''
    block =  [376, 72, 48, 48]
    block_vx = 0
    block_vy = 0
    block_speed = 6
    face = happy
    
    ''' scoring '''
    ticks = 0
    score = 0
    collected_coins = 0

    ''' make starting walls '''
    platform_gap = 200
    walls = []
    coins = []
    
    for i in range(5):
        left, right, coin = generate_platform(i * platform_gap + 2 * platform_gap)
        walls.append(left)
        walls.append(right)

        if coin != None:
            coins.append(coin)

    ''' background scroll position '''
    bg_y = 0
    scroll_speed = 0
    
    ''' initial wall speed '''
    wall_speed = 2

    ''' set stage '''
    stage = START

    ''' music '''
    set_music(start_theme)

def update_platforms():
    global walls, coins
    
    to_remove = []
    
    for wall in walls:
        wall[1] -= wall_speed

        if wall[1] + wall[3] < 0:
            to_remove.append(wall)

    if len(to_remove) > 0:
        walls = [wall for wall in walls if wall not in to_remove]
        
        y = walls[-1][1] + platform_gap
        left, right, coin = generate_platform(y)
        walls.append(left)
        walls.append(right)
        
        if coin != None:
            coins.append(coin)
            
def update_coins():
    global score
    
    to_remove = None
    
    for coin in coins:
        coin[1] -= wall_speed

        if coin[1] + coin[3] < 0:
            to_remove = coin

    if to_remove != None:
        coins.remove(to_remove)

def update_block():
    global block, block_vx, block_vy, block_speed, face
    global score, collected_coins
    global message, message_timer
    global bg_y
    
    ''' apply gravity '''
    block_vy += gravity
    block_vy = min(block_vy, terminal_velocity)

    if block[1] < 500:
        block[1] += block_vy
    else:
        for obj in (walls + coins):
            obj[1] -= block_vy

        bg_y -= block_vy

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

    ''' block wraps around screen '''
    if block[0] < 0 - block[2]:
        block[0] = WIDTH - block[2]
    elif block[0] > WIDTH:
        block[0] = 0 - block[2]

    ''' collect coins '''
    hit_list = [coin for coin in coins if intersects(block, coin)]
            
    for hit in hit_list:
        coin_sound.play()
        coins.remove(hit)
        collected_coins += 1
        score += 100

        if collected_coins == 15:
            block_speed += 2
            message = "Speed Bonus!"
            message_timer = 2 * refresh_rate
            
    ''' update face '''
    if block_vy > 3:
        face = falling
    elif block[1] < 150:
        face = scared
    else:
        face = happy

    
def update_score():
    global score

    score += 1
    
def update_level():
    global wall_speed
    
    if ticks % 100 == 0:
        wall_speed += .08

def update_bg():
    global bg_y, scroll_speed

    if bg_y > -400:
        scroll_speed = wall_speed
    else:
        scroll_speed = 5 * wall_speed // 6
        
    bg_y -= scroll_speed

    if bg_y < -600:
        bg_y = -400

# AI
def get_move_direction():
    next_wall = None
    for wall in walls:
        if wall[1] >= block[1] + block[3]:
            gap = wall[0] + wall[2] + 100
            next_wall = wall
            break

    block_center = block[0] + block[2] / 2
    block_top = block[1]

    if block_center > gap:
        left_dist = block_center - gap
    else:
        left_dist = block_center + (WIDTH - gap)

    if block_center < gap:
        right_dist = gap - block_center
    else:
        right_dist = (WIDTH - block_center) + gap

    coin_center = None
    for coin in coins:
        if 0 < next_wall[1] - coin[1] < 150:
            coin_center = coin[0] + coin[2] / 2
    
    if coin_center != None:
        risk_limit = block_top - 3000 / wall_speed
        
        if abs(left_dist - right_dist) < risk_limit:
            if coin_center < block_center:
                return -1
            else:
                return 1

    if abs(block_center - gap) < 10:
        return 0
    elif left_dist < right_dist:
        return -1
    else:
        return 1
    
# Drawing functions
def draw_background():
    screen.blit(bg_surf, [0, bg_y])
    
def draw_block():
    screen.blit(face, [block[0], block[1]])
    
def draw_platforms():
    for wall in walls:
        screen.blit(platform_surf, [wall[0], wall[1]])

def draw_coins():
    for coin in coins:
        screen.blit(star, [coin[0], coin[1]])
        
def draw_score():
    text = font_md.render(str(score), 1, WHITE)
    screen.blit(text, [16, 16])
    
    text = font_xs.render(str(collected_coins), 1, YELLOW)
    w = text.get_width()
    screen.blit(text, [WIDTH - w - 16, 20])

    screen.blit(star_sm, [WIDTH - w - 48, 20])
    
def draw_start_screen():
        text = font_xl.render("BLOCK LIFE", 1, BROWN)
        w = text.get_width()
        screen.blit(text, [WIDTH/2 - w/2, 180])
        
        text = font_xs.render("Press SPACE to start", 1, WHITE)
        w = text.get_width()
        screen.blit(text, [WIDTH/2 - w/2, 290])
        
def draw_end_screen():
        text = font_lg.render("GAME OVER", 1, WHITE)
        w = text.get_width()
        screen.blit(text, [WIDTH/2 - w/2, 210])
        
        text = font_xs.render("Press SPACE to play again", 1, WHITE)
        w = text.get_width()
        screen.blit(text, [WIDTH/2 - w/2, 280])

def draw_message(message):
        text = font_md.render(message, 1, WHITE)
        w = text.get_width()
        screen.blit(text, (WIDTH/2 - w/2, 200))

# Game loop
setup()
done = False
message_timer = 0

while not done:
    # Event processing (React to key presses, mouse clicks, etc.)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if stage == START:
                    set_music(main_theme)
                    stage = PLAYING
                elif stage == END:
                    setup()

    state = pygame.key.get_pressed()
    
    # Game logic
    if stage == PLAYING:
        direction = get_move_direction()
        
        ''' block controls '''
        left = direction == -1
        right = direction == 1
            
        if left:
            block_vx = -block_speed
        elif right:
            block_vx = block_speed
        else:
            block_vx = 0

        ''' update game '''
        update_platforms()
        update_coins()
        update_block()
        update_score()
        update_level()
        update_bg()
        
        ''' check for dead block '''
        if block[1] < 0:
            stage = END
            face = dead
            set_music(end_theme)
            
        ''' messages '''
        if message_timer > 0:
            message_timer -= 1

        ''' count ticks '''
        ticks += 1

    # Drawing code
    draw_background()
    draw_block()
    draw_platforms()
    draw_coins()
    draw_score()

    if stage == START:
        draw_start_screen()
    elif stage == END:
        draw_end_screen()
    elif message_timer > 0:
        draw_message(message)
        
    # Update screen
    pygame.display.flip()

    # Limit refresh rate 
    clock.tick(refresh_rate)

# Close window and quit
pygame.quit()
