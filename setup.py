"""
SpotifyApp python package configuration.

Nathan Rossol <nrossol@umich.edu>
"""

from setuptools import setup

setup(
    name='spotifyapp',
    version='0.1.0',
    packages=['spotifyapp'],
    include_package_data=True,
    install_requires=[
        'Flask',
	'requests',
    ],
    python_requires='>=3.8',
)
