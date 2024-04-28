import turtle
import pandas
import csv
screen = turtle.Screen()
screen.title("U.S States Game")
image = "blank_states_img.gif"
screen.addshape(image)
turtle.shape(image)

data = pandas.read_csv("50_states.csv") #imports the data from the csv file 50 states
all_states = data.state.to_list() # creates a list of states names from the data (50 states csv)
guessed_states = []

while len(guessed_states)< 50:
    answer_state = screen.textinput(title=f"Guess the State {len(guessed_states)}/50", prompt = "Names a state").title()
    print(answer_state)
    if answer_state == "Exit":
        missing_states = [state for state in all_states if state not in guessed_states]
        new_data = pandas.DataFrame(missing_states)
        new_data.to_csv("states_to_learn.csv")
        break
    if answer_state in all_states: # checks in the user inputs answer against the list of all states in all_sattes list
        guessed_states.append(answer_state)
        t = turtle.Turtle()
        t.penup()
        t.hideturtle()
        state_data = data[data.state == answer_state] # creates a new variable if the answer is correct. Does this by
        # opening data (data) then in data checking each row in the state column (data.state) matches the answer
        # input(answer state). It then pulls ou tthe entire data row and stores it as state_data
        t.goto(int(state_data.x), int(state_data.y)) # retriets the x and Y data from state_data
        # alternative option is t.write(state_data.state.item())
        t.write(answer_state)


## alternative method to create csv file of missing states by merging and deleting all duplicates
# guessed_states_df = pandas.DataFrame(guessed_states)
# all_states_df = pandas.DataFrame(all_states)
# merged_df = pandas.merge(all_states_df, guessed_states_df, indicator=True, how='outer').query('_merge == "left_only"').drop('_merge', axis=1)
#merged_df.to_csv("states_to_learn.csv")
screen.exitonclick()