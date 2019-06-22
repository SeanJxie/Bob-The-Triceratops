import arcade as ac
import random
from Game import game_objects

# Screen parameters
SC_WIDTH = 1200
SC_HEIGHT = 600
SC_TITLE = "Bob The Triceratops"

# Constants
PLAYER_WIDTH = 200
PLAYER_HEIGHT = 100
GRAVITY_CONSTANT = 1
MAX_JUMP = 500
FLOOR = 50

FLOOR_TILE_HEIGHT = 110
FLOOR_TILE_WIDTH = 300

# Game variables --------------------------------------------------------------
# Used for starting/stopping the game
game_state = False
# Used to avoid jumping while not on floor
in_air = True

# Used to represent x-value of the center of the screen
# relative to the game environment
screen_center = SC_WIDTH / 2

# "Difficulty" of game
game_speed = 10
background_speed = game_speed / 1.1
frame_count = 1

# Player variables
player_x = 200
player_y = 100
jumping = False
hit_state = False
# For the terrible "running" effect
player_angle = 0
running_speed = 4
player_score = 0
# Tracking the "game start" jump
initial_jump = False

# x-value of tree is random
# There is only one tree per floor segment
tree_x = random.randint(SC_WIDTH, 2 * SC_WIDTH)
# x-value of tree varies between 145px and 155px
tree_y = random.randint(145, 155)

# Aesthetics variables --------------------------------------------------------
# Amount and list of initial x-values of floor "tiles"
floor_tiles = 8
floor_x = \
    [
        FLOOR_TILE_WIDTH / 2 + FLOOR_TILE_WIDTH * k
        for k in range(floor_tiles)
    ]

# Initial x_values of background "tiles"
background_tiles = 3
background_x = \
    [
        SC_WIDTH / 2 + SC_WIDTH * k
        for k in range(background_tiles)
    ]


# Constantly updating the functions
def update(delta_time):
    global frame_count

    ac.start_render()

    # All values are reset when player is not playing
    if game_state is False:
        reset_values()

    # Rendering aesthetics
    draw_background()
    draw_floor()
    draw_bob()

    # Player interactions
    floor_boundary(FLOOR)
    gravity(GRAVITY_CONSTANT)
    jump(jumping)

    if initial_jump and game_state:
        # Moving the player and the viewport
        viewport(screen_center)
        move_with_screen()

        # Game mechanics
        obstacles()
        collision()
        score()
        difficulty_progression()
        move_background()
        running()

        frame_count += 1


# PLAYER INTERACTION ----------------------------------------------------------
# Player
def draw_bob():
    global bob, player_angle, running_speed
    # Bob Player object is drawn using the game_objects module
    bob = game_objects.PlayerObject(
        player_x, player_y,
        PLAYER_WIDTH, PLAYER_HEIGHT,
        player_angle
    )
    bob.draw()


def running():
    # The "running" effect
    # the player rotates 20 degrees in direction
    # for a complete range of 40 degrees
    global player_angle, running_speed
    angle_cap = 20
    if player_angle >= angle_cap:
        running_speed = -running_speed

    elif player_angle <= -angle_cap:
        running_speed = -running_speed

    player_angle += running_speed


# Simulating the effect of gravity
def gravity(g_const):
    global player_y, velocity

    def fall_dist():
        return MAX_JUMP - player_y

    # Calculating velocity at a given height
    # using the gravity constant
    velocity = (2 * g_const * fall_dist()) ** 0.5
    player_y -= velocity


# To perform a full jump
def jump(state):
    global player_y, jumping

    if state:
        # Player "jumps" with twice the force
        # of the constant effect of gravity
        player_y += 2 * velocity

        # Checking if player has reached the jump height
        # a little is subtracted off of MAX_JUMP to avoid the risk of
        # calculating negative distance
        if player_y >= MAX_JUMP - 2:
            jumping = False


# Moving the screen
def viewport(viewport_x):
    ac.set_viewport(
        viewport_x - SC_WIDTH / 2,
        viewport_x + SC_WIDTH / 2,
        0,
        SC_HEIGHT
    )


def move_with_screen():
    global player_x, screen_center
    player_x += game_speed
    screen_center += game_speed


# Everything that has to do with the "ground" in game
def floor_boundary(y_bound):
    global player_y, in_air

    # Collision with ground
    if player_y - PLAYER_HEIGHT <= y_bound:
        player_y = y_bound + PLAYER_HEIGHT
        in_air = False

    else:
        in_air = True


