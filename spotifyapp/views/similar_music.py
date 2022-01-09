"""
SpotifyApp similar music view.
"""
import flask
import spotifyapp
import datetime
import requests

@spotifyapp.app.route('/similar_music/')
def show_similar_music():

    # Determine if the user is authorized:
    if 'header' not in flask.session:
        context = {
            "authorized": False,
            "expired": False,
        }
        return flask.render_template("similar_music.html", **context)

    context = {
        "authorized": True,
        "expired": False,
    }

    # Perform access token check if user is authorized:
    if (datetime.datetime.now(datetime.timezone.utc) - flask.session["time_authorized"]).total_seconds() >= 3540:
        context["expired"] = True
        return flask.render_template("similar_music.html", **context)
        
    # Get the related songs for this user:
    get_related_songs(context)
    
    return flask.render_template("similar_music.html", **context)


def get_related_songs(context):
    # First, we want to gather the user's top artists:
    top_artists = requests.get("https://api.spotify.com/v1/me/top/artists?limit=3", headers=flask.session["header"])

    code = spotifyapp.model.check_status_code(context, "", top_artists)

    if code == 200:
        top_artists = top_artists.json()["items"]
    else:
        return # Stop if error present

    # We must add all 5 seed artists for the best results:
    link = "https://api.spotify.com/v1/recommendations?seed_artists="

    for i, artist in enumerate(top_artists):
        id = artist["id"]
        link += id
        if i < len(top_artists) - 1:
            link += "," 

    link += "&limit=50"

    songs = requests.get(link, headers=flask.session["header"])

    code = spotifyapp.model.check_status_code(context, "", songs)

    if code == 200:
        context["songs"] = songs.json()["tracks"]
    else:
        return
