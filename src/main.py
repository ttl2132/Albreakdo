from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.properties import (
    NumericProperty, ReferenceListProperty, ObjectProperty, StringProperty
)
from kivy.vector import Vector
from kivy.graphics import Rectangle, Color
from kivy.uix.screenmanager import ScreenManager, Screen, WipeTransition

DURATION = 100

class Paddle(Widget):
    """
    add docstring
    """

    paddleR = NumericProperty(255)
    paddleG = NumericProperty(255)
    paddleB = NumericProperty(255)
    timer = NumericProperty(DURATION)

    def on_touch_up(self, touch):
        """
        touch controls to change paddles if touched paddle
        """
        if self.collide_point(touch.x, touch.y):
            #white to tan
            if(self.paddleR == 255 and self.paddleG == 255 and self.paddleB == 255):
                self.paddleR = 210
                self.paddleG = 180
                self.paddleB = 140

            #tan to green
            elif (self.paddleR == 210 and self.paddleG == 180 and self.paddleB == 140):
                self.paddleR = 0
                self.paddleG = 255
                self.paddleB = 0

            #green to blue
            elif (self.paddleR == 0 and self.paddleG == 255 and self.paddleB == 0):
                self.paddleR = 0
                self.paddleG = 0
                self.paddleB = 255

            #blue to white
            elif (self.paddleR == 0 and self.paddleG == 0 and self.paddleB == 255):
                self.paddleR = 255
                self.paddleG = 255
                self.paddleB = 255            

    def bounce_ball(self, ball):
        """
        set ball fixed velocity based on color paddle.
        """
        if self.collide_widget(ball):
            vx, vy = ball.velocity

            #if paddle is white
            if(self.paddleR == 255 and self.paddleG == 255 and self.paddleB == 255):
                if (vx > 0):
                    vel = Vector(5, 15)
                else:
                    vel = Vector(-5, 15)

            #if paddle is tan
            if(self.paddleR == 210 and self.paddleG == 180 and self.paddleB == 140):
                if (vx > 0):
                    vel = Vector(4, 12)
                else:
                    vel = Vector(-4, 12)

            #if paddle is green
            elif(self.paddleR == 0 and self.paddleG == 255 and self.paddleB == 0):
                if (vx > 0):
                    vel = Vector(3, 9)
                else:
                    vel = Vector(-3, 9)

            #if paddle is blue
            elif(self.paddleR == 0 and self.paddleG == 0 and self.paddleB == 255):
                if (vx > 0):
                    vel = Vector(2, 6)
                else:
                    vel = Vector(-2, 6)
            
            #change ball color and velocity to match paddle hit
            ball.velocity = vel.x, vel.y
            ball.ballR = self.paddleR
            ball.ballG = self.paddleG
            ball.ballB = self.paddleB

class Ball(Widget):
    """
    add docstring
    """
    # def __init__(self):
    #     pass

    ballR = NumericProperty(255)
    ballG = NumericProperty(0)
    ballB = NumericProperty(0)

    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)

    def move(self):
        """
        add docstring
        """
        self.pos = Vector(*self.velocity) + self.pos
#       I think that this line of code can go within __init__ function instead


