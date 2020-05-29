# this imports everything from tkinter
# tkinter is the main graphical user interface library for python
from tkinter import *
import time
from random import randint

class Game:
    def __init__(self):
        # creates a tkinter window
        window = Tk()
        # creates a canvas
        self.canvas = Canvas(window, width=600, height=400)
        #"packs" the canvas into the window
        self.canvas.pack()
        self.create_bg()
        self.ring     = Ring(self.canvas, 100)
        self.sonic    = Sonic(self.canvas, "Sonic")
        self.knuckles = Sonic(self.canvas, "Knuckles")
        self.canvas.bind("<KeyPress>", self.key_press)
        self.canvas.bind("<KeyRelease>", self.key_release)
        self.canvas.focus_set()

        self.ring_image     = PhotoImage(file="img/Big/ring.gif")
        self.sonic_score    = self.canvas.create_text( 60, 380, text=0, font=("Purisa", 32), fill="blue")
        self.knuckles_score = self.canvas.create_text(540, 380, text=0, font=("Purisa", 32), fill="red")
        
        self.anim()
        # keeps the window running
        window.mainloop()

    def key_press(self, key):
        if key.char.lower() == "a":
            self.sonic.move(self.sonic.LEFT)
        if key.char.lower() == "d":
            self.sonic.move(self.sonic.RIGHT)
        if key.char.lower() == "w":
            self.sonic.jump()                       # added clause

        if key.char.lower() == "j":
            self.knuckles.move(self.knuckles.LEFT)
        if key.char.lower() == "l":
            self.knuckles.move(self.knuckles.RIGHT)
        if key.char.lower() == "i":
            self.knuckles.jump()

    def key_release(self, key):
        if key.char.lower() == "a" or key.char.lower() == "d":
            self.sonic.stance()
        elif key.char.lower() == "j" or key.char.lower() == "l":
            self.knuckles.stance()

    def create_bg(self):
        self.bg_image = PhotoImage(file="img/bg.png")
        self.background = self.canvas.create_image(300, 200, image=self.bg_image)

    def anim(self):
        while True:
            self.ring.anim()
            self.sonic.anim()
            self.knuckles.anim()
            self.collision(self.sonic)
            self.collision(self.knuckles)
            time.sleep(0.1)

    def collision(self, player):
        ring_pos = self.ring.pos()
        player_pos = player.pos()
        # checks if sonic and ring collide
        if player_pos[0] - 20 < ring_pos[0] < player_pos[0] + 20:
            if player_pos[1] - 20 < ring_pos[1] < player_pos[1] + 20:       # added a lot to this function
                if ring_pos[0] < 300:
                    self.ring.move(randint(0, 300), 0)
                else:
                    self.ring.move(randint(-300, 0), 0)

                if ring_pos[1] > 280:
                    self.ring.move(0, randint(-25, 0))                        ######## spaghetti
                else:
                    self.ring.move(0, randint(0, 25))
                print(self.ring.pos())
                player.score = player.score + 1
                if player.name == "Sonic":
                    self.canvas.itemconfig(self.sonic_score, text=player.score)
                else:
                    self.canvas.itemconfig(self.knuckles_score, text=player.score)

class Sonic:
    RIGHT   = "right"
    LEFT    = "left"
    STANCE  = "stance"
    RUN     = "run"
    JUMP    = "jump"

    STANCE_LIST = [ "0",  "1",  "2",  "3", "4"]
    RUN_LIST    = ["11", "12", "13", "14"]
    JUMP_LIST   = ["22", "23", "24", "25", "26", "27"]     # added list
    SPEED  = 25
    def __init__(self, canvas, name):
        self.animation = 0
        self.direction = self.RIGHT
        self.action = self.STANCE
        self.name = name
        self.score = 0
        
        self.sprite = PhotoImage(file="img/" + self.name + "/" + self.direction + "/0.png")
        self.sonic = canvas.create_image(300, 330, image=self.sprite)
        self.canvas = canvas


    def move(self, direction):
        self.direction = direction
        if self.action != self.JUMP:
            self.action = self.RUN      # added clause
        else:
            if self.direction == self.RIGHT:
                self.canvas.move(self.sonic,  self.SPEED, 0) ######## spaghetti
            else:
                self.canvas.move(self.sonic, -self.SPEED, 0)

    def stance(self):
        if self.action != self.JUMP:
            self.action = self.STANCE

    def jump(self):
        if self.action != self.JUMP:
            self.animation = 0
            self.action = self.JUMP        # added function

    def pos(self):
        return self.canvas.coords(self.sonic)

    def anim(self):
        if self.action == self.RUN:
            sprite_list = self.RUN_LIST
        elif self.action == self.STANCE:
            sprite_list = self.STANCE_LIST
        elif self.action == self.JUMP:
            sprite_list = self.JUMP_LIST       # added clause
            self.jump_anim()

        if self.action == self.RUN and self.direction == self.RIGHT:
            self.canvas.move(self.sonic,  self.SPEED, 0)
        elif self.action == self.RUN and self.direction == self.LEFT:
            self.canvas.move(self.sonic, -self.SPEED, 0)

        self.animation = (self.animation + 1) % (len(sprite_list))
        self.sprite = PhotoImage(file="img/" + self.name + "/" + self.direction + "/" + sprite_list[self.animation] + ".png")
        self.canvas.itemconfig(self.sonic, image=self.sprite)
        self.canvas.update()

    def jump_anim(self):
        if self.animation < len(self.JUMP_LIST)/2:
            self.canvas.move(self.sonic, 0, -self.SPEED)
        elif not self.animation == len(self.JUMP_LIST) - 1:           # added function
            self.canvas.move(self.sonic, 0, self.SPEED)
        else:
            self.canvas.move(self.sonic, 0, self.SPEED)
            self.action = self.STANCE ######## spaghetti
        

class Ring:
    def __init__(self, canvas, x):
        self.sprite = PhotoImage(file="img/Rings/0.png")
        self.ring = canvas.create_image(x, 330, image=self.sprite)
        self.animation = 0
        self.canvas = canvas

    def move(self, x, y):
        self.canvas.move(self.ring, x, y)           # added argument

    def pos(self):
        return self.canvas.coords(self.ring)

    def anim(self):
        self.ANIM = ["0", "1", "2", "3", "4"]
        self.animation = (self.animation + 1) % len(self.ANIM)
        self.sprite = PhotoImage(file="img/Rings/" + self.ANIM[self.animation] + ".png")
        self.canvas.itemconfig(self.ring, image=self.sprite)
        self.canvas.update()

Game()
