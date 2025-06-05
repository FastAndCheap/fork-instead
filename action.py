# SPDX-FileCopyrightText: 2025 Alec Delaney
# SPDX-License-Identifier: MIT

# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "pygithub",
# ]
# ///

"""Script for suggesting forking the repository for new issues and/or pull requests."""

import json
import os
import sys

import github

def envvar_as_bool(envvar_name: str) -> bool:
    """Convert a string environment variable to a boolean."""
    envvar = os.environ["INPUT_ASSIGN_TO_USER"].lower()
    if envvar not in ("y", "yes", "n", "no", "true", "false", "on", "off"):
        print(f"'{envvar_name}' must be a YAML boolean value")
        sys.exit(1)
    return envvar in ("y", "yes", "true", "on")

try:
    token = os.environ["INPUT_GITHUB_TOKEN"]

    message = os.environ["INPUT_MESSAGE"]

    on_issues = envvar_as_bool("INPUT_ON_ISSUES")
    on_pull_requests = envvar_as_bool("INPUT_LABEL")
    lock = envvar_as_bool("INPUT_LOCK")
    close = envvar_as_bool("INPUT_CLOSE")

    repo = os.environ["ACTION_REPO"]
    event_path = os.environ["ACTION_EVENT_PATH"]

    with open(event_path) as jsonfile:
        event = json.load(jsonfile)

    if event["type"] == "IssuesEvent" and event["action"] == "opened":
        number: int = event["issue"]["number"]
        is_issue = True
    elif event["type"] == "PullRequestEvent" and event["action"] in ("opened", "reopened"):
        number: int = event["pull_request"]["number"]
        is_issue = False
    else:
        print("Ah good, nothing to do here")
        sys.exit(0)

    g = github.Github(token)
    g_repo = g.get_repo(repo)
    g_issue = g_repo.get_issue(number) if is_issue else g_repo.get_pull(number).as_issue()
    g_issue.create_comment(message)

    if lock:
        g_issue.lock("resolved")

    if close:
        g_issue.edit(state="closed", state_reason="not_planned")

except SystemExit:
    raise

except:
    print("Something went wrong while performing the action.")
    print("You've met with a terrible fate, haven't you?")
    sys.exit(1)
