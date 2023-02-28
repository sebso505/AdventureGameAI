import flask
from flask import request
import openai
import random
import openai
import os
import requests  # to get image from the web
import shutil  # to save it locally

openai.api_key = "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"

# Create the application.
APP = flask.Flask(__name__)


promptName = ''
promptStory = ''
currentSummary = ''
currentChoice = ''
currentStep = 0
bad_choice = ''
game_on = True
allImgDir = "YourQuestAIImages"
projectDir = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Documents\GitHub\AdventureGameAI\YourQuestAI\static')
imageDir = os.path.join(projectDir, allImgDir)
folderNo = ''
game = 'Book/Videogame...'
name = 'Your name...'
print(imageDir)


def makeDIRforDALLE():
    if not folderNo:
        if not os.path.exists(os.path.join(projectDir, allImgDir)):
            print("nu exista, creez")
            os.makedirs(os.path.join(projectDir, allImgDir))
            os.makedirs(os.path.join(imageDir, 'Game1'))
            numberWeShouldUse = 1
            print(f'from 1 {numberWeShouldUse}')
        else:
            dir_list = os.listdir(os.path.join(projectDir, allImgDir))
            dir_names = [name for name in dir_list if os.path.isdir(os.path.join(os.path.join(projectDir, allImgDir), name))]
            print(dir_names)
            dirNumber = len(dir_names)
            lastIteminDirnames = dir_names[dirNumber - 1]
            numberWeShouldUse = lastIteminDirnames.replace('Game', '')
            numberWeShouldUse= int(numberWeShouldUse) + 1
            os.makedirs(os.path.join(imageDir, 'Game' + str(numberWeShouldUse)))
            print(f'from 2 {numberWeShouldUse}')
        return numberWeShouldUse

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
        self.image = ''
        self.visual = ''

    def update_params(self, currentSummary, currentChoice, currentStep):
        self.currentSummary = currentSummary
        self.currentChoice = currentChoice
        self.currentStep = currentStep

    def plot_of_game(self, ):
        if not game_on:
            self.prompt = f"{self.robot_act}We are in the world of {self.book}.Based on {self.currentSummary}  and the fact that this choice was picked {self.currentChoice} create an ending for the story, where {self.name} is defeated tragically, 2 or 3 sentences long."
        elif currentStep == 0:
            self.prompt = f"{self.robot_act}We are in the world of {self.book}.Based on the book or game: {self.book} and create an intro, 5 sentences long, in which you introduce me, {self.name}, the main character , in the game. You narrate this intro about me."
        elif currentStep == 8:
            self.prompt = f"{self.robot_act}We are in the world of {self.book}.Based on {self.currentSummary}  and the fact that this choice was picked {self.currentChoice} create a story that is nearing its conclusion, 2 or 3 sentences long."
        elif currentStep == 9:
            self.prompt = f"{self.robot_act}We are in the world of {self.book}.Based on {self.currentSummary}  and the fact that this choice was picked {self.currentChoice} create a cliffhanger for the story, 2 or 3 sentences long."
        elif currentStep == 10:
            self.prompt = f"{self.robot_act}We are in the world of {self.book}.Based on {self.currentSummary}  and the fact that this choice was picked {self.currentChoice} create an ending for the story, where {self.name} emerges victorious, 2 or 3 sentences long."
        else:
            self.prompt = f"{self.robot_act} We are in the world of {self.book}. Based on {self.currentSummary} and the fact that this choice was picked {self.currentChoice}, create the story, 2 or 3 sentences long"
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
            prompt=f"{self.robot_act} Reading this plot {self.plot} generate 3 choices, each on a new line, dont note them with numbers, from which I should choose to continue the game. It is a must that you make one of the choices bad. Also, at the end of the bad one, write the character ~, but for the other choices, dont write anything after them.",
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
        random.shuffle(self.final_choice)
        return self.final_choice
    def createVisualDesc(self):
        self.visual = openai.Completion.create(
            engine="text-davinci-003",
            prompt=f"Reading this plot: {self.summary} generate a visual description, 2 sentences long. Keep in mind that i will use this to generate an image with DALL-E",
            max_tokens=300,
            n=1,
            stop=None,
            temperature=0.8,
        ).get("choices")[0].text
        print(f"The visual desc is: {self.visual}")
        return self.visual

    def generateImage(self):
        self.image = openai.Image.create(
            prompt=f"A gorgeous  digital illustration of {self.visual}, detailed, trending in artstation, fantasy, mesmerizing, captivating",
            n=2,
            size="512x512"
        ).get("data")[0].url
        image_url = self.image
        print (self.image)
        print(f"NUMARUL ESTE {folderNo}")
        filename = imageDir+"/Game"+str(folderNo) +"/image"+str(currentStep+1)+".jpg"
        imageTrueLocation = filename.replace('\\', '/')
        self.imageName="static/YourQuestAIImages/Game"+str(folderNo) +"/image"+str(currentStep+1)+".jpg"
        print(self.imageName)
        # Open the url image, set stream to True, this will return the stream content.
        r = requests.get(image_url, stream=True)

        # Check if the image was retrieved successfully
        if r.status_code == 200:
            # Set decode_content value to True, otherwise the downloaded image file's size will be zero.
            r.raw.decode_content = True

            # Open a local file with wb ( write binary ) permission.
            with open(imageTrueLocation, 'wb') as f:
                shutil.copyfileobj(r.raw, f)

            print('Image sucessfully Downloaded: ', imageTrueLocation)
        else:
            print('Image Couldn\'t be retreived')

        return self.imageName

