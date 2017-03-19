#!/bin/sh

set -ex

bundle exec jekyll clean
bundle exec jekyll build
rsync -avr --delete-after --delete-excluded --exclude-from=exclude_upload.txt _site/ holger@holger-peters.de:/home/holger/public_html
