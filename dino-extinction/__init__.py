from flask import Flask

app = Flask(__name__)

from dino-extinction import routes
