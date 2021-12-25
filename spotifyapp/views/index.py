"""
SpotifyApp index (main) view.
"""
import flask
import spotifyapp

@spotifyapp.app.route('/')
def show_index():

    authorized = True
    if 'header' not in flask.session:
        authorized = False

    # Connect to database:
    connection = spotifyapp.model.get_db()

    # gather necessary info:
    # TO DO

    context = {
        "authorized": authorized,
    }
    return flask.render_template("index.html", **context)