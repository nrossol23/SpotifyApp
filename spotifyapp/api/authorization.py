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

    return flask.redirect(url)


@spotifyapp.app.route('/get_token/')
def get_auth_token():
    """Obtain the auth token for the user to allow for future API requests."""

    spotify_response_code = flask.request.args.get("code")

    # Define JSON body for get request.
    body = {
        "grant_type": "authorization_code",
        "code": spotify_response_code,
        "redirect_uri": "http://172.17.162.159:8000/get_token/",
        "client_id": "b23c8c7be9f04bda9183dd13c8a89464",
        "client_secret": "d6f30a312ad745ab8c2250cc764f01ae"
    }

    # Make get request to obtain user's auth token.
    auth_response = requests.post("https://accounts.spotify.com/api/token", data=body)
    auth_response = auth_response.json()

    print(auth_response)
    
    header = {
        "Authorization": "Bearer " + auth_response["access_token"]
    }

    # Store the new auth header for this user in their cookie.
    flask.session["header"] = header
    return flask.redirect("show_index")