from turtle import Turtle
import random
import time
COLORS = ["red", "orange", "yellow", "green", "blue", "purple"]
STARTING_MOVE_DISTANCE = 5
MOVE_INCREMENT = 10
STARTING_POSITION = [(280, 40), (280, 80), (280, 120), (280, 160), (280, 200), (280, 240), (280, 280)]


class CarManager(Turtle):
    def __init__(self):
        super().__init__()
        self.shape("square")
        self.color(random.choice(COLORS))
        self.shapesize(stretch_wid=1, stretch_len=4)
        self.penup()
        self.random_y = random.randint(-200, 280)
        self.goto(280, self.random_y)
        self.x_move = -STARTING_MOVE_DISTANCE
        self.move_speed = 0.1

    def move(self):
        new_x = self.xcor() + self.x_move
        self.goto(new_x, self.random_y)

class CarController(Turtle):
    def __init__(self):
        self.move_speed = None
        self.cars = []
        self.car_generation_delay = 10  # Set the delay between car generations

    def create_car(self):
        new_car = CarManager()
        self.cars.append(new_car)

    def move_cars(self):
        for car in self.cars:
            car.move()

    def update(self):
        # Introduce a delay between car generations
        if time.time() % self.car_generation_delay < 0.1:  # Adjust the threshold as needed
            self.create_car()

    def increase_speed(self):
        for car in self.cars:
            car.move_speed += 0.01

    def reset_speed(self):
        self.move_speed = 0.1

    def reset_cars(self):
        for car in self.cars:
            car.goto(300, random.randint(-200, 280))
        self.reset_speed()
            