"""
Spotify API authorization endpoints.
"""
import flask
import spotifyapp
import requests
from urllib.parse import urlencode

@spotifyapp.app.route('/authorize/')
def connect_to_spotify():
    """Authorize the user to connect their spotify account with the app."""

    # Make initial authorization request to authorize our app with the spotify account.
    query_params = {
        "client_id": "b23c8c7be9f04bda9183dd13c8a89464",
        "response_type": "code",
        "redirect_uri": "http://172.17.162.159:8000/get_token/",
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
        flask.abort(Response('There was an error while authorizing your spotify account.'))

    spotify_response_code = flask.request.args.get("code")

    # Define JSON body for get request.
    body = {
        "grant_type": "authorization_code",
        "code": spotify_response_code,
        "redirect_uri": "http://172.17.162.159:8000/get_token/",
        "client_id": "b23c8c7be9f04bda9183dd13c8a89464",
        "client_secret": "d6f30a312ad745ab8c2250cc764f01ae"
    }

    # Make get request to obtain user's access token.
    auth_response = requests.post("https://accounts.spotify.com/api/token", data=body)
    auth_response = auth_response.json()

    # Check the status of the response:
    if auth_response.status_code is not "200":
        flask.abort(Response('Could not obtain access token.'))

    header = {
        "Authorization": "Bearer " + auth_response["access_token"]
    }

    # Store the new auth header for this user in their cookie.
    flask.session["header"] = header
    flask.session["refresh_token"] = auth_response["refresh_token"]
    return flask.redirect("show_index")


@spotifyapp.app.route('/refresh_token/')
def refresh_token():
    """Refresh the user's access token after expiration."""

    body = {
        "grant_type": "refresh_token",
        "refresh_token": flask.session["refresh_token"],
        "client_id": "b23c8c7be9f04bda9183dd13c8a89464"
    }

    # Authorization header must include client id and client secret.
    headers = {
        "Authorization": "Basic " + "b23c8c7be9f04bda9183dd13c8a89464" + ":" + "d6f30a312ad745ab8c2250cc764f01ae"
    }

    refresh_response = requests.post("https://accounts.spotify.com/api/token", headers=headers)
    refresh_response = refresh_response.json()

    # Update to the new token:
    new_access_header = {
        "Authorization": "Bearer " + refresh_response["access_token"]
    }

    flask.session["header"] = new_access_header
    return flask.redirect("show_index")