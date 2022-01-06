"""
SpotifyApp stats view.
"""
import flask
import spotifyapp
import datetime
import requests

@spotifyapp.app.route('/stats/')
def show_stats():

    # Determine if the user is authorized:
    if 'header' not in flask.session:
        context = {
            "authorized": False,
            "expired": False,
        }
        return flask.render_template("stats.html", **context)

    context = {
        "authorized": True,
        "expired": False,
    }

    # Perform access token check if user is authorized:
    if (datetime.datetime.now(datetime.timezone.utc) - flask.session["time_authorized"]).total_seconds() >= 3540:
        context["expired"] = True
        return flask.render_template("stats.html", **context)

    # Gather all info through Spotify's API:
    get_profile_info(context)
    get_track_info(context)
    get_artist_info(context)

    return flask.render_template("stats.html", **context)


def get_profile_info(context):
    """Get the user's general profile info:"""
    profile_info = requests.get("https://api.spotify.com/v1/me", headers=flask.session["header"])

    code = spotifyapp.model.check_status_code(context, "profile_info_", profile_info)

    if code == 200:
        profile_info = profile_info.json()
        context["profile_info"] = profile_info

def get_track_info(context):
    """Get the user's top 10 tracks from the last six months."""
    track_info = requests.get("https://api.spotify.com/v1/me/top/tracks?limit=10", headers=flask.session["header"])

    code = spotifyapp.model.check_status_code(context, "track_info_", track_info)

    if code == 200:
        track_info = track_info.json()
        context["track_info"] = track_info["items"]

def get_artist_info(context):
    """Get the user's top 10 artists from the last six months."""
    artist_info = requests.get("https://api.spotify.com/v1/me/top/artists?limit=10", headers=flask.session["header"])

    code = spotifyapp.model.check_status_code(context, "artist_info_", artist_info)

    if code == 200:
        artist_info = artist_info.json()
        context["artist_info"] = artist_info["items"]