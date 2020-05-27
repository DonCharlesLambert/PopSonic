from tkinter import *
import time

class Game():
    def __init__(self):
        root = Tk() # creates a window
        self.canvas = Canvas(root, width=600, height=400) # creates a canvas to draw in the window
        self.create_bg()
        self.ring = Ring(self.canvas, 500)
        self.sonic = Sonic(self.canvas, "Sonic") #creates Sonic object and puts it on the canvas
        self.knuckles = Sonic(self.canvas, "Knuckles")
        self.canvas.bind("<KeyPress>", self.key_press) # calls key_press function when btn is press
        self.canvas.bind("<KeyRelease>", self.key_release)
        self.canvas.focus_set() # focuses button presses on the canvas
        self.canvas.pack() # packs the canvas into the window
        self.animation()
        root.mainloop() # keeps the window up

    def create_bg(self):
        self.bg_sprite  = PhotoImage(file="img/bg.png")
        self.background = self.canvas.create_image(300, 200, image=self.bg_sprite)

    def key_press(self, key):
        if key.char == "d":
            self.sonic.move(self.sonic.RIGHT)
        if key.char == "a":
            self.sonic.move(self.sonic.LEFT)

        if key.char == "l":
            self.knuckles.move(self.sonic.RIGHT)
        if key.char == "j":
            self.knuckles.move(self.sonic.LEFT)

    def key_release(self, key):
        if key.char == "a" or key.char == "d":
            self.sonic.stance()
        elif  key.char == "l" or key.char == "j":
            self.knuckles.stance()

    def collision(self, player):
        if self.ring.pos()[0] - 10 < player.pos()[0] < self.ring.pos()[0] + 10:
            x = self.ring.pos()[0]
            if x < 300:
                self.ring.move(200)
            else:
                self.ring.move(-200)

    def animation(self):
        while True:
            self.collision(self.sonic)
            self.collision(self.knuckles)
            time.sleep(0.1)
            self.sonic.anim()
            self.knuckles.anim()
            self.ring.anim()
            self.canvas.update()
                

class Sonic():
    SPEED  = 25

    STANCE = "stance"
    RUN    = "run"
    LEFT   = "left"
    RIGHT  = "right"

    STANCE = ["0" , "1", "2", "3", "4"]
    RUN    = ["11", "12", "13", "14"]
    def __init__(self, canvas, name):
        self.sprite = PhotoImage(file="img/" + name + "/left/0.png") # gets the sonic image
        self.sonic = canvas.create_image(300, 330, image=self.sprite) # puts sonic image on canvas
        self.canvas = canvas
        self.name = name
        
        self.animation = 0
        self.direction = self.RIGHT
        self.action = self.STANCE

    def stance(self):
        self.action = self.STANCE
    
    def move(self, direction):
        self.action = self.RUN
        self.direction = direction

    def pos(self):
        return self.canvas.coords(self.sonic)

    def anim(self):
        direction = self.direction
        if self.action == self.RUN:
            sprite_list = self.RUN
            
        elif self.action == self.STANCE:
            sprite_list = self.STANCE

        
        if direction == self.RIGHT and self.action == self.RUN:
            self.canvas.move(self.sonic, self.SPEED, 0)
        elif direction == self.LEFT and self.action == self.RUN:
            self.canvas.move(self.sonic, -self.SPEED, 0)
        
        self.animation = (self.animation + 1) % len(sprite_list)    
        self.sprite = PhotoImage(file=r"img/" + self.name + "/" + self.direction + "/" + sprite_list[self.animation] + ".png")
        self.canvas.itemconfig(self.sonic, image=self.sprite)
        self.canvas.update()

class Ring():
    ANIM = ["0", "1", "2", "3", "4"]
    animation = 0
    def __init__(self, canvas, x):
        self.sprite = PhotoImage(file="img/Rings/0.png")
        self.ring = canvas.create_image(x, 330, image=self.sprite)
        self.canvas = canvas

    def move(self, x):
        self.canvas.move(self.ring, x, 0)

    def pos(self):
        return self.canvas.coords(self.ring)

    def anim(self):
        self.animation = (self.animation + 1) % len(self.ANIM)    
        self.sprite = PhotoImage(file=r"img/Rings/" + self.ANIM[self.animation] + ".png")
        self.canvas.itemconfig(self.ring, image=self.sprite)
        self.canvas.update()

Game() # creates the game object
