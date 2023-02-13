

from flask import render_template, Flask
# Create the application.
APP = Flask(__name__)


@APP.route('/')
def index():
    """ Displays the index page accessible at '/'
    """
    return render_template('index.html', name='Radu')



if __name__ == '__main__':
    APP.debug=True
    APP.run()
    APP.run(host='0.0.0.0')
    #changes 21:49

    #Changes 6:39