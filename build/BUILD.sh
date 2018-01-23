#!/bin/bash

set -e
cd "$( dirname "${BASH_SOURCE[0]}" )"

curl -O ftp://ftp.fu-berlin.de/misc/movies/database/frozendata/actors.list.gz
curl -O ftp://ftp.fu-berlin.de/misc/movies/database/frozendata/actresses.list.gz
curl -O ftp://ftp.fu-berlin.de/misc/movies/database/frozendata/genres.list.gz
curl -O ftp://ftp.fu-berlin.de/misc/movies/database/frozendata/release-dates.list.gz

python ./BUILD.py
