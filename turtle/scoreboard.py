from turtle import Turtle, Screen

FONT = ("Courier", 24, "normal")
ALIGNMENT = "center"


class Scoreboard(Turtle):
    def __init__(self):
        super().__init__()
        self.score = 0
        self.color("black")
        self.penup()
        self.goto(0, 270)
        self.score = 0
        self.hideturtle()
        self.update_scoreboard()

    def update_scoreboard(self):
        self.clear()
        self.goto(0, 270)
        self.write(self.score, align=ALIGNMENT, font=FONT)

    def point(self):
        self.score += 1
        self.update_scoreboard()

    def game_over(self):
        self.goto(0, 0)
        self.write(f"GAME OVER, Score: {self.score}" , align=ALIGNMENT, font=FONT)


    def reset_score(self):
        self.score = 0
        self.update_scoreboard()

