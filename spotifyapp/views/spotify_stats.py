"""
SpotifyApp stats view.
"""
import flask
import spotifyapp

@spotifyapp.app.route('/stats/')
def show_stats():

    # Perform auth check

    context = {

    }
    
    return flask.render_template("stats.html", **context)