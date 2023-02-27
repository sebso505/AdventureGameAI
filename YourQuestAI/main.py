import flask
from flask import request
import openai

openai.api_key = "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"

# Create the application.
APP = flask.Flask(__name__)

promptName = ''
promptStory = ''
currentSummary = ''
currentChoice = ''
currentStep = 0
game_on = True

class talkingRobot:
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
        self.plot = openai.Completion.create(
            engine="text-davinci-003",
            prompt=self.prompt,
            max_tokens=1000,
            n=1,
            stop=None,
            temperature=0.9,
        ).get("choices")[0].text
        print(f'The plot is:{self.plot} What is your choice, {self.name}?')
        return self.plot

    def summary_of_plot(self):
        self.summary = openai.Completion.create(
            engine="text-davinci-003",
            prompt=f"{self.robot_act} Create a summary for this plot: {self.plot}, max 2 or 3 sentences",
            max_tokens=350,
            n=1,
            stop=None,
            temperature=0.8,
        ).get("choices")[0].text
        print(f"The summary is: {self.summary}")
        print("End of summary")
        return self.summary

    def choices_robot(self):
        self.choices = openai.Completion.create(
            engine="text-davinci-003",
            prompt=f"{self.robot_act} Reading this plot: {self.plot} generate 3 choices, each one on a new line of text, noted 1. through 3. from which I should choose to continue the game. It is a must that you make one of the choices bad. Also, at the end of the bad one, write the character ~, but for the other choices, dont write anything after them.",
            max_tokens=300,
            n=1,
            stop=None,
            temperature=0.8,
        ).get("choices")[0].text
        print(f"The choices are: {self.choices}")
        return self.choices

    def choices_separated(self):
        self.options = []
        self.options = self.choices.split("\n")
        print(self.options)
        self.final_choice = [self.options[2], self.options[3], self.options[4]]
        return self.final_choice

@APP.route('/')
def index():
    """ Displays the index page accessible at '/'
    """
    return flask.render_template('introPage.html', name='Sebi')

@APP.route('/', methods=['POST'])
def add1():
    global promptName
    global promptStory
    global currentSummary
    global currentChoice
    global currentStep
    global game_on
    if request.method == 'POST':
        if currentStep == 0:
            promptName = request.form.get('variableName')
            promptStory = request.form.get('variableStory')
        else:
            currentChoice = request.values.get('choice')
            print(currentChoice)
        game = talkingRobot(promptName, promptStory, currentSummary, currentChoice, currentStep)
        if currentStep < 10 and game_on:
            game.update_params(currentSummary, currentChoice, currentStep)
            plot = game.plot_of_game()
            currentSummary = game.summary_of_plot()
            game.choices_robot()
            bad_choice = ''
            choices = game.choices_separated()
            print(f'Alegeri in if {choices}')
            for i, choice in enumerate(choices):
                if '~' in choice:
                    choices[i] = choice.replace('~', '')
                    bad_choice = choices[i]
            currentStep += 1
            print(currentStep)
            return flask.render_template('GameTab.html', plot=plot, choice1=choices[0], choice2=choices[1], choice3=choices[2], bad_choice=bad_choice)


if __name__ == '__main__':
    APP.debug = True
    APP.run()
