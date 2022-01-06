"""SpotifyApp model (database) API."""
import sqlite3
import flask
import spotifyapp
import requests

def dict_factory(cursor, row):
    """Convert database row objects to a dictionary keyed on column name.

    This is useful for building dictionaries which are then used to render a
    template.  Note that this would be inefficient for large queries.
    """
    return {col[0]: row[idx] for idx, col in enumerate(cursor.description)}


def get_db():
    """Open a new database connection.

    Flask docs:
    https://flask.palletsprojects.com/en/1.0.x/appcontext/#storing-data
    """
    if 'sqlite_db' not in flask.g:
        db_filename = spotifyapp.app.config['DATABASE_FILENAME']
        flask.g.sqlite_db = sqlite3.connect(str(db_filename))
        flask.g.sqlite_db.row_factory = dict_factory

        # Foreign keys have to be enabled per-connection.  This is an sqlite3
        # backwards compatibility thing.
        flask.g.sqlite_db.execute("PRAGMA foreign_keys = ON")

    return flask.g.sqlite_db


@spotifyapp.app.teardown_appcontext
def close_db(error):
    """Close the database at the end of a request.

    Flask docs:
    https://flask.palletsprojects.com/en/1.0.x/appcontext/#storing-data
    """
    assert error or not error  # Needed to avoid superfluous style error
    sqlite_db = flask.g.pop('sqlite_db', None)
    if sqlite_db is not None:
        sqlite_db.commit()
        sqlite_db.close()


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