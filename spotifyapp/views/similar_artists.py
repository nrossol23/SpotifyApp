"""
SpotifyApp similar artists view.
"""
import flask
import spotifyapp
import datetime
import requests

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
        
    # Get the related artists for this user:
    get_related_artists(context)

    print(context["artists"])
    
    return flask.render_template("similar_artists.html", **context)


def get_related_artists(context):
    # First, we want to gather the user's top artists:
    top_artists = requests.get("https://api.spotify.com/v1/me/top/artists?limit=3", headers=flask.session["header"])

    code = spotifyapp.model.check_status_code(context, "", top_artists)

    if code == 200:
        top_artists = top_artists.json()["items"]
    else:
        return # Stop if error present


    # Next, we want to get related artists of the top 3 artists.
    related_artists = []

    # Loop through every top artist
    for artist in top_artists:
        related_subset = requests.get("https://api.spotify.com/v1/artists/" + artist["id"] +"/related-artists", headers=flask.session["header"])

        code = spotifyapp.model.check_status_code(context, "", related_subset)

        if code == 200:
            related_subset = related_subset.json()["artists"]
            for artist in related_subset:
                related_artists.append(artist)
        else:
            return # Stop if error present.

    context["artists"] = related_artists