class Game(Widget):
    """
    add docstring
    """
    ball = ObjectProperty(None)
    player1 = ObjectProperty(None)
    canvasOpacity = NumericProperty(0)

    #logic/assets inspired by https://github.com/Dirk-Sandberg/2DKivyGame.git
    cloud_texture = ObjectProperty(None)
    sun_texture = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(Game,self).__init__(**kwargs)
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)
        self._keyboard.bind(on_key_up=self._on_keyboard_up)

        # Create textures
        self.cloud_texture = Image(source="cloud.png").texture
        self.cloud_texture.wrap = 'repeat'
        self.cloud_texture.uvsize = (
            Window.width / self.cloud_texture.width, -1
            )
        self.sun_texture = Image(source="sun.png").texture
        self.sun_texture.uvsize = (Window.width / self.sun_texture.width, -1)

        button_size = (Window.width/5, Window.height/8)
        self.restart_button = Button(
            pos = (Window.width*0.4, self.center_y + self.height * 2.5),
            size = button_size, text='Try Again',
            on_release=self.restart
        )
        self.menu_button = Button(
            pos = (Window.width*0.4, self.center_y + self.height * 1.5),
            size = button_size, text='Back to Main Menu',
            on_release=self.change_screen
        )

        self.keyPressed = set()

    def _keyboard_closed(self):
        """
        add docstring
        """
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard.unbind(on_key_up=self._on_keyboard_up)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        """
        keyboard controls for paddle if playing on computer
        """

        self.keyPressed.add(keycode[1])

        if keycode[1] == 'spacebar':
            #white to tan
            if(self.player1.paddleR == 255 and self.player1.paddleG == 255 and self.player1.paddleB == 255):
                self.player1.paddleR = 210
                self.player1.paddleG = 180
                self.player1.paddleB = 140

            #tan to green
            elif (self.player1.paddleR == 210 and self.player1.paddleG == 180 and self.player1.paddleB == 140):
                self.player1.paddleR = 0
                self.player1.paddleG = 255
                self.player1.paddleB = 0

            #green to blue
            elif (self.player1.paddleR == 0 and self.player1.paddleG == 255 and self.player1.paddleB == 0):
                self.player1.paddleR = 0
                self.player1.paddleG = 0
                self.player1.paddleB = 255

            #blue to white
            elif (self.player1.paddleR == 0 and self.player1.paddleG == 0 and self.player1.paddleB == 255):
                self.player1.paddleR = 255
                self.player1.paddleG = 255
                self.player1.paddleB = 255

        return True

    def _on_keyboard_up(self, keyboard, keycode):
        """
        keyboard controls for paddle if playing on computer
        """
        if keycode[1] in self.keyPressed:
            self.keyPressed.remove(keycode[1])

    def key_move(self, dt):
        """
        keyboard controls for paddle if playing on computer
        """
        currentx = self.player1.pos[0]
        currenty = self.player1.pos[1]

        step_size = 1000 * dt

        if 'right' in self.keyPressed:
            currentx += step_size

        if 'left' in self.keyPressed:
            currentx -= step_size

        self.player1.pos = (currentx, currenty)

    def on_touch_move(self, touch):
        """
        add docstring
        """
        if touch.x < self.width / 2:
            self.player1.center_x = touch.x
        if touch.x > self.width - self.width / 2:
            self.player1.center_x = touch.x

    def on_size(self, *args):
        """
        add docstring
        """
        self.cloud_texture.uvsize = (self.width / self.cloud_texture.width, -1)

    def serve_ball(self, vel=(2, -5)):
        """
        add docstring
        """
        #make ball (ray) come from sun's position
        self.ball.center = (0.25 * self.center_x, self.center_y + self.center_y/2) 
        self.ball.velocity = vel
        self.ball.ballR = 255
        self.ball.ballG = 0
        self.ball.ballB = 0

    def update(self, dt):
        """
        add docstring
        """

        #print game over!
        #if(self.canvasOpacity == 0.6):
            #l = Label(text='Game Over!', font_size=100, pos=self.pos)

        # Update the uvpos of the texture
        self.cloud_texture.uvpos = ((self.cloud_texture.uvpos[0] +
            dt/2.0) % Window.width, self.cloud_texture.uvpos[1])
        # Redraw the texture
        texture = self.property('cloud_texture')
        texture.dispatch(self)

        self.ball.move()
        self.key_move(dt)

        #make timer slower or faster based on time left
        #activate a canvas on the screen which makes it redder at each mark
        if(self.player1.timer >= 80):
            self.canvasOpacity = 0
            self.player1.timer -= 2 * 0.01
        elif(self.player1.timer >= 50 and self.player1.timer < 80):
            self.player1.timer -= 4 * 0.01
            self.canvasOpacity = 0.2
        elif(self.player1.timer >= 20 and self.player1.timer < 50):
            self.player1.timer -= 6 * 0.01
            self.canvasOpacity = 0.4
        elif(self.player1.timer > 0 and self.player1.timer < 20):
            if self.player1.timer < 6 * 0.01:
                self.player1.timer = 0
                self.game_over()
            else:
                self.player1.timer -= 6 * 0.01
                self.canvasOpacity = 0.6
        elif(self.player1.timer <= 0):
            self.canvasOpacity = 1
            self.player1.timer = 0
            self.game_over()

        # bounce off paddles
        self.player1.bounce_ball(self.ball)

        # bounce ball off top
        if self.ball.top > self.top:
            self.ball.velocity_y *= -1

        # bounce off sides
        if self.ball.x < self.x:
            self.ball.velocity_x *= -1
        if self.ball.x > self.width:
            self.ball.velocity_x *= -1

        # went off bottom
        if self.ball.y < self.y:
            self.serve_ball()

    def play(self):
        self.reset()
        self.serve_ball()
        Clock.schedule_interval(self.update, 1.0 / 60.0)

    def game_over(self):
        self.remove_widget(self.restart_button)
        self.remove_widget(self.menu_button)
        self.add_widget(self.restart_button)
        self.add_widget(self.menu_button)

    def restart(self, instance):
        self.reset()
        self.play()

    def change_screen(self, instance):
        sm = self.parent.parent
        sm.current = 'home'

    def reset(self):
        self.remove_widget(self.restart_button)
        self.remove_widget(self.menu_button)
        Clock.unschedule(self.update)
        self.player1.timer = DURATION

class Control(Widget):
    """
    add docstring
    """
    player1 = ObjectProperty(None)

    def on_touch_move(self, touch):
        """
        add docstring
        """
        if touch.x < self.width / 2:
            self.player1.center_x = touch.x
        if touch.x > self.width - self.width / 2:
            self.player1.center_x = touch.x
    
class About(Widget):
    """
    add docstring
    """

class ElectroMagneticSpectrum(Widget):
    """
    add docstring
    """

class Sun(Widget):
    """
    add docstring
    """

class Albedo(Widget):
    """
    add docstring
    """

class Colors(Widget):
    """
    add docstring
    """

class Gasses(Widget):
    """
    add docstring
    """

class Manager(ScreenManager):
    pass

class BrickBreakApp(App):
    """
    add docstring
    """

    # def __init__(self):
    #     pass  # do you need an __init__ function, or does the `build` function below serve the same purpose?

    def build(self):
        """
        add docstring
        """
        return Manager(transition=WipeTransition())

if __name__ == '__main__':
    BrickBreakApp().run()
