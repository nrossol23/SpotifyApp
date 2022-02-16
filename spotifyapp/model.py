"""SpotifyApp model."""
import flask
import spotifyapp
import requests

def check_status_code(context, prefix, response):
    """Check the status code of the http response, and generate errors if applicable."""
    if response.status_code == 200:
        context[prefix + "status_code"] = 200
        return 200
    if response.status_code == 401:
        context[prefix + "status_code"] = 401
        context[prefix + "error"] = "There was an error with you access token. Please re-authenticate."
        return 401
    elif response.status_code == 403:
        context[prefix + "status_code"] = 403
        context[prefix + "error"] = "There was a bad OAuth request, which could be caused by several things. \
                            Please try again or re-authenticate."
        return 403
    elif response.status_code == 429:
        context[prefix + "status_code"] = 429
        context[prefix + "error"] = "The app is currently experiencing too many requests at once. Please try again later."
        return 429