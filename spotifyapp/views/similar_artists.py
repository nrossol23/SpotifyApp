"""
SpotifyApp similar artists view.
"""
import flask
import spotifyapp

@spotifyapp.app.route('/similar_artists/')
def show_similar_artists():

    # Perform auth check

    context = {

    }
    
    return flask.render_template("similar_artists.html", **context)