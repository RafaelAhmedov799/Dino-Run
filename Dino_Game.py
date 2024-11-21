import arcade
import random

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Dino Run"
GRAVITY = 0.5
DINO_JUMP = 12
CACTUS_SPEED = 5


class Game(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.bg = arcade.load_texture("images//bg.png")
        self.dino = Dino("images//dino1.png", 0.5)
        self.cactus = Cactus("images//cactus1.png", 0.5)
        self.game = True
        self.score = 0
        self.game_over = arcade.load_texture("images//game_over.png")
        self.win = arcade.load_texture("images//win.png")

    def setup(self):
        self.dino.center_x = 100
        self.dino.center_y = 200
        self.cactus.center_x = SCREEN_WIDTH
        self.cactus.center_y = 200
        self.cactus.change_x = CACTUS_SPEED
        self.cactus.append_texture(arcade.load_texture("images/cactus2.png"))
        self.dino.append_texture(arcade.load_texture(
            "images/dino1.png"))
        self.dino.append_texture(arcade.load_texture(
            "images/dino2.png"))
        self.dino.append_texture(arcade.load_texture(
            "images/dino3.png"))

    def on_draw(self):
        self.clear()
        if self.game:
            arcade.draw_texture_rectangle(
                SCREEN_WIDTH/2, SCREEN_HEIGHT/2, SCREEN_WIDTH, SCREEN_HEIGHT, self.bg)

            arcade.draw_text(f"Score: {self.score}", 15,
                             SCREEN_HEIGHT - 35, (255, 255, 255), 25)
        else:
            arcade.draw_texture_rectangle(
                SCREEN_WIDTH/2, SCREEN_HEIGHT/2, SCREEN_WIDTH, SCREEN_HEIGHT, self.game_over)
            arcade.draw_text(f"Final Score: {self.score}", SCREEN_WIDTH/2-125,
                             SCREEN_HEIGHT - 200, (255, 255, 255), 30)
        if self.score >= 20:
            arcade.draw_texture_rectangle(
                SCREEN_WIDTH/2, SCREEN_HEIGHT/2, SCREEN_WIDTH, SCREEN_HEIGHT, self.win)
            self.setup()
            self.dino.stop()
            self.cactus.stop()
        self.dino.draw()
        self.cactus.draw()

    def update(self, delta_time):
        self.dino.update_animation(delta_time)
        self.dino.update()
        self.cactus.update_animation(delta_time)
        self.cactus.update()
        if arcade.check_for_collision(self.cactus, self.dino):
            self.game = False
            self.dino.stop()
            self.cactus.stop()

    def on_key_press(self, key, modifiers):
        if self.game:
            if key == arcade.key.SPACE and not self.dino.jump:
                self.dino.change_y = DINO_JUMP
                self.dino.jump = True


class Animate(arcade.Sprite):
    i = 0
    time = 0
    # to make it move its legs and change texture

    def update_animation(self, delta_time):
        self.time += delta_time
        if self.time >= 0.1:
            self.time = 0
            if self.i == len(self.textures) - 1:
                self.i = 0
            else:
                self.i += 1
            self.set_texture(self.i)


class Dino(Animate):
    jump = False

    def update(self):
        self.center_y += self.change_y
        self.change_y -= GRAVITY
        if self.center_y < 200:
            self.center_y = 200
            self.jump = False


class Cactus(Animate):
    def update(self):
        self.center_x -= self.change_x
        if self.right < 0:
            self.left = SCREEN_WIDTH + random.randint(0, SCREEN_WIDTH)
            window.score += 1


window = Game(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
window.setup()
arcade.run()
