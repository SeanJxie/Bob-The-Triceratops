import arcade as ac

"""
Module for handling game objects which can cause a game-over

"""


class PlayerObject:
    def __init__(self, x_pos, y_pos, width, height, angle, visual=False):
        self.x = x_pos
        self.y = y_pos
        self.wt = width
        self.ht = height
        self.a = angle
        self.vis = visual

    def draw(self):
        # Loading and drawing Bob
        bob_texture = ac.load_texture("Assets/Bob.png")
        ac.draw_texture_rectangle(
            self.x, self.y,
            self.wt, self.ht,
            bob_texture,
            angle=self.a
        )

    def get_hit_box(self):
        left_bound = self.x - self.wt / 2
        right_bound = self.x + self.wt / 2
        lower_bound = self.y - self.ht / 2
        upper_bound = self.y + self.ht / 2

        if self.vis:
            ac.draw_line(
                right_bound,
                self.y - self.ht / 2,
                right_bound,
                self.y + self.ht / 2,
                ac.color.RED
            )

            ac.draw_line(
                left_bound,
                self.y + self.ht / 2,
                right_bound,
                self.y + self.ht / 2,
                ac.color.RED
            )

            ac.draw_line(
                left_bound,
                self.y - self.ht / 2,
                right_bound,
                self.y - self.ht / 2,
                ac.color.RED
            )

        # Returns hitbox as list
        return [left_bound, right_bound, upper_bound, lower_bound]


class TreeObject:
    def __init__(self, x_pos, y_pos, visual=False):
        self.x = x_pos
        self.y = y_pos
        self.vis = visual

        # Constants
        self.TREE_HEIGHT = 150
        self.TREE_WIDTH = 80

    def draw(self):
        tree_texture = ac.load_texture("Assets/tree.png")
        ac.draw_texture_rectangle(
            self.x, self.y,
            self.TREE_WIDTH,
            self.TREE_HEIGHT,
            tree_texture
        )

    def get_hit_box(self):
        left_bound = self.x - self.TREE_WIDTH / 2
        right_bound = self.x + self.TREE_WIDTH / 2
        upper_bound = self.y + self.TREE_HEIGHT / 2

        if self.vis:
            ac.draw_line(
                left_bound,
                self.y - self.TREE_HEIGHT / 2,
                left_bound,
                self.y + self.TREE_HEIGHT / 2,
                ac.color.RED
            )

            ac.draw_line(
                right_bound,
                self.y - self.TREE_HEIGHT / 2,
                right_bound,
                self.y + self.TREE_HEIGHT / 2,
                ac.color.RED
            )

            ac.draw_line(
                left_bound,
                self.y + self.TREE_HEIGHT / 2,
                right_bound,
                self.y + self.TREE_HEIGHT / 2,
                ac.color.RED
            )

        # Returns hitbox as list
        return [left_bound, right_bound, upper_bound]