class genRandom:
    def __init__(self):
        self.name = ''
        self.game = ''
    def getRandomName(self):
        self.name = openai.Completion.create(
            engine="text-davinci-003",
            prompt="Give me a random Character Name",
            max_tokens=350,
            n=1,
            stop=None,
            temperature=0.8,
        ).get("choices")[0].text
        print(f'Random name is {self.name}')
        return self.name
    def getRandomGame(self):
        self.game = openai.Completion.create(
            engine="text-davinci-003",
            prompt="Give me a random Book or Game or Movie. Only the name should be returned",
            max_tokens=350,
            n=1,
            stop=None,
            temperature=1,
        ).get("choices")[0].text
        print(f'Random game is {self.game}')
        return self.game

@APP.route('/')
def index():
    """ Displays the index page accessible at '/'
    """
    return flask.render_template('introPage.html', name='Your name...', game='Book/Videogame...')

@APP.route('/', methods=['POST'])
def add():
    global promptName
    global promptStory
    global currentSummary
    global currentChoice
    global currentStep
    global game_on
    global bad_choice
    global getLastNumberinLastItem
    global folderNo
    global game
    global name
    print(folderNo)
    print(f'game status {game_on}')
    if request.method == 'POST':
        if currentStep == 0:
            # generated = genRandom()
            # if request.form["button"] == "randomName":
            #     name = generated.getRandomName()
            #     return flask.render_template('introPage.html', name=name, game=game)
            # elif request.form["button"] == "randomGame":
            #     game = generated.getRandomGame()
            #     return flask.render_template('introPage.html', name=name, game=game)
            promptName = request.form.get('variableName')
            promptStory = request.form.get('variableStory')
            print(promptName)
            print(promptStory)
            folderNo = makeDIRforDALLE()
        else:
            currentChoice = request.values.get('choice')
            if currentChoice == bad_choice:
                game_on = False
                print(f'game status {game_on}')
                print(currentChoice)
        game = talkingRobot(promptName, promptStory, currentSummary, currentChoice, currentStep)
        if currentStep < 10 and game_on:
            game.update_params(currentSummary, currentChoice, currentStep)
            plot = game.plot_of_game()
            currentSummary = game.summary_of_plot()
            game.createVisualDesc()
            imageGen = game.generateImage()
            game.choices_robot()
            choices = game.choices_separated()
            print(f'Alegeri in if {choices}')
            for i, choice in enumerate(choices):
                if '~' in choice:
                    choices[i] = choice.replace('~', '')
                    bad_choice = choices[i]
            currentStep += 1
            print(f'Pasul curent {currentStep}')
            print(f'Alegere Gresita {bad_choice}')
            return flask.render_template('GameTab.html', plot=plot, choice1=choices[0], choice2=choices[1], choice3 = choices[2], bad_choice=bad_choice, image=imageGen)
        elif currentStep == 10:
            game.update_params(currentSummary, currentChoice, currentStep)
            plot = game.plot_of_game()
            currentSummary = game.summary_of_plot()
            game.createVisualDesc()
            imageGen = game.generateImage()
            currentStep += 1
            if game_on:
                return flask.render_template('GoodEnd.html', plot=plot,image=imageGen)
            else:
                return flask.render_template('BadEnd.html', plot=plot)
        elif currentStep == 11:
            promptName = ''
            promptStory = ''
            currentSummary = ''
            currentChoice = ''
            currentStep = 0
            bad_choice = ''
            game_on = True
            allImgDir = "YourQuestAIImages"
            projectDir = os.path.join(os.path.join(os.environ['USERPROFILE']),
                                      'Documents\GitHub\AdventureGameAI\YourQuestAI\static')
            imageDir = os.path.join(projectDir, allImgDir)
            folderNo = ''
            print(imageDir)
            return flask.render_template('introPage.html')


if __name__ == '__main__':
    APP.debug = True
    APP.run()
