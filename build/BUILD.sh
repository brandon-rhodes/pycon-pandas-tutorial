#!/bin/bash
#
# All we want is the CSV files, but "imdbpy2sql.py" will not create them
# unless it believes it can really talk to postgresql.

wget -nc -nd -r -l 1 ftp://ftp.fu-berlin.de/pub/misc/movies/database/
mkdir -p ../data
imdbpy2sql.py -d . -u sqlite:imdb.db -c . --csv-only-write
chmod -w *.csv
rm *.db

#imdbpy2sql.py -d . -u postgres://host/database -c ../data --csv-only-write
