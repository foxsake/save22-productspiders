#!/bin/bash

if [ $# -eq 0 ]
  then
    echo "Usage: "
    echo "testspider.sh [options] <spider name>"
    echo ""
    echo "Options:"
    echo "--remold : remove old .csv and .log files"
    echo "TODO!"
fi

#delete .pyc files
find . -name '*.pyc' | xargs rm -rf

#delete old files
rm $1*.csv
rm $1*.log

#repeat scrapy run n times. TODO
echo 'running...'
for i in `seq 1 1`;
    do
        runpart="scrapy crawl $1 -o $1$i.csv --loglevel DEBUG --logfile=$1$i.log";
        $runpart
    done
zip -m -T $1.zip $1*

echo "kdonebye:-)"

# if test $i -ne 1; then
        #     run=$run" && "$runpart;
        # else
        #     run=$runpart;
        # fi;
#run="$run && zip -m -T $1.zip $1*"
#echo "i will run the command = $run"
# echo $run