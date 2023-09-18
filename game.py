# Eduardo Cisneros vka2jm

"""
--- 2D Boxing ---

Goal of the game is to try and beat your opponent in a boxing match
If you can get your opponent's health bar to completely disappear by damaging them, you win!
Otherwise, the game will be decided by which opponent did the most damage when the timer has hit 0

Features
User Input: Users can control the two boxers on the screen using the controls below
Game Over: Game will end once the timer runs out or if a boxer is defeated
Graphics/Images: The boxing ring background is a local image

Sprite Animations: Sprite was used for boxers
Restart from Game Over: Users are given the option to click the space bar and restart once the game is over
Timer: Timer at the top of the screen that ends game if it is at 0
Health Bar: Displays how much health each boxer has
Two players simultaneously: Both boxers are controlled by users and are fighting eachother

Controls
a/left arrow: move left
d/right arrow: move right
w/up arrow: punch
s/down arrow: block
"""

import uvage

screen_width = 800
screen_height = 600
camera = uvage.Camera(screen_width, screen_height)

# loading spritesheet
boxer_sprite = "SPRITE.png"
boxer_movements = uvage.load_sprite_sheet(boxer_sprite, 10, 10)

# specific sprites
boxer_LR = [boxer_movements[3], boxer_movements[4], boxer_movements[0]]
left_LR_frame = 0
right_LR_frame = 0
boxer_punches = [boxer_movements[16], boxer_movements[17], boxer_movements[18], boxer_movements[19]]
left_punch_frame = 0
right_punch_frame = 0
boxer_block = [boxer_movements[20], boxer_movements[21], boxer_movements[22], boxer_movements[23]]
left_block_frame = 0
right_block_frame = 0
boxer_defeated = [boxer_movements[1], boxer_movements[2], boxer_movements[33], boxer_movements[32]]
defeated_frame = 0

# boxers
left_boxer = 0
right_boxer = 0

# health bars
left_health = 300
left_bar_x = 210
right_health = 300
right_bar_x = 590

# timer
timer = 120
time_elapsed = 0
game_over = False

def setup(): # starting screen
    global camera, left_boxer, right_boxer, boxer_LR
    left_boxer = uvage.from_image(100,375,boxer_LR[-1])
    right_boxer = uvage.from_image(700, 375, boxer_LR[-1])
    left_boxer.scale_by(10)
    right_boxer.scale_by(10)
    right_boxer.flip()

def background(): # import boxing ring image
    background = uvage.from_image(screen_width / 2, screen_height / 2, "Ring.png")
    camera.draw(background)

def left_boxer_motions(): # boxer moving side to side, blocking, and punching
    global camera, left_boxer, boxer_LR, left_LR_frame, boxer_punches, left_punch_frame, boxer_block, left_block_frame

    # --- boxer movement ---
    boxer_is_moving = False
    if not uvage.is_pressing("s") and not uvage.is_pressing("w") and uvage.is_pressing("a") and left_boxer.x > 100:
        left_boxer.x -= 2
        boxer_is_moving = True
    if not uvage.is_pressing("s") and not uvage.is_pressing("w") and uvage.is_pressing("d") and left_boxer.x < 700:
        left_boxer.x += 2
        boxer_is_moving = True

    if boxer_is_moving == True:
        left_LR_frame += .2
        if left_LR_frame > 1:
            left_LR_frame = 0
        left_boxer.image = boxer_LR[int(left_LR_frame)]
    else:
        left_boxer.image = boxer_LR[-1]

    # --- punching movements ---
    if uvage.is_pressing("w"):
        left_boxer.image = boxer_punches[int(left_punch_frame)]
        if left_punch_frame > 3:
            left_punch_frame = 0
        else:
            left_punch_frame += .5

    # --- blocking ---
    if uvage.is_pressing("s"):
        left_boxer.image = boxer_block[int(left_block_frame)]
        if left_block_frame > 3:
            left_punch_frame = 3
        else:
            left_block_frame += .5

    camera.draw(left_boxer)

def right_boxer_motions(): # boxer moving side to side, blocking, and punching
    global camera, right_boxer, boxer_LR, right_LR_frame, boxer_punches, right_punch_frame, boxer_block, right_block_frame

    # --- boxer movement ---
    boxer_is_moving = False
    if not uvage.is_pressing("down arrow") and not uvage.is_pressing("up arrow") and uvage.is_pressing("left arrow") and right_boxer.x > 100:
        right_boxer.x -= 2
        boxer_is_moving = True
    if not uvage.is_pressing("down arrow") and not uvage.is_pressing("up arrow") and uvage.is_pressing("right arrow") and right_boxer.x < 700:
        right_boxer.x += 2
        boxer_is_moving = True

    if boxer_is_moving == True:
        right_LR_frame += .2
        if right_LR_frame > 1:
            right_LR_frame = 0
        right_boxer.image = boxer_LR[int(right_LR_frame)]
    else:
        right_boxer.image = boxer_LR[-1]

    # --- punching movements ---
    if uvage.is_pressing("up arrow"):
        right_boxer.image = boxer_punches[int(right_punch_frame)]
        if right_punch_frame > 3:
            right_punch_frame = 0
        else:
            right_punch_frame += .5

    # --- blocking ---
    if uvage.is_pressing("down arrow"):
        right_boxer.image = boxer_block[int(right_block_frame)]
        if right_block_frame > 3:
            right_punch_frame = 3
        else:
            right_block_frame += .5

    camera.draw(right_boxer)

