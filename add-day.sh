#!/bin/bash
day_num=$1
day_dir=2023/day_${day_num}


if ! [ -d day_dir ]; then
    mkdir $day_dir
    touch ${day_dir}/example_input.txt
    cp solution.template.py ${day_dir}/solution.py
fi
