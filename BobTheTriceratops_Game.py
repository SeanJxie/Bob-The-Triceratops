import arcade as ac
import Game_Objects

# Work on looping textures
# create github

# Screen parameters
SC_WIDTH = 1200
SC_HEIGHT = 600
SC_TITLE = "Bob The Triceratops"

# Constants
PLAYER_X = 200
PLAYER_LENGTH = 200
PLAYER_HEIGHT = 100
GRAVITY_CONSTANT = 1
MAX_JUMP = 500
FLOOR = 50

# Variables
player_y = 100
jumping = False
# Used to avoid jumping while not on floor
in_air = True


# Constantly updating the functions
def update(delta_time):
    ac.start_render()
    draw_floor()
    draw_bob(PLAYER_X, player_y)

    floor_boundary(FLOOR)
    gravity(GRAVITY_CONSTANT)
    jump(jumping)


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
    ac.draw_texture_rectangle(x, y, PLAYER_LENGTH,
                              PLAYER_HEIGHT, bob_texture)


def draw_floor():
    floor_texture = ac.load_texture("Assets/floor.png")

    def fit_screen_floor(center_x):
        for k in range(1, 5):
            ac.draw_texture_rectangle(100, FLOOR,
                                      300 + k * 300, 110, floor_texture)
    fit_screen_floor(600)


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
