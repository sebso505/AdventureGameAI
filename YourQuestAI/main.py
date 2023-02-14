
import flask
from flask import request

# Create the application.
APP = flask.Flask(__name__)

promptName = ''
promptStory = ''

@APP.route('/')
def index():
    """ Displays the index page accessible at '/'
    """
    return flask.render_template('index.html', name='Sebi')

@APP.route('/' , methods=['POST'])
def add():
    global promptName;
    global promptStory;
    if request.method == 'POST':
        promptName += request.form.get('variableName')
        promptStory += request.form.get('variableStory')
        print(promptName)
        print(promptStory)
        return flask.render_template('index.html', name="Cristian Maestrul Codului")





if __name__ == '__main__':
    APP.debug=True
    APP.run()

    #changes 21:49

    #Changes 6:39

