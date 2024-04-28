# main.py
import time
import random
from turtle import Screen, Turtle
from player import Player
from car_manager import CarManager, CarController
from scoreboard import Scoreboard

def reset_game():
    global game_is_on
    player.reset_player()
    car_controller.reset_cars()
    scoreboard.reset_score()
    game_is_on = True

    # Reset all components
    player.reset_player()
    car_controller.reset_cars()  # Corrected method name
    scoreboard.reset_score()
    game_is_on = True

screen = Screen()
screen.setup(width=600, height=600)
screen.tracer(0)

player = Player()
car_controller = CarController()
scoreboard = Scoreboard()

screen.listen()
screen.onkey(player.go_up, "Up")
screen.onkey(reset_game, "space")

game_is_on = True
while game_is_on:
    time.sleep(0.1)
    screen.update()
    car_controller.move_cars()
    car_controller.update()

    # Create cars randomly
    if random.randint(1, 6) == 1:
        car_controller.create_car()

    # Detect collision with cars
    for car in car_controller.cars:
        if player.distance(car) < 20:
            scoreboard.game_over()
            game_is_on = False  # Set the game_over_flag to True
            break

        # Detect turtle collision with wall
    if player.ycor() > 280:
        player.reset_player()
        scoreboard.point()
        car_controller.increase_speed()

screen.onkey(reset_game, "space")

screen.exitonclick()