def health_bars(): # health bars for respective players
    global camera, left_health, right_health, left_bar_x, right_bar_x

    camera.draw(uvage.from_text(30, 580, "P1", 50, "Black", bold=False))
    camera.draw(uvage.from_text(770, 580, "P2", 50, "Black", bold=False))

    # shorten health bar is damage is dealt to boxer
    if uvage.is_pressing("w") and not uvage.is_pressing("down arrow") and left_boxer.touches(right_boxer):
        right_health -= 1
        right_bar_x += .5

    if uvage.is_pressing("up arrow") and not uvage.is_pressing("s") and right_boxer.touches(left_boxer):
        left_health -= 1
        left_bar_x -= .5

    # change color of health bar based off of length
    if left_health <= 60:
        p1_color = "red"
    elif left_health <= 125:
        p1_color = "orange"
    elif left_health <= 200:
        p1_color = "yellow"
    else:
        p1_color = "green"

    if right_health <= 60:
        p2_color = "red"
    elif right_health <= 125:
        p2_color = "orange"
    elif right_health <= 200:
        p2_color = "yellow"
    else:
        p2_color = "green"

    left_health_bar = uvage.from_color(left_bar_x, 580, p1_color, left_health, 20)
    right_health_bar = uvage.from_color(right_bar_x, 580, p2_color, right_health, 20)
    camera.draw(left_health_bar)
    camera.draw(right_health_bar)

def end():
    global camera, timer, game_over

    # if time expires, go through winning conditions
    if timer <= 0:
        game_over = True
        camera.draw(uvage.from_text(400, 175, "GAME OVER", 50, "Yellow", bold=False))
        camera.draw(uvage.from_text(400, 245, "PRESS SPACE BAR TO RESTART", 50, "Yellow", bold=False))

        if left_health < right_health:
            camera.draw(uvage.from_text(400, 210, "P2 WINS BY DECISION", 50, "Yellow", bold=False))
        if left_health > right_health:
            camera.draw(uvage.from_text(400, 210, "P1 WINS BY DECISION", 50, "Yellow", bold=False))
        if left_health == right_health:
            camera.draw(uvage.from_text(400, 210, "DRAW", 50, "Yellow", bold=False))

    # if a boxer's health bar is gone, declare a winner
    if left_health < 0:
        game_over = True
        camera.draw(uvage.from_text(400, 175, "GAME OVER", 50, "Yellow", bold=False))
        camera.draw(uvage.from_text(400, 210, "P2 WINS", 50, "Yellow", bold=False))
        camera.draw(uvage.from_text(400, 245, "PRESS SPACE BAR TO RESTART", 50, "Yellow", bold=False))

    if right_health < 0:
        game_over = True
        camera.draw(uvage.from_text(400, 175, "GAME OVER", 50, "Yellow", bold=False))
        camera.draw(uvage.from_text(400, 210, "P1 WINS", 50, "Yellow", bold=False))
        camera.draw(uvage.from_text(400, 245, "PRESS SPACE BAR TO RESTART", 50, "Yellow", bold=False))


def restart(): # allows users to restart the game after it is over
    global camera, game_over, left_boxer, right_boxer, left_health, left_bar_x, right_health, right_bar_x, timer, time_elapsed

    # resetting global variables if space bar is pressed
    if uvage.is_pressing("space"):
        left_boxer = 0
        right_boxer = 0
        left_health = 300
        left_bar_x = 210
        right_health = 300
        right_bar_x = 590
        timer = 120
        time_elapsed = 0
        game_over = False
        setup()

def tick(): # game running function
    global camera, game_over, timer, time_elapsed
    camera.clear("Black")

    if not game_over:
        background()
        left_boxer_motions()
        right_boxer_motions()
        health_bars()
        end()

        # timer
        time_elapsed += 1
        if time_elapsed > 30:
            timer -= 1
            time_elapsed = 0
        camera.draw(uvage.from_text(screen_width/2, screen_height/10, str(timer), 60, "Yellow", bold=True))
        camera.display()

    if game_over:
        restart()

setup()
ticks_per_second = 30
uvage.timer_loop(ticks_per_second, tick)
