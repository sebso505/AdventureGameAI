
import flask
from flask import request

# Create the application.
APP = flask.Flask(__name__)

promptName = ''
promptStory = ''
currentSummary = ''
currentChoice = ''
currentStep = 0
game_on = True
class Talking_Robot():

    def __init__(self, promptName, promptStory, currentSummary, currentChoice, currentStep):
        self.name = promptName
        self.book = promptStory
        self.robot_act = f"I want you to act as if you are a classic text adventure game and we are playing. I don’t want you to ever break out of your character, and you must not refer to yourself in any way."
        self.game_on = False
        self.count = 0
        self.currentSummary = currentSummary
        self.currentChoice = currentChoice
        self.currentStep = currentStep
        self.prompt = ''

    def update_params(self, currentSummary, currentChoice, currentStep):
        self.currentSummary = currentSummary
        self.currentChoice = currentChoice
        self.currentStep = currentStep

    def plot_of_game(self, ):
        if currentStep == 0:
            self.prompt = f"{self.robot_act}Based on the book: {self.book} create an intro, 5 sentences long, in which you introduce me, {self.name}, the main character , in the game. You narrate this intro about me."
        elif currentStep == 8:
            self.prompt = f"{self.robot_act}Based on {self.currentSummary} and the fact that this choice was picked {self.currentChoice} create a story that is nearing its conclusion, 2 or 3 sentences long."
        elif currentStep == 9:
            self.prompt = f"{self.robot_act}Based on {self.currentSummary} and the fact that this choice was picked {self.currentChoice} create an ending for the story, 2 or 3 sentences long."
        elif currentStep == 10:
            if game_on:
                self.prompt = f"{self.robot_act}Based on {self.currentSummary} and the fact that this choice was picked {self.currentChoice} create an ending for the story, where {self.name} emerges victorious, 2 or 3 sentences long."
            else:
                self.prompt = f"{self.robot_act}Based on {self.currentSummary} and the fact that this choice was picked {self.currentChoice} create an ending for the story, where {self.name} is defeated tragically, 2 or 3 sentences long."
        else:
            self.prompt = f"{self.robot_act}Based on {self.currentSummary} and the fact that this choice was picked {self.currentChoice} create a plot, 2 or 3 sentences long"
        self.plot = "Test Self Plot"
        print(f'The plot is:{self.plot} What is your choice, {self.name}?')
        return self.plot

    def summary_of_plot(self):
        self.summary = "Test Self Summary"
        print(f"The summary is: {self.summary}")
        print("End of summary")
        return self.summary

    def choices_robot(self):
        self.choices = "Test choice 1\nTest choice2\nTest choice3~"
        print(f"The choices are: {self.choices}")
        return self.choices

    def choices_separated(self):
        self.options = []
        self.options = self.choices.split("\n")
        self.final_choice = [self.options[2], self.options[3], self.options[4]]
        return self.final_choice

game = Talking_Robot(promptName, promptStory, currentSummary, currentChoice, currentStep)

@APP.route('/')
def index():
    """ Displays the index page accessible at '/'
    """
    return flask.render_template('introPage.html', name='Sebi')

@APP.route('/GameTab' , methods=['POST'])
def add():
    global promptName
    global promptStory
    global currentSummary
    global currentChoice
    global currentStep
    global game_on
    if request.method == 'POST':
        promptName += request.form.get('variableName')
        promptStory += request.form.get('variableStory')
        print(promptName)
        print(promptStory)
        game.update_params(currentSummary, currentChoice, currentStep)
        plot = game.plot_of_game()
        currentSummary = game.summary_of_plot()
        game.choices_robot()
        bad_choice = ''
        choices = game.choices_separated()
        i = 0
        for i, choice in enumerate(choices):
            if '~' in choice:
                choices[i] = choice.replace('~', '')
                bad_choice = choices[i]
            i += 1
        currentStep += 1
        choices.clear()
        return flask.render_template('GameTab.html')


@APP.route('/GameTab', methods=['POST'])
def add():
    global promptName
    global promptStory
    global currentSummary
    global currentChoice
    global currentStep
    global game_on
    if request.method == 'POST':
        currentChoice += request.form.get('choiceSelected')
        promptStory += request.form.get('variableStory')
        print(promptName)
        print(promptStory)
        if game_on == True:
            while currentStep < 10 and game_on:
                game.update_params(currentSummary, currentChoice, currentStep)
                plot=game.plot_of_game()
                currentSummary = game.summary_of_plot()
                game.choices_robot()
                bad_choice = ''
                choices = game.choices_separated()
                i = 0
                for i, choice in enumerate(choices):
                    if '~' in choice:
                        choices[i] = choice.replace('~', '')
                        bad_choice = choices[i]
                    i += 1
                if currentChoice == bad_choice or currentStep == 10:
                    plot = game.plot_of_game()
                    game_on = False
                currentStep += 1
                choices.clear()
                return flask.render_template('GameTab.html')


if __name__ == '__main__':
    APP.debug=True
    APP.run()

    #changes 21:49

    #Changes 6:39

