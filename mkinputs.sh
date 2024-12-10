#!/bin/zsh

for i in `seq 1 1 25`; do
    NUM=$(printf %02d $i)
    sed "s/\\$\\$/$NUM/g" template.py > day_${NUM}.py
done
