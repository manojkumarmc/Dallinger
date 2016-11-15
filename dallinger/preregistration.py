"""Preregister experiments through the Open Science Framework."""

import os
import requests

personal_access_token = os.environ.get('OSF_ACCESS_TOKEN')

root = "https://api.osf.io/v2"


def register(id):
    """Preregister the experiment."""
    create_osf_project()


def create_osf_project(id):
    requests.post(
        "{}/nodes/".format(root),
        data={
            "type": "nodes",
            "category": "project",
            "title": "hello",
            "description": "",
        },
        headers={
            "Authorization": "Bearer {}".format(personal_access_token)
        }
    )
