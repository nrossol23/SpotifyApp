"""
SpotifyApp stats view.
"""
import flask
import spotifyapp
import datetime

@spotifyapp.app.route('/stats/')
def show_stats():

    # Determine if the user is authorized:
    if 'header' not in flask.session:
        context = {
            "authorized": False,
        }
        return flask.render_template("stats.html", **context)

    # Perform access token check if user is authorized:
    if (datetime.datetime.now(datetime.timezone.utc) - flask.session["time_authorized"]).total_seconds() >= 3540:
        return flask.redirect("/authorize/")

    context = {
        "authorized": True,
    }
    
    return flask.render_template("stats.html", **context)