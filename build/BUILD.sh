#!/bin/bash

set -e
cd "$( dirname "${BASH_SOURCE[0]}" )"

curl -O ftp://ftp.fu-berlin.de/pub/misc/movies/database/temporaryaccess/actors.list.gz
curl -O ftp://ftp.fu-berlin.de/pub/misc/movies/database/temporaryaccess/actresses.list.gz
curl -O ftp://ftp.fu-berlin.de/pub/misc/movies/database/temporaryaccess/genres.list.gz
curl -O ftp://ftp.fu-berlin.de/pub/misc/movies/database/temporaryaccess/release-dates.list.gz

python ./BUILD.py
