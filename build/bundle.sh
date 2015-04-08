#!/bin/bash

cd $(dirname "$0")
cd ../..
pwd
rm -f Pandas-Tutorial.zip
zip Pandas-Tutorial.zip \
    pandas-tutorial/Exercises* \
    pandas-tutorial/Solutions* \
    pandas-tutorial/*.css \
    pandas-tutorial/cheat-sheet.txt \
    pandas-tutorial/sales*.csv \
    pandas-tutorial/data/*.csv
