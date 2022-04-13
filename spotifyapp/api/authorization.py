"""
Spotify API authorization endpoints.
"""
import flask
import spotifyapp
import requests
import datetime
from urllib.parse import urlencode

@spotifyapp.app.route('/authorize/')
def connect_to_spotify():
    """Authorize the user to connect their spotify account with the app."""

    # Make initial authorization request to authorize our app with the spotify account.
    query_params = {
        "client_id": "<CLIENT ID HERE>",
        "response_type": "code",
        "redirect_uri": "http://localhost:8000/get_token/",
        "scope": "user-library-read user-top-read user-read-email",
        "show_dialog": True
    }

    url = "https://accounts.spotify.com/authorize/"
    url = url + "?" + urlencode(query_params)

    # We want to redirect to this url, not just send an HTTP request to it.
    return flask.redirect(url)


@spotifyapp.app.route('/get_token/')
def get_access_token():
    """
    Obtain the auth token for the user to allow for future API requests.
    This is the callback for the /authorize/ root.
    """

    # First check if the authorization worked properly:
    if "error" in flask.request.args:
        flask.abort(flask.Response('There was an error while authorizing your spotify account.'))

    spotify_response_code = flask.request.args.get("code")

    # Define JSON body for get request.
    body = {
        "grant_type": "authorization_code",
        "code": spotify_response_code,
        "redirect_uri": "http://localhost:8000/get_token/",
        "client_id": "<CLIENT ID HERE>",
        "client_secret": "<CLIENT SECRET HERE>"
    }

    # Make get request to obtain user's access token.
    auth_response = requests.post("https://accounts.spotify.com/api/token", data=body)

    # Check the status of the response:
    if auth_response.status_code != 200:
        flask.abort(flask.Response('Could not obtain access token.'))

    auth_response = auth_response.json()

    header = {
        "Authorization": "Bearer " + auth_response["access_token"]
    }

    # Store the new auth header for this user in their cookie.
    flask.session["header"] = header
    flask.session["time_authorized"] = datetime.datetime.now(datetime.timezone.utc)
    return flask.redirect("/")