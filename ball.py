from tkinter import *
from datetime import datetime
import random


window_height = 720
window_width = 1280

window = Tk()
window.resizable(0,0)
canvas = Canvas(window, width = window_width, height = window_height, borderwidth=0 ,highlightthickness=0, background="white")
objects= set()
bar = [0, 0]

class Game: 

    def __init__(self):
        self.keys = set() 
        global objects
        canvas.bind("<Button-1>", self.mousePress)
        window.bind("<KeyPress>", self.keyPressHandler)  
        window.bind("<KeyRelease>", self.keyReleaseHandler)
        bar[0] = canvas.create_rectangle(0,300,20,420, fill="blue")
        bar[1] = canvas.create_rectangle(1260,300,1280,420, fill="blue")
        canvas.pack()

        t_prev = datetime.now()
        while(True):    
            t_next = datetime.now()
            t_delta = (t_next - t_prev).total_seconds()
            
            self.move_bar(t_delta)
            for ball in objects:   
                ball.move(t_delta)

            t_prev = t_next
            window.update()

    def mousePress(self, event): 
        element(event.x, event.y)

    def keyPressHandler(self, event):
        self.keys.add(event.keycode)

    def move_bar(self, t_delta):
        move_leftbar_posY = 5 * t_delta * 20
        move_rightbar_posY = 5 * t_delta * 20

        for key in self.keys:
            if canvas.coords(bar[0])[1] < 0:
                canvas.delete(bar[0])
                bar[0] = canvas.create_rectangle(0,0,20,120, fill="blue")

            elif canvas.coords(bar[0])[3] > window_height:
                canvas.delete(bar[0])
                bar[0] = canvas.create_rectangle(0,window_height-120,20,window_height, fill="blue")

            if canvas.coords(bar[1])[1] < 0:
                canvas.delete(bar[1])
                bar[1] = canvas.create_rectangle(window_width-20,0,window_width,120, fill="blue")
            
            elif canvas.coords(bar[1])[3] > window_height:
                canvas.delete(bar[1])
                bar[1] = canvas.create_rectangle(window_width-20,window_height-120,window_width,window_height, fill="blue")

            if key == ord('W'):
                canvas.move(bar[0], 0, -move_leftbar_posY)
            elif key == ord('S'):
                canvas.move(bar[0], 0, move_leftbar_posY)

            if key == 38:
                canvas.move(bar[1], 0, -move_rightbar_posY)
            elif key == 40:
                canvas.move(bar[1], 0, move_rightbar_posY)

    def keyReleaseHandler(self, event):
        if event.keycode in self.keys: self.keys.remove(event.keycode)

class element:
    def __init__(self, x, y):
        self.r = random.randint(0,255)
        self.g = random.randint(0,255)
        self.b = random.randint(0,255)
        self.radius = 40
        self.posY = 0
        self.posX = 0
        self.status = 0 
        self.pos = [0,0,0,0]
        self.mass = 2
        self.velocity = 0
        
        if x + self.radius > window_width:
            x = window_width - self.radius
        elif x - self.radius < 0:
            x = self.radius

        if y + self.radius > window_height:
            y = window_height - self.radius
        elif y - self.radius < 0:
            y = self.radius

        self.canvas_id = canvas.create_oval(x - self.radius, y - self.radius, x + self.radius, y + self.radius, fill="#%02x%02x%02x" % (self.r, self.g, self.b), outline="black", width = 1)
        
        objects.add(self)

    def move(self, delta_time):
 
        self.velocity += 9.8 * delta_time
        self.posY += self.velocity * delta_time
        self.pos = canvas.coords(self.canvas_id)

        for ball in objects:
            crash, ball_id = self.collision(ball)
            if crash == True:
                ball_pos = canvas.coords(ball_id)

                if self.pos[2] - self.radius < ball_pos[2] - self.radius: 
                    self.posX = -abs(self.posY - ball.posY/self.mass)

                elif self.pos[2] - self.radius > ball_pos[2] - self.radius: 
                    self.posX = abs(self.posY - ball.posY/self.mass)

                if self.pos[3] - self.radius < ball_pos[3] - self.radius:  
                    self.posY = -abs(self.posX - ball.posX/self.mass)

                elif self.pos[3] - self.radius > ball_pos[3] - self.radius: 
                    self.posY = abs(self.posX - ball.posX/self.mass)
                
                elif self.pos[3] - self.radius == ball_pos[3] - self.radius:
                    self.posY *= -1

            else:
                pass

        for i in range(2):
            crash, bar_id = self.bar_collision(i)
            if crash == True:
                bar_pos = canvas.coords(bar_id)

                if self.pos[3] >= bar_pos[1] or self.pos[1] <= bar_pos[3]:
                    self.posY *= -1

                if self.pos[0] < bar_pos[2] or self.pos[2] > bar_pos[0]:
                    self.posX *= -1

                    if self.posX == 0 and self.pos[2] > bar_pos[0]:
                        self.posX = -1
                    elif self.posX == 0 and self.pos[0] < bar_pos[2]:
                        self.posX = 1

        self.posX *= 1 - self.mass * 0.0001

        if self.pos[3] >= window_height and self.status == 0:
            self.status = 1
            self.posY *= -1 + self.mass * 0.1

        elif self.posY > 0 and self.status == 1:
            self.status = 0
            self.posY *= -1

        elif self.pos[1] <= 0:
            self.posY *= -1

        if self.pos[0] < 0 or self.pos[2] > window_width:
            self.posX *= -1

        elif self.velocity <= 0.1 and self.status == 1:
            self.velocity = 0

        canvas.move(self.canvas_id, self.posX, self.posY) 

    def collision(self, obj):
        if canvas.coords(self.canvas_id)[0] <= canvas.coords(obj.canvas_id)[2] and canvas.coords(self.canvas_id)[2] >= canvas.coords(obj.canvas_id)[0] and canvas.coords(self.canvas_id)[1] <= canvas.coords(obj.canvas_id)[3] and canvas.coords(self.canvas_id)[3] >= canvas.coords(obj.canvas_id)[1] and self.canvas_id != obj.canvas_id: 
            return True, obj.canvas_id
        else:
            return False, 0

    def bar_collision(self, i):
        if canvas.coords(self.canvas_id)[0] <= canvas.coords(bar[i])[2] and canvas.coords(self.canvas_id)[2] >= canvas.coords(bar[i])[0] and canvas.coords(self.canvas_id)[1] <= canvas.coords(bar[i])[3] and canvas.coords(self.canvas_id)[3] >= canvas.coords(bar[i])[1]: 
            return True, bar[i]
        else:
            return False, 0

Game()
