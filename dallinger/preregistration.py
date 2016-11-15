"""Preregister experiments through the Open Science Framework."""

import os
import requests

personal_access_token = os.environ.get('OSF_ACCESS_TOKEN')

root = "https://api.osf.io/v2"


def register(id, snapshot):
    """Preregister the experiment."""
    create_osf_project()


def create_osf_project(id, description=None):

    if not description:
        description = "Experiment preregistered by Dallinger."

    requests.post(
        "{}/nodes/".format(root),
        data={
            "type": "nodes",
            "category": "project",
            "title": id,
            "description": description,
        },
        headers={
            "Authorization": "Bearer {}".format(personal_access_token)
        }
    )

create_osf_project("2423-234-234-234-23")
