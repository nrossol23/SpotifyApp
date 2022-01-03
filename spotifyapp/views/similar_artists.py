"""
SpotifyApp similar artists view.
"""
import flask
import spotifyapp
import datetime

@spotifyapp.app.route('/similar_artists/')
def show_similar_artists():

    # Determine if the user is authorized:
    if 'header' not in flask.session:
        context = {
            "authorized": False,
            "expired": False,
        }
        return flask.render_template("similar_artists.html", **context)

    context = {
        "authorized": True,
        "expired": False,
    }

    # Perform access token check if user is authorized:
    if (datetime.datetime.now(datetime.timezone.utc) - flask.session["time_authorized"]).total_seconds() >= 3540:
        context["expired"] = True
        
    return flask.render_template("similar_artists.html", **context)