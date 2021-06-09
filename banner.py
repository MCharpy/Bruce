#!/usr/bin/env python3

from PIL import Image
import git
import pytz
import datetime

# List of project files to commit (as every run reset the repo)
project_files = ['banner.py', 'requirements.txt', 'banner.png', 'README.md', 'img']


# Opens banner image. It must be black and white and at most 52 in width and 7 in height
with Image.open("banner.png") as image:
    # Open the current repo to work on it
    repo = git.Repo.init('.')
    # Resets the repo
    repo.git.update_ref('-d', 'HEAD')
    # Add every important files for the next commit
    repo.index.add(project_files)

    day_delta = datetime.timedelta(days=1)

    # Get date with UTC timezone and hour at midday
    today = pytz.utc.localize(datetime.datetime.now().replace(hour=12, minute=0, second=0, microsecond=0))

    # Get first sunday at least one year ago
    first_day = today - datetime.timedelta(weeks=52)
    while (first_day.weekday() != 6):
        first_day -= day_delta

    # For each possible position in the github contributions graph, get the pixel color in the image and create a commit if the pixel is black
    for x in range(image.width):
        for y in range(image.height):
            if image.getpixel((x,y))[0] == 0:
                repo.index.commit('Pixel ' + first_day.strftime("%a %b %d %H:%M:%S %Y %z") + ' at x ' + str(x) + ' y ' + str(y), author_date=first_day)
            first_day += day_delta
