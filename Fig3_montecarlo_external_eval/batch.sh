#!/bin/bash

for BIAS in 0.5 0.1
do
    for POS in 5 10 20
    do
        python meanfield_montecarlo_multi_external.py $BIAS $POS
        python plot.py
        DIR=p${BIAS}_inputpos${POS}
        mkdir ${DIR}
        mv *.csv *.svg $DIR
    done
done
