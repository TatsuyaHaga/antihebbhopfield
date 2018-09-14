#!/bin/bash

time python3 hopfield_meanfield_montecarlo_multi.py
python3 plot_maxoverlap_2D.py
python3 plot_cornum_2D.py
