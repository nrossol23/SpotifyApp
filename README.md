# SpotifyApp

Created using Python and Flask and utilizes Spotify's official web API. The app allows users to easily connect and authenticate their own Spotify account and gain access to in depth statistics and recommendations based on their own listening activity.

Author: Nathan Rossol

This app requires a client id and client secret key to run. Here is how to set this up:
  1. Create a spotify developer account here: https://developer.spotify.com/dashboard/
  2. Create a new app
  3. Click on the new app and paste the client ID into all lines showing "<CLIENT ID HERE>" in authorization.py.
  4. Paste the client secret into all lines showing "<CLIENT SECRET HERE>" in authorization.py.

In order to run this web app locally:
  1. Clone this repo.
  2. If on MacOS, install python using:
     "brew install python3"
     If on WSL or Linux, install python using:
     "sudo apt-get update" and
     "sudo apt-get install python3 python3-pip python3-venv python3-wheel python3-setuptools"
  4. Run the "spotifyinstall" script located in the bin folder.
  5. Ensure you are in the newly created virtual environment by using: "source env/bin/activate".
  6. Run the "spotifyrun" script located in the bin folder.
  7. Connect to localhost:8000.
