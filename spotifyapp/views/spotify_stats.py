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

    # Get the user's general profile info:
    profile_info = requests.get("https://api.spotify.com/v1/me", headers=flask.session["header"])

    # Check the response's status code:
    if profile_info.status_code == 200:
        context["profile_info_status_code"] = 200
        profile_info = profile_info.json()
        context["profile_info"] = profile_info

        # Now attempt to grab the user's top tracks and artists info:
        get_track_info(context)
        get_artist_info(context)

    elif profile_info.status_code == 401:
        context["profile_info_status_code"] = 401
        context["profile_info_error"] = "There was an error with you access token. Please re-authenticate."

    elif profile_info.status_code == 403:
        context["profile_info_status_code"] = 403
        context["profile_info_error"] = "There was a bad OAuth request, which could be caused by several things. \
                            Please try again or re-authenticate."

    elif profile_info.status_code == 429:
        context["profile_info_status_code"] = 429
        context["profile_info_error"] = "The app is currently experiencing too many requests at once. Please try again later."

    return flask.render_template("stats.html", **context)


def get_track_info(context):
    """Get the user's top 6 tacks from the last six months."""
    track_info = requests.get("https://api.spotify.com/v1/me/top/tracks?limit=10", headers=flask.session["header"])

    # Check the response's status code:
    if track_info.status_code == 200:
        context["track_info_status_code"] = 200
        track_info = track_info.json()
        context["track_info"] = track_info["items"]

    elif track_info.status_code == 401:
        context["track_info_status_code"] = 401
        context["track_info_error"] = "There was an error with you access token. Please re-authenticate."

    elif track_info.status_code == 403:
        context["track_info_status_code"] = 403
        context["track_info_error"] = "There was a bad OAuth request, which could be caused by several things. \
                            Please try again or re-authenticate."

    elif track_info.status_code == 429:
        context["track_info_status_code"] = 429
        context["track_info_error"] = "The app is currently experiencing too many requests at once. Please try again later."


def get_artist_info(context):
    """Get the user's top 6 tacks from the last six months."""
    artist_info = requests.get("https://api.spotify.com/v1/me/top/artists?limit=10", headers=flask.session["header"])

    # Check the response's status code:
    if artist_info.status_code == 200:
        context["artist_info_status_code"] = 200
        artist_info = artist_info.json()
        context["artist_info"] = artist_info["items"]

    elif artist_info.status_code == 401:
        context["artist_info_status_code"] = 401
        context["artist_info_error"] = "There was an error with you access token. Please re-authenticate."

    elif artist_info.status_code == 403:
        context["artist_info_status_code"] = 403
        context["artist_info_error"] = "There was a bad OAuth request, which could be caused by several things. \
                            Please try again or re-authenticate."

    elif artist_info.status_code == 429:
        context["artist_info_status_code"] = 429
        context["artist_info_error"] = "The app is currently experiencing too many requests at once. Please try again later."