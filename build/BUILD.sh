#!/bin/bash

set -e
cd "$( dirname "${BASH_SOURCE[0]}" )"

curl -O ftp://ftp.fu-berlin.de/pub/misc/movies/database/actors.list.gz
curl -O ftp://ftp.fu-berlin.de/pub/misc/movies/database/actresses.list.gz
curl -O ftp://ftp.fu-berlin.de/pub/misc/movies/database/genres.list.gz
curl -O ftp://ftp.fu-berlin.de/pub/misc/movies/database/release-dates.list.gz

python ./BUILD.py