def keypress(symbol, modifiers):
    global jumping, initial_jump, game_state
    if symbol == ac.key.SPACE and not in_air:
        jumping = True
        initial_jump = True
        game_state = True


# GAME MECHANICS --------------------------------------------------------------
def obstacles():
    global tree_x, tree_y, tree
    tree = game_objects.TreeObject(tree_x, tree_y)

    tree.draw()
    # If tree gets out of screen, reset it to a random x-value
    # Ahead of the screen
    if tree_x <= screen_center - SC_WIDTH / 2:
        tree_x += random.randint(SC_WIDTH, 2 * SC_WIDTH)
        tree_y = random.randint(145, 155)


def collision():
    global hit_state, game_state
    # Indices of hitbox sides
    left = 0
    right = 1
    upper = 2
    lower = 3

    player_hitbox = bob.get_hit_box()
    tree_hitbox = tree.get_hit_box()

    # Collision logic
    if (tree_hitbox[left] <= player_hitbox[right] <= tree_hitbox[right]
        or
        (tree_hitbox[left] <= player_hitbox[left] <= tree_hitbox[right]
        )) \
            and \
            (tree_hitbox[upper] >= player_hitbox[lower]):
        game_state = False


def score():
    global player_score
    # +1 point every 10 frames
    if frame_count % 10 == 0:
        player_score += 1

    ac.draw_text(
        f"Score: {player_score}",
        screen_center - 600, 573,
        ac.color.BLACK, 20
    )


def difficulty_progression():
    global game_speed
    # Every 100 frames, game accelerates by 0.15 px/s^2
    if frame_count % 100 == 0:
        game_speed += 0.15


def move_background():
    # A separate function from draw_background() for easy
    # disable of background movement

    # The background moves slowly
    # to the right, producing the effect of distance
    for i in range(background_tiles):
        background_x[i] += background_speed


def reset_values():
    global frame_count, game_speed, background_x, floor_x, tree_x
    global screen_center, player_x, player_score, player_angle, tree_y

    # The initial values when game is not being player
    background_x = \
        [
            SC_WIDTH / 2 + SC_WIDTH * k
            for k in range(background_tiles)
        ]

    floor_x = \
        [
            FLOOR_TILE_WIDTH / 2 + FLOOR_TILE_WIDTH * k
            for k in range(floor_tiles)
        ]

    tree_x = random.randint(SC_WIDTH, 2 * SC_WIDTH)
    tree_y = random.randint(145, 155)

    screen_center = SC_WIDTH / 2
    player_x = 200
    game_speed = 10
    frame_count = 0
    player_score = 0
    player_angle = 0


# AESTHETICS ------------------------------------------------------------------
def draw_floor():
    floor_texture = ac.load_texture("Assets/floor.png")

    # Drawing the floor tiles using floor_x list
    for i in range(floor_tiles):
        ac.draw_texture_rectangle(
            floor_x[i], FLOOR,
            FLOOR_TILE_WIDTH, FLOOR_TILE_HEIGHT,
            floor_texture
        )

        # Check if a floor texture has moved off of the screen
        # If so reset it to "in front" of the viewing area
        if floor_x[i] <= screen_center - SC_WIDTH / 2 - FLOOR_TILE_WIDTH / 2:
            floor_x[i] += 2 * SC_WIDTH


def draw_background():
    background_texture = ac.load_texture("Assets/background.png")

    # Same logic as draw_floor() function
    # Except it's for a slower moving background
    for i in range(background_tiles):
        ac.draw_texture_rectangle(
            background_x[i], SC_HEIGHT / 2,
            SC_WIDTH, SC_HEIGHT,
            background_texture
        )

        # Looping to front of screen when out of view
        if background_x[i] <= screen_center - SC_WIDTH - 100:
            background_x[i] += len(background_x) * SC_WIDTH

    ac.draw_texture_rectangle(
        -SC_WIDTH / 2, SC_HEIGHT / 2,
        SC_WIDTH, SC_HEIGHT,
        background_texture
    )


# All window related things
def window_setup():
    ac.open_window(SC_WIDTH, SC_HEIGHT, SC_TITLE)
    ac.set_background_color([153, 217, 234])

    # Game runs at 60 updates/second
    ac.schedule(update, 1 / 60)

    # Player input
    window = ac.get_window()
    window.on_key_press = keypress

    ac.run()


window_setup()
