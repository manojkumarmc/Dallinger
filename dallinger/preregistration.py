"""Preregister experiments through the Open Science Framework."""

import requests

username = ""
password = ""

root = "https://api.osf.io/v2"


def register(id):
    """Preregister the experiment."""
    create_osf_project()


def create_osf_project(id):
    requests.post(
        "{}/nodes/".format(root),
        auth=(username, password),
        data={
            "type": "nodes",
            "category": "project",
            "title": "",
            "description": "",
        }
    )
