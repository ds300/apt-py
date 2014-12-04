# Installation

This requires berkeley db, which can be installed via homebrew for OSX, or using a real package manager if you're using a sane linux distribution.

    brew install berkeley-db

The python bindings for berkeleydb (in package bsddb3) need to know where berekeleydb is during the setup script, so you need to set the `BERKELEYDB_DIR` environment variable before running pip.

e.g.

    sudo BERKELEYDB_DIR=$(brew --cellar)/berkeley-db/5.3.28 pip install -r requirements.txt

And that should be it.