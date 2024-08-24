import random
import arcade

# -------------GAME CONSTANTS ----------
SCREEN_HEIGHT = 600
SCREEN_WIDTH = 800

BOX_ICON = ":resources:images/tiles/boxCrate_single.png"
PLAYER_ICON = ":resources:images/animated_characters/female_person/femalePerson_walk4.png"

BOX_SCALE = 0.6
PLAYER_SCALE = 0.6

PLAYER_SPEED = 10
WALL_SPEED = 0

GAME_TITLE = "WALL CLIMBER"


class Player(arcade.Sprite):
    def __init__(self, image, scale):
        super().__init__(image, scale)
        self.center_x = 0
        self.center_y = 0
        self.change_x = 0
        self.change_y = 0

    def update(self, delta_time: float = 1 / 60, *args, **kwargs):
        # move the player
        self.center_x += self.change_x
        self.center_y += self.change_y

        # confine the player withing the screen boundaries
        if self.left < 0:
            self.left = 0
        if self.right > SCREEN_WIDTH:
            self.right = SCREEN_WIDTH

        if self.bottom < 0:
            self.bottom = 0
        if self.top > SCREEN_HEIGHT:
            self.top = SCREEN_HEIGHT


class Wall(arcade.Sprite):
    def __init__(self, image, scale):
        super().__init__(image, scale)
        self.center_x = 0
        self.center_y = 0


class MyGame(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)

        # initializing the game physics engine
        self.physics_engine = None

        # creating sprite lists
        self.player_sprites_list = None
        self.wall_sprites_list = None

        # creating player
        self.player = None
        self.player_life = 100

        # setting up the wall
        self.wall = None

        # set the background color
        arcade.set_background_color(arcade.color.DEEP_JUNGLE_GREEN)

    def set_up(self):
        """ Initializing the game and setting up the variables"""

        # setting up the game's physics engine which make sure that a player doesn't walk through the walls
        # self.physics_engine = arcade.PhysicsEngineSimple(self.player, self.wall_sprites_list)

        # setting up the sprite lists
        self.player_sprites_list = arcade.SpriteList()
        self.wall_sprites_list = arcade.SpriteList()

        # setting up the player
        self.player = Player(PLAYER_ICON, PLAYER_SCALE)
        self.player.center_x = 50
        self.player.center_y = 70
        self.player_sprites_list.append(self.player)

        # setting up the walls
        for x in range(100, 760, 76):
            wall = Wall(BOX_ICON, BOX_SCALE)
            wall.center_x = x
            wall.center_y = 300
            self.wall_sprites_list.append(wall)

        walls_clique_top = [[400, 548],
                            [400, 472],
                            [476, 472],
                            [476, 548]]

        for coordinate in walls_clique_top:
            wall = Wall(BOX_ICON, BOX_SCALE)
            wall.center_x = coordinate[0]
            wall.center_y = coordinate[1]
            self.wall_sprites_list.append(wall)

        walls_clique_bottom = [[300, 140], [376, 140]]
        for element in walls_clique_bottom:
            wall = Wall(BOX_ICON, BOX_SCALE)
            wall.center_x = element[0]
            wall.center_y = element[1]
            self.wall_sprites_list.append(wall)

    def on_update(self, delta_time):
        # self.physics_engine.update()
        self.player_sprites_list.update()

        # handle player collision with walls
        hit_list = arcade.check_for_collision_with_list(self.player, self.wall_sprites_list)
        # decrement player's life everytime they hit a wall
        if len(hit_list) > 0 and self.player_life > 0:
            self.player_life -= 1

        # check if the player life is zero and end the game
        if self.player_life == 0:
            pass

    def on_draw(self):
        """Drawing all the sprites on the screen"""
        self.clear()
        self.player_sprites_list.draw()
        self.wall_sprites_list.draw()

        arcade.draw_text(f"Life: {self.player_life}", 10, 580, arcade.color.WHITE, 16)

    def on_key_press(self, key, modifiers):
        """ control the player movements using arrow keys
            Allow the player to jump, kneel, and walk forward and backward
        """
        if key == arcade.key.UP:
            self.player.change_y = PLAYER_SPEED
        elif key == arcade.key.DOWN:
            self.player.change_y = -PLAYER_SPEED
        elif key == arcade.key.LEFT:
            self.player.change_x = -PLAYER_SPEED
        elif key == arcade.key.RIGHT:
            self.player.change_x = PLAYER_SPEED

    def on_key_release(self, key, modifiers):
        """called when a key is released"""
        if key == arcade.key.UP or key == arcade.key.DOWN:
            self.player.change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player.change_x = 0


def main():
    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, GAME_TITLE)
    window.set_up()
    arcade.run()


if __name__ == "__main__":
    main()
