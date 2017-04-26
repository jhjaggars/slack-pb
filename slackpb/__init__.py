#!/usr/bin/env python

from __future__ import absolute_import, division, print_function
import json
import requests
import sys
import os
import argparse


API_BASE = "https://slack.com/api/"
UPLOAD_URL = "%s/files.upload" % API_BASE
USERS_URL = "%s/users.list" % API_BASE

TOKEN_FILE = "~/.slack-token"
USERS_FILE = "~/.slack-users.json"


def read_file(filename):
    with open(os.path.expanduser(filename)) as fp:
        return fp.read().strip()


def write_file(filename, content):
    with open(os.path.expanduser(filename), "w") as fp:
        fp.write(content)


def load_users():
    if not os.path.exists(USERS_FILE):
        write_file(
            USERS_FILE,
            requests.post(USERS_URL, data={"token": read_file(TOKEN_FILE)}).text
        )

    content = read_file(USERS_FILE)
    doc = json.loads(content)

    return {u["name"]: u["id"] for u in doc["members"]}


def paste(filename, token=read_file(TOKEN_FILE), filetype="auto", channels=None, filename_override=None):

    if filename == "-":
        content = sys.stdin.read().strip()
    else:
        content = read_file(filename)

    payload = {
        "content": content,
        "filetype": filetype,
        "token": token,
        "filename": filename_override or filename
    }

    if channels:
        users = load_users()

        def replace_channel(channel):
            if channel.startswith("#"):
                return channel
            else:
                return users[channel]

        payload["channels"] = ",".join(replace_channel(c) for c in channels)

    resp = requests.post(UPLOAD_URL, data=payload)
    print(resp.json()["file"]["permalink"])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--channels", nargs="*", default=None)
    parser.add_argument("--filetype", default="auto")
    parser.add_argument("--filename", default=None)
    parser.add_argument("file")

    args = parser.parse_args()

    paste(args.file, filetype=args.filetype, channels=args.channels, filename_override=args.filename)

if __name__ == "__main__":
    main()
