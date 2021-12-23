"""
SpotifyApp index (main) view.
"""
import flask
import spotifyapp

@spotifyapp.app.route('/')
def show_index():

    logged_in = True
    if 'username' not in flask.session:
        logged_in = False

    # Connect to database:
    connection = spotifyapp.model.get_db()

    # gather necessary info:


    context = {
        "logged_in": logged_in,
    }
    return flask.render_template("index.html", **context)