import math
import tkinter
from tkinter import Tk, Label

MOVEMENT_STEP = 10


class Oval:
    def __init__(self, x, y, r, vx, vy, color):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.r = r
        self.m = 20
        self.color = color

    def move(self, time_between_ticks, acceleration):
        # self.vx = self.vx + acceleration * time_between_ticks
        # self.vy = self.vy + acceleration * time_between_ticks
        self.x = self.x + self.vx * time_between_ticks
        self.y = self.y + self.vy * time_between_ticks

    def kresli(self, canvas):
        canvas.create_oval(self.x - self.r, self.y - self.r, self.x + self.r, self.y + self.r, outline="white",
                           fill=self.color)


class CollisionDetection:
    def __init__(self, objects):
        self.objects = objects

    def find_objects_in_collision(self):
        collisions = []
        for i in range(len(self.objects)):
            for j in range(i + 1, len(self.objects)):
                first_ellipse = self.objects[i]
                second_ellipse = self.objects[j]
                info = self.find_collision(first_ellipse, second_ellipse)
                if info is None:
                    continue
                # print('info', info)
                # print('Collision! With overlapping', 20 - info.d)
                collisions.append([i, j, info])
        ##                if find_collision(self.objects[i],self.objects[j])
        # print('Kolizie', len(collisions))
        return collisions

    def find_collision(self, o1, o2):
        dx = o2.x - o1.x
        dy = o2.y - o1.y
        d = math.sqrt(dx ** 2 + dy ** 2)
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
            self.solve_collision(self.objects[first_object_in_collision_idx],
                                 self.objects[second_object_in_collision_idx], info)
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


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Scene:
    def __init__(self, root):

        self.root = root
        self.root.geometry(f'{WINDOW_WIDTH}x{WINDOW_HEIGHT}')
        self.root.title('Billiard')
        GAME_WIDTH = 700
        GAME_HEIGHT = 450
        self.radius = 10
        self.shoot_event_occured = False
        self.objects = []
        self.canvas = tkinter.Canvas(root, width=GAME_WIDTH, height=GAME_HEIGHT, bg='white')
        self.main_ball = Oval(x=200, y=200, r=self.radius, vx=0, vy=0,color='red')
        self.main_ball.kresli(self.canvas)
        self.objects.append(self.main_ball)
        self.create_billiard()
        self.canvas.pack(anchor=tkinter.CENTER, expand=True)
        self.root.bind("<Button-1>", self.on_click)
        self.canvas.bind("<B1-Motion>", self.on_left_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_left_release)
    def on_click(self, event):
        ...
    def on_left_drag(self, event):
        self.canvas.delete('line')
        self.canvas.create_line(event.x, event.y, self.main_ball.x, self.main_ball.y, tags='line', width=2)

    def dist(self, p1: Point, p2: Point):
        return math.sqrt((p1.x - p2.x) ** 2 + (p1.y - p2.y)**2)
    def on_left_release(self, event):
        if self.shoot_event_occured == False:
            self.canvas.delete('line')
            # print(f'Release eventx = {event.x}, eventy = {event.y}')
            # print(f'Ball x = {self.main_ball.x}, y = {self.main_ball.y}')
            # print('cos = ',math.cos(self.main_ball.x - event.x))
            # print('sin = ', math.sin(self.main_ball.y - event.y))
            p1 = Point(x=event.x, y=event.y)
            p2 = Point(x=self.main_ball.x,y=self.main_ball.y)
            distance = self.dist(p1, p2)
            delta_y = self.main_ball.y - event.y
            delta_x = self.main_ball.x - event.x
            angle = math.atan2(delta_y, delta_x)
            self.main_ball.vx = math.cos(angle) * distance
            self.main_ball.vy = math.sin(angle) * distance
            self.shoot_event_occured = True
        else:
            self.canvas.delete('line')
            print('Restart game to shoot a ball again!')
    def create_billiard(self):
        num_of_balls = 0
        start_x = 400
        start_y = 200
        for i in range(5):
            num_of_balls += 1
            start_x += i * 2 * self.radius
            new_start_y = start_y - num_of_balls * self.radius
            for j in range(num_of_balls):
                ov = Oval(x=start_x, y=new_start_y, r=self.radius, vx=0, vy=0, color='black')
                ov.kresli(canvas=self.canvas)
                self.objects.append(ov)
                # self.canvas.create_oval(start_x - self.radius, new_start_y - self.radius, start_x + self.radius, new_start_y + self.radius, outline="white", fill="black")
                new_start_y += self.radius * 2
            start_x = 400
    def tick(self):
        self.canvas.delete('all')
        acceleration = 1
        time_between_ticks = 0.02
        for ellipse in self.objects:
            ellipse.move(time_between_ticks=time_between_ticks, acceleration=acceleration)
            ellipse.kresli(self.canvas)
        d = CollisionDetection(self.objects)
        collisions = d.find_objects_in_collision()

        r = CollisionSolution(self.objects)
        r.solve_all_collisions(collisions)

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 500

root = Tk()
inst = Scene(root)
# inst.create_billiard()

def my_timer_tick():
    # print('Tu som!')
    inst.tick()
    root.after(20, my_timer_tick)


root.after(20, my_timer_tick())

root.mainloop()  # This line starts the Tkinter main loop