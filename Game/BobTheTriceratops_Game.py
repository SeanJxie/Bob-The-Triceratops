import arcade as ac
import Game_Objects

# Create background textures
# Create object class

# Screen parameters
SC_WIDTH = 1200
SC_HEIGHT = 600
SC_TITLE = "Bob The Triceratops"

# Constants
PLAYER_LENGTH = 200
PLAYER_HEIGHT = 100
GRAVITY_CONSTANT = 1
MAX_JUMP = 500
FLOOR = 50

PLATFORM_HEIGHT = 110
PLATFORM_LENGTH = 300

# Game variables --------------------------------------------------------------
player_x = 200
player_y = 100
jumping = False

# Used to avoid jumping while not on floor
in_air = True

# Used to represent x-value of the center of the screen
# relative to the game environment
screen_center = SC_WIDTH / 2

# "Difficulty" of game
game_speed = 1

# Aesthetics variables --------------------------------------------------------
# Amount and list of floor "tiles"
floor_tiles = 8
floor_x = [150 + 300 * k for k in range(floor_tiles)]


# Constantly updating the functions
def update(delta_time):
    global screen_center, player_x
    ac.start_render()
    draw_floor()
    draw_bob(player_x, player_y)
    floor_boundary(FLOOR)
    gravity(GRAVITY_CONSTANT)
    jump(jumping)

    # Moving the player and the viewport
    viewport(screen_center)
    move_with_screen()


# PLAYER INTERACTION ----------------------------------------------------------
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
    global jumping
    if symbol == ac.key.SPACE and not in_air:
        jumping = True


# AESTHETICS ------------------------------------------------------------------
def draw_bob(x, y):
    # Loading and drawing Bob
    bob_texture = ac.load_texture("Assets/Bob.png")
    ac.draw_texture_rectangle(
        x, y,
        PLAYER_LENGTH, PLAYER_HEIGHT,
        bob_texture
    )


def draw_floor():
    floor_texture = ac.load_texture("Assets/floor.png")

    for i in range(floor_tiles):
        ac.draw_texture_rectangle(
            floor_x[i], FLOOR,
            PLATFORM_LENGTH, PLATFORM_HEIGHT,
            floor_texture
        )

        # Check if a floor texture has moved off of the screen
        # If so reset it to "in front" of the viewing area
        if floor_x[i] <= screen_center - SC_WIDTH / 2 - PLATFORM_LENGTH / 2:
            floor_x[i] += 2 * SC_WIDTH


# All window related things
def window_setup():
    ac.open_window(SC_WIDTH, SC_HEIGHT, SC_TITLE)
    ac.set_background_color(ac.color.WHITE)

    # Game runs at 60 updates/second
    ac.schedule(update, 1 / 60)

    # Player input
    window = ac.get_window()
    window.on_key_press = keypress

    ac.run()


window_setup()
