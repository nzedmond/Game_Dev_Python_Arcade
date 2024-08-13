import arcade
import random

SPRITE_SCALING_PLAYER = 0.6
SPRITE_SCALING_METEOR = 0.3
SPRITE_SCALING_LASER = 0.8
METEOR_COUNT = 50

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
LASER_SPEED = 20
PLAYER_SPEED = 10

PLAYER_ICON = ":resources:images/space_shooter/playerShip1_orange.png"
METEOR_ICON = ":resources:images/space_shooter/playerShip1_blue.png"
LASER_ICON = ":resources:images/space_shooter/laserRed01.png"
GAME_MUSIC = "seffect1.mp3"
EXPLOSION = "explosion1.mp3"


class Player(arcade.Sprite):
    def __init__(self, image, scale, x, y):
        super().__init__(image, scale, x, y)
        self.center_x = x
        self.center_y = y
        self.change_x = 0

    def update(self, delta_time: float = 1 / 60, *args, **kwargs):
        # Move the player
        self.center_x += self.change_x

        # confine the player within teh screen boundaries
        if self.left < 0:
            self.left = 0
        if self.right > SCREEN_WIDTH:
            self.right = SCREEN_WIDTH


class Meteor(arcade.Sprite):
    def __init__(self, image, scale):
        super().__init__(image, scale)
        self.center_x = 0
        self.center_y = 0

    def update(self, delta_time: float = 1 / 60, *args, **kwargs):
        # move meteors down
        self.center_y -= 1

        # keep the meteors withing the active zone
        if self.top < 0:
            self.bottom = SCREEN_HEIGHT


class Laser(arcade.Sprite):
    def __init__(self, image, scale):
        super().__init__(image, scale)
        self.center_x = 0
        self.center_y = 0
        self.change_y = 0

    # def update(self, delta_time: float = 1 / 60, *args, **kwargs):
    #     # move the laser beam
    #     self.center_y += 1
    #
    #     # keep releasing beams as long as the game is on (the player is alive)
    #     if self.bottom >


class MyGame(arcade.Window):
    """Main application class"""

    def __init__(self):
        """Initializer"""
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, "Sprites and Bullets Demo")
        self.music = arcade.load_sound(GAME_MUSIC)
        arcade.play_sound(self.music)
        # variables to hold sprite lists
        self.player_list = None
        self.meteor_list = None
        self.laser_list = None

        # set up the player info
        self.player_sprite = None
        self.score = 0

        # hide the cursor
        self.set_mouse_visible(False)

        arcade.set_background_color(arcade.color.AMAZON)

    def setup(self):
        """Set up the game and initialize the variables"""

        # sprite lists
        self.player_list = arcade.SpriteList()
        self.meteor_list = arcade.SpriteList()
        self.laser_list = arcade.SpriteList()

        # set up the starting score
        self.score = 0

        # set up  the player
        self.player_sprite = Player(PLAYER_ICON, SPRITE_SCALING_PLAYER, 50, 70)
        self.player_list.append(self.player_sprite)

        # create the meteors
        for i in range(METEOR_COUNT):
            meteor = Meteor(METEOR_ICON, SPRITE_SCALING_METEOR)

            # position the meteor
            meteor.angle = 180
            meteor.center_x = random.randrange(50, SCREEN_WIDTH - 50)
            meteor.center_y = random.randrange(70, SCREEN_HEIGHT)

            self.meteor_list.append(meteor)

    def on_draw(self):
        self.clear()
        self.meteor_list.draw()
        self.player_list.draw()
        self.laser_list.draw()

        arcade.draw_text(f"Score: {self.score}", 10, 20, arcade.color.WHITE, 14)

    def on_key_press(self, key, modifiers):
        """called whenever a key is pressed on the keyboard"""
        # control the player movement
        if key == arcade.key.LEFT:
            self.player_sprite.change_x = -PLAYER_SPEED
        elif key == arcade.key.RIGHT:
            self.player_sprite.change_x = PLAYER_SPEED

        # control the lasers
        if key == arcade.key.SPACE or key == arcade.key.UP:
            laser = Laser(LASER_ICON, SPRITE_SCALING_LASER)
            laser.center_x = self.player_sprite.center_x
            laser.center_y = self.player_sprite.center_y + 40
            laser.change_y = LASER_SPEED

            self.laser_list.append(laser)

    def on_key_release(self, key, modifiers):
        """called whenever a key is released"""
        if key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player_sprite.change_x = 0

    def on_update(self, delta_time: float):
        """Movement and game logic"""
        self.meteor_list.update()
        self.player_list.update()
        self.laser_list.update()
        # loop through all the lasers
        for laser in self.laser_list:
            # check if the laser hits the stone
            hit_list = arcade.check_for_collision_with_list(laser, self.meteor_list)

            # garbage collect all hit meteors
            if len(hit_list) > 0:
                laser.remove_from_sprite_lists()

            # for every meteor we hit, increment the score and garbage collect it
            for meteor in hit_list:
                meteor.remove_from_sprite_lists()
                self.score += 1

            # if the laser goes off the screen, garbage collect it
            if laser.bottom > SCREEN_HEIGHT:
                laser.remove_from_sprite_lists()


def main():
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
