"""SpotifyApp Package Initializer"""
import flask

app = flask.Flask(__name__)

app.config.from_object('spotifyapp.config')

import spotifyapp.views
import spotifyapp.model
import spotifyapp.api