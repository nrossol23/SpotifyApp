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

    # Get the user's general profile info:
    profile_info = requests.get("https://api.spotify.com/v1/me", headers=flask.session["header"])

    # Check the response's status code:
    if profile_info.status_code == 200:
        context["status_code"] = 200
        profile_info = profile_info.json()
        context["user_data"] = profile_info
        context["error"] = "No errors."

    elif profile_info.status_code == 401:
        context["status_code"] = 401
        context["error"] = "There was an error with you access token. Please re-authenticate."

    elif profile_info.status_code == 403:
        context["status_code"] = 403
        context["error"] = "There was a bad OAuth request, which could be caused by several things. \
                            Please try again or re-authenticate."

    elif profile_info.status_code == 429:
        context["status_code"] = 429
        context["error"] = "The app is currently experiencing too many requests at once. Please try again later."

    print(context)

    return flask.render_template("stats.html", **context)