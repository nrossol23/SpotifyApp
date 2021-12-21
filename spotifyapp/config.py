"""SpotifyApp devlopment configuration."""

import pathlib

# Root of this application, useful if it doesn't occupy an entire domain
APPLICATION_ROOT = '/'

# Secret key for encrypting cookies
SECRET_KEY = (b"*\xb2\x82N\x0e\x8c\n\xcd?\xf2x\xfcQ"
              b"\x97\xe6Sv\x85\xf7X\xc8\xc0jS")
SESSION_COOKIE_NAME = 'login'

# File Upload to var/uploads/
SPOTIFYAPP_ROOT = pathlib.Path(__file__).resolve().parent.parent
UPLOAD_FOLDER = SPOTIFYAPP_ROOT/'var'/'uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
MAX_CONTENT_LENGTH = 16 * 1024 * 1024

# Database file is var/spotifyapp.sqlite3
DATABASE_FILENAME = SPOTIFYAPP_ROOT/'var'/'spotifyapp.sqlite3'
