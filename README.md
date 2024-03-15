# Sonic Pi Logging
This is the repo for Sonic Pi with logging stated in Eric dissertation.

## Features

This repo is built on Sonic Pi version 3.2.2 and the logging function utilizes C++.

The server runs on the following packages:

-   [Flask](https://flask.palletsprojects.com/en/3.0.x/)
-   [MySQL](https://www.mysql.com/)
-   [SQLAlchemy](https://www.sqlalchemy.org/)

## Pre-requirements for server

Standard Python development environment with Flask package for hosting the server.

MySQL for hosting database.

An IDE for code editing.

## Pre-requirements for Sonic Pi logging

Visual Studio IDE (or any other IDE compatible with Qt) for code editing.

## Server setup

-   Clone
    -   `git clone https://anonymous.4open.science/r/dissertation_repo_sonicpi/git`
-   Create a virtual environment (optional)
    -   `conda create -n sonicpilogging python=3.7 -y`
    -   `conda activate sonicpilogging`
-   Install requirements
    -   `pip install -r repo/sonic-py-flask/requirements.txt`
-   Install database
    -   Install your own MySQL and set it up
    -   Go to `repo/sonic-py-flask/model.py`
    -   Modify the database information between lines 9 and 16
-   Run
    -   cd `repo/sonic-py-flask/`
    -   `python main.py`

## Sonic Pi build

This logging only add two logging files to the original Sonic Pi files without modifying it's own software structure, thus, the build method is referred to the original build method in several MD files in this repo, called "INSTALL-[OS].md"

Directory for logging functions files is `repo/app/gui/qt/eric_logging`
