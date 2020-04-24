from tkinter import *

class Game():
    def __init__(self):
        root = Tk() # creates a window
        self.canvas = Canvas(root, width=600, height=400) # creates a canvas to draw in the window
        self.create_bg()
        self.ring = Ring(self.canvas, 500)
        self.sonic = Sonic(self.canvas) #creates Sonic object and puts it on the canvas
        self.canvas.bind("<KeyPress>", self.key_press) # calls key_press function when btn is press
        self.canvas.focus_set() # focuses button presses on the canvas
        self.canvas.pack() # packs the canvas into the window
        self.animation()
        root.mainloop() # keeps the window up

    def create_bg(self):
        self.bg_sprite  = PhotoImage(file="Sonic/bg.png")
        self.background = self.canvas.create_image(300, 200, image=self.bg_sprite)

    def key_press(self, key):
        if key.char == "d":
            self.sonic.move("right")
        if key.char == "a":
            self.sonic.move("left")

    def animation(self):
        while True:
            if self.ring.pos()[0] - 10 < self.sonic.pos()[0] < self.ring.pos()[0] + 10:
                x = self.ring.pos()[0]
                if x < 300:
                    self.ring.move(200)
                else:
                    self.ring.move(-200)
            self.canvas.update()
                

class Sonic():
    animation = 0
    RIGHT = [ "5",  "6",  "7",  "8",  "9", "10"]
    LEFT  = ["20", "21", "22", "23", "24", "25"]
    def __init__(self, canvas):
        self.sprite = PhotoImage(file="Sonic/0.png") # gets the sonic image
        self.sonic = canvas.create_image(300, 330, image=self.sprite) # puts sonic image on canvas
        self.canvas = canvas
        
    def move(self, direction):
        if direction == "right":
            self.canvas.move(self.sonic, 10, 0)
        elif direction == "left":
            self.canvas.move(self.sonic, -10, 0)
        self.anim(direction)

    def pos(self):
        return self.canvas.coords(self.sonic)

    def anim(self, direction):
        sprite_list = ["0"]
        if direction == "right":
            sprite_list = self.RIGHT
        else:
            sprite_list = self.LEFT

        self.animation = (self.animation + 1) % len(sprite_list)    
        self.sprite = PhotoImage(file=r"Sonic/" + sprite_list[self.animation] + ".png")
        self.canvas.itemconfig(self.sonic, image=self.sprite)
        self.canvas.update()

class Ring():
    def __init__(self, canvas, x):
        self.sprite = PhotoImage(file="Sonic/Rings/0.png")
        self.ring = canvas.create_image(x, 330, image=self.sprite)
        self.canvas = canvas

    def move(self, x):
        self.canvas.move(self.ring, x, 0)

    def pos(self):
        return self.canvas.coords(self.ring)

Game() # creates the game object
