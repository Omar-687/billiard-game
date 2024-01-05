import math
import tkinter
from tkinter import Tk, Label

MOVEMENT_STEP = 10
class Oval:
    def __init__(self, x, y, r, vx, vy):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.r = r
        self.m = 20

    def move(self, time_between_ticks, acceleration):
        self.vx = self.vx + acceleration * time_between_ticks
        self.vy = self.vy + acceleration * time_between_ticks
        self.x = self.x + self.vx * time_between_ticks
        self.y = self.y + self.vy * time_between_ticks



    def kresli(self, canvas):
        canvas.create_oval(self.x - self.r, self.y - self.r, self.x + self.r, self.y + self.r, outline="white", fill="purple")
        


class CollisionDetection:
    def __init__(self, objects):
        self.objects = objects
    def find_objects_in_collision(self):
        collisions = []
        for i in range(len(self.objects)):
            for j in range(i+1, len(self.objects)):
                first_ellipse = self.objects[i]
                second_ellipse = self.objects[j]
                info = self.find_collision(first_ellipse, second_ellipse)
                if info is None:
                    continue
                # print('info', info)
                print('Collision! With overlapping',20 - info.d)
                collisions.append([i, j, info])
##                if find_collision(self.objects[i],self.objects[j])
        print('Kolizie',len(collisions))
        return collisions
        
    def find_collision(self, o1, o2):
        dx = o2.x - o1.x
        dy = o2.y - o1.y
        d = math.sqrt(dx**2 + dy**2)
        if d < 20:
            info = Information(dx, dy, d)
            return info
        return None

class Information:
    def __init__(self, dx, dy, d):
        self.dx = dx
        self.dy = dy
        self.d = d

class CollisionSolution:
    def __init__(self, objects):
        self.objects = objects

    def solve_all_collisions(self, kolizie):
        for kolizia in kolizie:
            first_object_in_collision_idx = kolizia[0]
            second_object_in_collision_idx = kolizia[1]
            info = kolizia[2]
            self.solve_collision(self.objects[first_object_in_collision_idx], self.objects[second_object_in_collision_idx], info)
        return self.objects
    def solve_collision(self, o1, o2, info):
        nx = info.dx / info.d
        ny = info.dy / info.d
        s = 20 - info.d
        o1.x = o1.x - nx * s / 2
        o1.y = o1.y - ny * s / 2
        o2.x = o2.x + nx * s / 2
        o2.y = o2.y + ny * s / 2

        k = -2 * ((o2.vx - o1.vx) * nx + (o2.vy - o1.vy) * ny) / (1 / o1.m + 1 / o2.m)
        o1.vx = o1.vx - k * nx / o1.m
        o1.vy = o1.vy - k * ny / o1.m
        o2.vx = o2.vx + k * nx / o2.m
        o2.vy = o2.vy + k * ny / o2.m
        
class Scene:
    def __init__(self, root):

        self.root = root
        self.root.geometry(f'{WINDOW_WIDTH}x{WINDOW_HEIGHT}')
        self.root.title('Odtlacanie kruzkov')

        self.radius = 20
        GAME_WIDTH = 450
        GAME_HEIGHT = 450
        self.canvas = tkinter.Canvas(root, width=GAME_WIDTH, height=GAME_HEIGHT, bg='white')
        self.canvas.pack(anchor=tkinter.CENTER, expand=True)
        self.start_line_x = 0
        self.start_line_y = 0

        self.objects = []
        self.root.bind("<Key>", self.key_pressed)
        self.root.bind("<Left>", self.move_left)
        self.root.bind("<Right>", self.move_right)
        self.root.bind("<Up>", self.move_up)
        self.root.bind("<Down>", self.move_down)
        self.root.bind("<Button-1>", self.on_click)
        self.root.bind("<Button-3>", self.on_click)
        self.canvas.bind("<B1-Motion>", self.on_left_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_left_release)
        self.canvas.bind("<ButtonRelease-3>", self.on_right_release)
    def on_right_release(self, event):
        print('On right release')
        self.canvas.delete('line')
        self.objects[self.selected_i].vx = 10
        self.objects[self.selected_i].vy = 10
    def on_left_drag(self, event):
        self.canvas.delete('line')
        self.canvas.create_line(self.start_line_x, self.start_line_y, event.x, event.y, fill='blue',tags='line')
        print(event.x,event.y, sep=',')
    def on_left_release(self, event):
        print('release')


    def create_new_cell(self, x, y):
        oval = Oval(x, y, self.radius,0,0)
        self.objects.append(oval)
        oval.kresli(self.canvas)

    def select_cell(self, x, y):
        print('ok')
        for i in range(len(self.objects)):
            ellipse = self.objects[i]
            if self.is_point_inside_ellipse(x=x,y=y,a=ellipse.x,b=ellipse.y):
                self.start_line_x = ellipse.x
                self.start_line_y = ellipse.y
                break

    def is_point_inside_ellipse(self,x, y, a, b):
        # Calculate the left-hand side of the ellipse equation
        lhs = ((a - x) **2 / self.radius**2) + ((b - y) **2 / self.radius**2)

        # Compare LHS to 1
        if lhs < 1:
            return True  # The point is inside the ellipse
        elif lhs == 1:
            return True  # The point is on the ellipse
        else:
            return False  # The point is outside the ellipse

    def on_click(self,event):
        if event.num == 1:
            self.select_cell(x=event.x,y=event.y)
        # Get the x and y coordinates of the mouse click
        if event.num == 3:
            self.create_new_cell(x=event.x,y=event.y)
            # points = (x - self.radius, y - self.radius, x + self.radius, y + self.radius)
            # self.objects.append(self.canvas.create_oval(*points, outline="white", fill="purple"))
            print("Left mouse button clicked at ({}, {})".format(event.x, event.y))

    def tick(self):
        self.canvas.delete("all")  # Clear the entire canvas
        print('Updated objects ', len(self.objects))
        acceleration = 1
        time_between_ticks = 0.02
        for ellipse in self.objects:
            ellipse.move(time_between_ticks=time_between_ticks ,acceleration=acceleration)
            ellipse.kresli(self.canvas)
        d = CollisionDetection(self.objects)
        collisions = d.find_objects_in_collision()

        r = CollisionSolution(self.objects)
        r.solve_all_collisions(collisions)
    def key_pressed(self, event):
        print('clicked key')
    def move_left(self, event):
        self.canvas.move(self.arr_obj[0], -MOVEMENT_STEP, 0)
    def move_right(self, event):
        self.canvas.move(self.arr_obj[0], MOVEMENT_STEP, 0)
    def move_up(self, event):
        self.canvas.move(self.arr_obj[0], 0, -MOVEMENT_STEP)
    def move_down(self, event):
        self.canvas.move(self.arr_obj[0], 0, MOVEMENT_STEP)

WINDOW_WIDTH = 500
WINDOW_HEIGHT = 500

root = Tk()
inst = Scene(root)
def my_timer_tick():
    print('Tu som!')
    inst.tick()
    
    root.after(20,my_timer_tick)

root.after(20,my_timer_tick())

root.mainloop()  # This line starts the Tkinter main loop






