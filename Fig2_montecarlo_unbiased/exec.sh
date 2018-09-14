#!/bin/bash

time python3 hopfield_meanfield_montecarlo_multi.py
python3 plot.py
python3 plot_overlap_2D.py
python3 plot_cor_2D.py
python3 plot_meanrate.py
