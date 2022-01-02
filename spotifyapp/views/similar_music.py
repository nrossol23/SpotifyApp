"""
SpotifyApp similar music view.
"""
import flask
import spotifyapp

@spotifyapp.app.route('/similar_music/')
def show_similar_music():

    # Perform auth check

    context = {

    }
    
    return flask.render_template("similar_music.html", **context)