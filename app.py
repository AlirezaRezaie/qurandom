from flask import Flask, render_template
from random_verse import get_random_verse
import logging
import os

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)



app = Flask(__name__)

@app.route('/')
def index():
    # Fetch the verse from a remote resource
    verse,info = get_random_verse()
    
    # Render the HTML template with the verse as a variable
    return render_template('verse.html', verse=verse,info=info)

if __name__ == '__main__':
    from waitress import serve
    host,port = "0.0.0.0",8080
    logger.info(f"Started server process [{os.getpid()}]")
    serve(app, host=host, port=port)
